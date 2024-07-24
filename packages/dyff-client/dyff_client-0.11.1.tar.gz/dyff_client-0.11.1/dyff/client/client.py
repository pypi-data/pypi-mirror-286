# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Optional, Protocol, TypeVar, Union
from warnings import warn

import httpx
from azure.core.credentials import AccessToken, TokenCredential

# We bring this into our namespace so that people can catch it without being
# confused by having to import 'azure.core'
from azure.core.exceptions import HttpResponseError
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.policies import BearerTokenCredentialPolicy
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest

from dyff.schema.adapters import Adapter, create_pipeline
from dyff.schema.base import DyffBaseModel
from dyff.schema.dataset import arrow, binary
from dyff.schema.platform import (
    Artifact,
    ArtifactURL,
    DataSchema,
    Dataset,
    Digest,
    Documentation,
    DyffEntity,
    Evaluation,
    InferenceInterface,
    InferenceService,
    InferenceSession,
    InferenceSessionAndToken,
    Label,
    Measurement,
    Method,
    Model,
    Module,
    Report,
    SafetyCase,
    Status,
    StorageSignedURL,
)
from dyff.schema.requests import (
    AnalysisCreateRequest,
    DatasetCreateRequest,
    DocumentationEditRequest,
    EvaluationCreateRequest,
    InferenceServiceCreateRequest,
    InferenceSessionCreateRequest,
    InferenceSessionTokenCreateRequest,
    LabelUpdateRequest,
    MethodCreateRequest,
    ModelCreateRequest,
    ModuleCreateRequest,
    ReportCreateRequest,
)

from ._generated import DyffV0API as RawClient
from ._generated._serialization import Serializer
from ._generated.operations._operations import (
    DatasetsOperations as DatasetsOperationsGenerated,
)
from ._generated.operations._operations import (
    EvaluationsOperations as EvaluationsOperationsGenerated,
)
from ._generated.operations._operations import (
    InferenceservicesOperations as InferenceservicesOperationsGenerated,
)
from ._generated.operations._operations import (
    InferencesessionsOperations as InferencesessionsOperationsGenerated,
)
from ._generated.operations._operations import (
    MeasurementsOperations as MeasurementsOperationsGenerated,
)
from ._generated.operations._operations import (
    MethodsOperations as MethodsOperationsGenerated,
)
from ._generated.operations._operations import (
    ModelsOperations as ModelsOperationsGenerated,
)
from ._generated.operations._operations import (
    ModulesOperations as ModulesOperationsGenerated,
)
from ._generated.operations._operations import (
    ReportsOperations as ReportsOperationsGenerated,
)
from ._generated.operations._operations import (
    SafetycasesOperations as SafetycasesOperationsGenerated,
)

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import (
        MutableMapping,  # type: ignore  # pylint: disable=ungrouped-imports
    )
JSON = MutableMapping[str, Any]  # pylint: disable=unsubscriptable-object
T = TypeVar("T")
ClsType = Optional[
    Callable[[PipelineResponse[HttpRequest, HttpResponse], T, dict[str, Any]], Any]
]


_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


QueryT = Union[str, dict[str, Any], list[dict[str, Any]]]


def _require_id(x: DyffEntity | str) -> str:
    if isinstance(x, str):
        return x
    elif x.id is not None:
        return x.id
    else:
        raise ValueError(".id attribute not set")


def _encode_query(query: QueryT | None) -> Optional[str]:
    if query is None:
        return None
    elif isinstance(query, (list, dict)):
        query = json.dumps(query)
    return query


def _encode_labels(labels: Optional[dict[str, str]]) -> Optional[str]:
    """The Python client accepts 'annotations' and 'labels' as dicts, but they need to
    be json-encoded so that they can be forwarded as part of the HTTP query
    parameters."""
    if labels is None:
        return None
    # validate
    for k, v in labels.items():
        try:
            Label(key=k, value=v)
        except Exception as ex:
            raise HttpResponseError(
                f"label ({k}: {v}) has invalid format", status_code=400
            ) from ex
    return json.dumps(labels)


def _check_deprecated_verify_ssl_certificates(
    verify_ssl_certificates: bool, insecure: bool
):
    """Check if the deprecated parameter verify_ssl_certificates is set to insecure."""
    # verify_ssl_certificates deprecated
    # remove after 10/2024
    return not verify_ssl_certificates or insecure


def _retry_not_found(fn):
    def _impl(*args, **kwargs):
        delays = [1.0, 2.0, 5.0, 10.0, 10.0]
        retries = 0
        while True:
            try:
                return fn(*args, **kwargs)
            except HttpResponseError as ex:
                if ex.status_code == 404 and retries < len(delays):
                    time.sleep(delays[retries])
                    retries += 1
                else:
                    raise

    return _impl


def _downlinks(raw_ops, resource_id: str) -> list[ArtifactURL]:
    return [ArtifactURL.parse_obj(link) for link in raw_ops.downlinks(resource_id)]


_ResourceOperationsType = Union[
    "DatasetsOperations",
    "EvaluationsOperations",
    "MeasurementsOperations",
    "ModulesOperations",
    "ReportsOperations",
    "SafetycasesOperations",
]


def _download(
    ops: _ResourceOperationsType,
    resource_id: str,
    destination: Path | str,
    *,
    insecure: bool = False,
) -> None:
    destination = Path(destination).resolve()
    links = ops.downlinks(resource_id)

    file_links: list[ArtifactURL] = []
    file_paths: list[Path] = []
    for link in links:
        file_path = destination / link.artifact.path
        if not file_path.is_dir():
            # Sometimes paths like "." get included because s3 is weird
            file_links.append(link)
            file_paths.append(file_path)

    destination.mkdir(parents=True)
    # TODO: Make the download resumable

    # TODO: Download in parallel
    for link, path in zip(file_links, file_paths):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fout:
            with httpx.stream(
                "GET",
                link.signedURL.url,
                headers=link.signedURL.headers,
                verify=not insecure,
            ) as response:
                for chunk in response.iter_raw():
                    fout.write(chunk)


def _stream_logs(
    raw_ops,
    resource_id: str,
    *,
    insecure: bool = False,
) -> Iterable[str]:
    link = ArtifactURL.parse_obj(raw_ops.logs(resource_id))
    with httpx.stream(
        "GET",
        link.signedURL.url,
        headers=link.signedURL.headers,
        verify=not insecure,
    ) as response:
        yield from response.iter_lines()


def _download_logs(
    raw_ops,
    resource_id: str,
    destination: Path | str,
    *,
    insecure: bool = False,
) -> None:
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(str(destination))
    destination.parent.mkdir(exist_ok=True, parents=True)

    link = ArtifactURL.parse_obj(raw_ops.logs(resource_id))
    with open(destination, "wb") as fout:
        with httpx.stream(
            "GET",
            link.signedURL.url,
            headers=link.signedURL.headers,
            verify=not insecure,
        ) as response:
            for chunk in response.iter_raw():
                fout.write(chunk)


def _access_label(
    access: Literal["public", "preview", "private"]
) -> dict[str, Optional[str]]:
    if access == "private":
        label_value = None
    elif access == "preview":
        # TODO: Change usage of "internal" to "preview" on the backend
        label_value = "internal"
    else:
        label_value = str(access)
    return {"dyff.io/access": label_value}


SchemaType = TypeVar("SchemaType", bound=DyffBaseModel)
SchemaObject = Union[SchemaType, dict[str, Any]]


def _parse_schema_object(
    t: type[SchemaType], obj: SchemaObject[SchemaType]
) -> SchemaType:
    """If ``obj`` is a ``dict``, parse it as a ``t``.

    Else return it unchanged.
    """
    if isinstance(obj, dict):
        return t.parse_obj(obj)
    else:
        return obj


class _OpsProtocol(Protocol):
    def label(self, resource_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified resource with key-value pairs (stored in the ``.labels``
        field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param resource_id: The ID of the resource to label.
        :type resource_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        ...


class _PublishMixin:
    def publish(
        self: _OpsProtocol,
        resource_id: str,
        access: Literal["public", "preview", "private"],
    ) -> None:
        """Set the publication status of the resource in the Dyff cloud app.

        Publication status affects only:

            1. Deliberate outputs, such as the rendered HTML from a safety case
            2. The resource spec
            3. Associated documentation

        Other artifacts -- source code, data, logs, etc. -- are never accessible
        to unauthenticated users.

        The possible access modes are:

            1. ``"public"``: Anyone can view the results
            2. ``"preview"``: Authorized users can view the results as they
                would appear if they were public
            3. ``"private"``: The results are not visible in the app
        """
        return self.label(resource_id, _access_label(access))


class InferenceSessionClient:
    """A client used for making inference requests to a running
    :class:`~dyff.schema.platform.InferenceSession`.

    .. note::

      Do not instantiate this class. Create an instance using
      :meth:`inferencesessions.client() <dyff.client.client.InferencesessionsOperations>`

      `verify_ssl_certifcates` is deprecated, use `insecure` instead.
    """

    def __init__(
        self,
        *,
        session_id: str,
        token: str,
        dyff_api_endpoint: str,
        inference_endpoint: str,
        input_adapter: Optional[Adapter] = None,
        output_adapter: Optional[Adapter] = None,
        verify_ssl_certificates: bool = True,
        insecure: bool = False,
    ):
        # verify_ssl_certificates deprecated
        # remove after 10/2024
        insecure = _check_deprecated_verify_ssl_certificates(
            verify_ssl_certificates, insecure
        )

        self._session_id = session_id
        self._token = token
        self._dyff_api_endpoint = dyff_api_endpoint

        self._inference_endpoint = inference_endpoint
        self._input_adapter = input_adapter
        self._output_adapter = output_adapter

        self._client = httpx.Client(
            timeout=httpx.Timeout(5, read=None), verify=not insecure
        )

    def infer(self, body: Any) -> Any:
        """Make an inference request.

        The input and output are arbitrary JSON objects. The required format depends on
        the endpoint and input/output adapters specified when creating the inference
        client.

        :param Any body: A JSON object containing the inference input.
        :returns: A JSON object containing the inference output.
        """
        url = httpx.URL(
            f"{self._dyff_api_endpoint}/inferencesessions"
            f"/{self._session_id}/infer/{self._inference_endpoint}"
        )
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

        def once(x):
            yield x

        body = once(body)
        if self._input_adapter is not None:
            body = self._input_adapter(body)
        request_body = None
        for i, x in enumerate(body):
            if i > 0:
                raise ValueError("adapted input should contain exactly one element")
            request_body = x
        if request_body is None:
            raise ValueError("adapted input should contain exactly one element")

        request = self._client.build_request(
            "POST", url, headers=headers, json=request_body
        )
        response = self._client.send(request, stream=True)
        response.raise_for_status()
        response.read()
        json_response = once(response.json())
        if self._output_adapter is not None:
            json_response = self._output_adapter(json_response)
        return list(json_response)


class DatasetsOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Dataset` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.datasets`` attribute of :class:`~dyff.client.Client`.

      `verify_ssl_certifcates` is deprecated, use `insecure` instead.
    """

    def __init__(
        self,
        _raw_ops: DatasetsOperationsGenerated,
        *,
        verify_ssl_certificates: bool = True,
        insecure: bool = False,
    ):
        self._raw_ops = _raw_ops

        # verify_ssl_certificates deprecated
        # remove after 10/2024
        insecure = _check_deprecated_verify_ssl_certificates(
            verify_ssl_certificates, insecure
        )

        self._verify_ssl_certificates = not insecure
        self._insecure = insecure

    def get(self, dataset_id: str) -> Dataset:
        """Get a Dataset by its key.

        :param dataset_id: The dataset key
        :type dataset_id: str
        :return: The Dataset with the given key.
        """
        return Dataset.parse_obj(self._raw_ops.get(dataset_id))

    def delete(self, dataset_id: str) -> Status:
        """Mark a Dataset for deletion.

        :param dataset_id: The dataset key
        :type dataset_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(dataset_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        name: Optional[str] = None,
    ) -> list[Dataset]:
        """Get all Datasets matching a query. The query is a set of equality constraints
        specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword name: Default value is None.
        :paramtype name: str
        :return: list of ``Dataset`` resources satisfying the query.
        :rtype: list[Dataset]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Dataset.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                name=name,
            )
        ]

    def label(self, dataset_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Dataset with key-value pairs (stored in the ``.labels``
        field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param dataset_id: The ID of the Dataset to label.
        :type dataset_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(dataset_id, labels)

    def create(self, request: SchemaObject[DatasetCreateRequest]) -> Dataset:
        """Create a Dataset.

        .. note::
            This operation may incur compute costs.

        :param request: The dataset request specification.
        :type request: DatasetCreateRequest | dict
        :return: A full Dataset entity with .id and other properties set.
        """
        request = _parse_schema_object(DatasetCreateRequest, request)
        dataset = _retry_not_found(self._raw_ops.create)(request.dict())
        return Dataset.parse_obj(dataset)

    def create_arrow_dataset(
        self, dataset_directory: Path | str, *, account: str, name: str
    ) -> Dataset:
        """Create a Dataset resource describing an existing Arrow dataset.

        Internally, constructs a ``DatasetCreateRequest`` using information
        obtained from the Arrow dataset, then calls ``create()`` with the
        constructed request.

        Typical usage::

            dataset = client.datasets.create_arrow_dataset(dataset_directory, ...)
            client.datasets.upload_arrow_dataset(dataset, dataset_directory)

        :param dataset_directory: The root directory of the Arrow dataset.
        :type dataset_directory: str
        :keyword account: The account that will own the Dataset resource.
        :type account: str
        :keyword name: The name of the Dataset resource.
        :type name: str
        :returns: The complete Dataset resource.
        :rtype: Dataset
        """
        dataset_path = Path(dataset_directory)
        ds = arrow.open_dataset(str(dataset_path))
        file_paths = list(ds.files)  # type: ignore[attr-defined]
        artifact_paths = [
            str(Path(file_path).relative_to(dataset_path)) for file_path in file_paths
        ]
        artifacts = [
            Artifact(
                kind="parquet",
                path=artifact_path,
                digest=Digest(
                    md5=binary.encode(binary.file_digest("md5", file_path)),
                ),
            )
            for file_path, artifact_path in zip(file_paths, artifact_paths)
        ]
        schema = DataSchema(
            arrowSchema=arrow.encode_schema(ds.schema),
        )
        request = DatasetCreateRequest(
            account=account,
            name=name,
            artifacts=artifacts,
            schema=schema,
        )
        return self.create(request)

    def upload_arrow_dataset(
        self, dataset: Dataset, dataset_directory: Path | str
    ) -> None:
        """Uploads the data files in an existing Arrow dataset for which a Dataset
        resource has already been created.

        Typical usage::

            dataset = client.datasets.create_arrow_dataset(dataset_directory, ...)
            client.datasets.upload_arrow_dataset(dataset, dataset_directory)

        :param dataset: The Dataset resource for the Arrow dataset.
        :type dataset: Dataset
        :param dataset_directory: The root directory of the Arrow dataset.
        :type dataset_directory: str
        """
        if any(artifact.digest.md5 is None for artifact in dataset.artifacts):
            raise ValueError("artifact.digest.md5 must be set for all artifacts")
        for artifact in dataset.artifacts:
            assert artifact.digest.md5 is not None
            file_path = Path(dataset_directory) / artifact.path
            put_url_json = _retry_not_found(self._raw_ops.upload)(
                dataset.id, artifact.path
            )
            put_url = StorageSignedURL.parse_obj(put_url_json)
            if put_url.method != "PUT":
                raise ValueError(f"expected a PUT URL; got {put_url.method}")
            with open(file_path, "rb") as fin:
                headers = {
                    "content-md5": artifact.digest.md5,
                }
                headers.update(put_url.headers)
                response = httpx.put(
                    put_url.url,
                    content=fin,
                    headers=headers,
                    verify=not self._insecure,
                )
                response.raise_for_status()
        _retry_not_found(self._raw_ops.finalize)(dataset.id)

    def downlinks(self, dataset_id: str) -> list[ArtifactURL]:
        """Get a list of signed GET URLs from which Dataset artifacts can be downloaded.

        :param dataset_id: The ID of the Dataset.
        :type dataset_id: str
        :return: List of signed GET URLs.
        :rtype: list[ArtifactURL] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return _downlinks(self._raw_ops, dataset_id)

    def download(self, dataset_id: str, destination: Path | str) -> None:
        """Download all of the files in a dataset to a local directory.

        The destination path must not exist. Parent directories will be
        created.

        :param dataset_id: The ID of the Dataset.
        :type dataset_id: str
        :param destination: The destination directory. Must exist and be empty.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``datasets.downlinks(dataset_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download(self, dataset_id, destination, insecure=self._insecure)

    def documentation(self, dataset_id: str) -> Documentation:
        """Get the documentation associated with a Dataset.

        Get the documentation associated with a Dataset. Raises a 404 error if no entity
        exists with that key.

        :param dataset_id: The ID of the Dataset.
        :type dataset_id: str
        :return: The documentation associated with the Dataset.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(self._raw_ops.documentation(dataset_id))

    def edit_documentation(
        self, dataset_id: str, edit_request: DocumentationEditRequest
    ) -> Documentation:
        """Edit the documentation associated with a Dataset.

        Edit the documentation associated with a Dataset. Raises a 404 error if no
        entity exists with that key. Returns the modified Documentation.

        :param dataset_id: The ID of the Dataset.
        :type dataset_id: str
        :param edit_request: Object containing the edits to make.
        :type edit_request: DocumentationEditRequest
        :return: The modified documentation.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(
            # exclude_unset: Users can explicitly set a field to None, but we
            # don't want to overwrite with None implicitly
            self._raw_ops.edit_documentation(
                dataset_id, edit_request.dict(exclude_unset=True)
            )
        )


class EvaluationsOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Evaluation` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.evaluations`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(
        self, _raw_ops: EvaluationsOperationsGenerated, *, insecure: bool = False
    ):
        self._raw_ops = _raw_ops
        self._insecure = insecure

    def get(self, evaluation_id: str) -> Evaluation:
        """Get an Evaluation by its key.

        :param evaluation_id: The evaluation id
        :type evaluation_id: str
        :return: The Evaluation with the given key.
        """
        return Evaluation.parse_obj(self._raw_ops.get(evaluation_id))

    def delete(self, evaluation_id: str) -> Status:
        """Mark an Evaluation for deletion.

        :param evaluation_id: The evaluation key
        :type evaluation_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(evaluation_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        dataset: Optional[str] = None,
        inferenceService: Optional[str] = None,
        inferenceServiceName: Optional[str] = None,
        model: Optional[str] = None,
        modelName: Optional[str] = None,
    ) -> list[Evaluation]:
        """Get all Evaluations matching a query. The query is a set of equality
        constraints specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword dataset:
        :paramtype dataset: str
        :keyword inferenceService:
        :paramtype inferenceService: str
        :keyword inferenceServiceName:
        :paramtype inferenceServiceName: str
        :keyword model:
        :paramtype model: str
        :keyword modelName:
        :paramtype modelName: str
        :return: list of ``Evaluation`` resources satisfying the query.
        :rtype: list[Evaluation]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Evaluation.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                dataset=dataset,
                inference_service=inferenceService,
                inference_service_name=inferenceServiceName,
                model=model,
                model_name=modelName,
            )
        ]

    def label(self, evaluation_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Evaluation with key-value pairs (stored in the
        ``.labels`` field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param evaluation_id: The ID of the Evaluation to label.
        :type evaluation_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(evaluation_id, labels)

    def create(
        self,
        request: SchemaObject[EvaluationCreateRequest],
    ) -> Evaluation:
        """Create an Evaluation.

        .. note::
            This operation will incur compute costs.

        :param request: The evaluation request specification.
        :type request: EvaluationCreateRequest | dict
        :return: A full Evaluation entity with .id and other properties set.
        """
        request = _parse_schema_object(EvaluationCreateRequest, request)
        evaluation = _retry_not_found(self._raw_ops.create)(request.dict())
        return Evaluation.parse_obj(evaluation)

    def downlinks(self, evaluation_id: str) -> list[ArtifactURL]:
        """Get a list of signed GET URLs from which Evaluation artifacts can be
        downloaded.

        :param evaluation_id: The ID of the Evaluation.
        :type evaluation_id: str
        :return: List of signed GET URLs.
        :rtype: list[ArtifactURL] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return _downlinks(self._raw_ops, evaluation_id)

    def download(self, evaluation_id: str, destination: Path | str) -> None:
        """Download all of the files in an evaluation to a local directory.

        The destination path must not exist. Parent directories will be
        created.

        :param evaluation_id: The ID of the Evaluation.
        :type evaluation_id: str
        :param destination: The destination directory. Must exist and be empty.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``evaluations.downlinks(evaluation_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download(self, evaluation_id, destination, insecure=self._insecure)


class InferenceservicesOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.InferenceService` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.inferenceservices`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(self, _raw_ops: InferenceservicesOperationsGenerated):
        self._raw_ops = _raw_ops

    def get(self, service_id: str) -> InferenceService:
        """Get an InferenceService by its key.

        :param service_id: The inference service id
        :type service_id: str
        :return: The InferenceService with the given key.
        """
        return InferenceService.parse_obj(self._raw_ops.get(service_id))

    def delete(self, service_id: str) -> Status:
        """Mark an InferenceService for deletion.

        :param service_id: The inference service key
        :type service_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(service_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        name: Optional[str] = None,
        model: Optional[str] = None,
        modelName: Optional[str] = None,
    ) -> list[InferenceService]:
        """Get all InferenceServices matching a query. The query is a set of equality
        constraints specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword name:
        :paramtype name: str
        :keyword model:
        :paramtype model: str
        :keyword modelName:
        :paramtype modelName: str
        :return: list of ``InferenceService`` resources satisfying the query.
        :rtype: list[InferenceService]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            InferenceService.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                name=name,
                model=model,
                model_name=modelName,
            )
        ]

    def label(self, service_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified InferenceService with key-value pairs (stored in the
        ``.labels`` field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param service_id: The ID of the InferenceService to label.
        :type service_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(service_id, labels)

    def create(
        self, request: SchemaObject[InferenceServiceCreateRequest]
    ) -> InferenceService:
        """Create an InferenceService.

        .. note::
            This operation may incur compute costs.

        :param request: The inference service request specification.
        :type request: InferenceServiceCreateRequest | dict
        :return: A full InferenceService entity with .id and other properties set.
        """
        request = _parse_schema_object(InferenceServiceCreateRequest, request)
        inferenceservice = _retry_not_found(self._raw_ops.create)(request.dict())
        return InferenceService.parse_obj(inferenceservice)

    def documentation(self, service_id: str) -> Documentation:
        """Get the documentation associated with an InferenceService.

        Get the documentation associated with a InferenceService. Raises a 404 error if
        no entity exists with that key.

        :param service_id: The ID of the InferenceService.
        :type service_id: str
        :return: The documentation associated with the InferenceService.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(self._raw_ops.documentation(service_id))

    def edit_documentation(
        self, service_id: str, edit_request: DocumentationEditRequest
    ) -> Documentation:
        """Edit the documentation associated with an InferenceService.

        Edit the documentation associated with an InferenceService. Raises a 404 error
        if no entity exists with that key. Returns the modified Documentation.

        :param service_id: The ID of the InferenceService.
        :type service_id: str
        :param edit_request: Object containing the edits to make.
        :type edit_request: DocumentationEditRequest
        :return: The modified documentation.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(
            # exclude_unset: Users can explicitly set a field to None, but we
            # don't want to overwrite with None implicitly
            self._raw_ops.edit_documentation(
                service_id, edit_request.dict(exclude_unset=True)
            )
        )


class InferencesessionsOperations:
    """Operations on :class:`~dyff.schema.platform.Inferencesession` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.inferencesessions`` attribute of :class:`~dyff.client.Client`.

      `verify_ssl_certifcates` is deprecated, use `insecure` instead.
    """

    def __init__(
        self,
        _raw_ops: InferencesessionsOperationsGenerated,
        *,
        verify_ssl_certificates: bool = True,
        insecure: bool = False,
    ):
        self._raw_ops = _raw_ops

        # verify_ssl_certificates deprecated
        # remove after 10/2024
        insecure = _check_deprecated_verify_ssl_certificates(
            verify_ssl_certificates, insecure
        )

        self._verify_ssl_certificates = not insecure
        self._insecure = insecure

    def get(self, session_id: str) -> InferenceSession:
        """Get an InferenceSession by its key.

        :param session_id: The inference session id
        :type session_id: str
        :return: The InferenceSession with the given key.
        """
        return InferenceSession.parse_obj(self._raw_ops.get(session_id))

    def delete(self, session_id: str) -> Status:
        """Mark an InferenceSession for deletion.

        :param session_id: The inference session key
        :type session_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(session_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        name: Optional[str] = None,
        inferenceService: Optional[str] = None,
        inferenceServiceName: Optional[str] = None,
        model: Optional[str] = None,
        modelName: Optional[str] = None,
    ) -> list[InferenceSession]:
        """Get all InferenceSessions matching a query. The query is a set of equality
        constraints specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword name:
        :paramtype name: str
        :keyword model:
        :paramtype model: str
        :keyword modelName:
        :paramtype modelName: str
        :return: list of ``InferenceSession`` resources satisfying the query.
        :rtype: list[InferenceSession]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            InferenceSession.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                name=name,
                inference_service=inferenceService,
                inference_service_name=inferenceServiceName,
                model=model,
                model_name=modelName,
            )
        ]

    def label(self, session_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified InferenceSession with key-value pairs (stored in the
        ``.labels`` field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param session_id: The ID of the InferenceSession to label.
        :type session_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(session_id, labels)

    def create(
        self, request: SchemaObject[InferenceSessionCreateRequest]
    ) -> InferenceSessionAndToken:
        """Create an InferenceSession.

        .. note::
            This operation will incur compute costs.

        :param request: The inference session request specification.
        :type request: InferenceSessionCreateRequest | dict
        :return: A full InferenceSession entity with .id and other properties set.
        """
        request = _parse_schema_object(InferenceSessionCreateRequest, request)
        session_and_token = _retry_not_found(self._raw_ops.create)(request.dict())
        return InferenceSessionAndToken.parse_obj(session_and_token)

    def client(
        self,
        session_id: str,
        token: str,
        *,
        interface: Optional[InferenceInterface] = None,
        endpoint: Optional[str] = None,
        input_adapter: Optional[Adapter] = None,
        output_adapter: Optional[Adapter] = None,
    ) -> InferenceSessionClient:
        """Create an InferenceSessionClient that interacts with the given inference
        session. The token should be one returned either from
        ``Client.inferencesessions.create()`` or from
        ``Client.inferencesessions.token(session_id)``.

        The inference endpoint in the session must also be specified, either
        directly through the ``endpoint`` argument or by specifying an
        ``interface``. Specifying ``interface`` will also use the input and
        output adapters from the interface. You can also specify these
        separately in the ``input_adapter`` and ``output_adapter``. The
        non-``interface`` arguments override the corresponding values in
        ``interface`` if both are specified.

        :param session_id: The inference session to connect to
        :type session_id: str
        :param token: An access token with permission to run inference against
            the session.
        :type token: str
        :param interface: The interface to the session. Either ``interface``
            or ``endpoint`` must be specified.
        :type interface: Optional[InferenceInterface]
        :param endpoint: The inference endpoint in the session to call. Either
            ``endpoint`` or ``interface`` must be specified.
        :type endpoint: str
        :param input_adapter: Optional input adapter, applied to the input
            before sending it to the session. Will override the input adapter
            from ``interface`` if both are specified.
        :type input_adapter: Optional[Adapter]
        :param output_adapter: Optional output adapter, applied to the output
            of the session before returning to the client. Will override the
            output adapter from ``interface`` if both are specified.
        :type output_adapter: Optional[Adapter]
        :return: An ``InferenceSessionClient`` that makes inference calls to
            the specified session.
        """
        if interface is not None:
            endpoint = endpoint or interface.endpoint
            if input_adapter is None:
                if interface.inputPipeline is not None:
                    input_adapter = create_pipeline(interface.inputPipeline)
            if output_adapter is None:
                if interface.outputPipeline is not None:
                    output_adapter = create_pipeline(interface.outputPipeline)
        if endpoint is None:
            raise ValueError("either 'endpoint' or 'interface' is required")
        return InferenceSessionClient(
            session_id=session_id,
            token=token,
            dyff_api_endpoint=self._raw_ops._client._base_url,
            inference_endpoint=endpoint,
            input_adapter=input_adapter,
            output_adapter=output_adapter,
            insecure=self._insecure,
        )

    def ready(self, session_id: str) -> bool:
        """Return True if the session is ready to receive inference input.

        The readiness probe is expected to fail with status codes 404 or 503,
        as these will occur at times during normal session start-up. The
        ``ready()`` method returns False in these cases. Any other status
        codes will raise an ``HttpResponseError``.

        :param str session_id: The ID of the session.
        :raises HttpResponseError:
        """
        try:
            self._raw_ops.ready(session_id)
        except HttpResponseError as ex:
            if ex.status_code in [404, 503]:
                return False
            else:
                raise
        return True

    def terminate(self, session_id: str) -> Status:
        """Terminate a session.

        :param session_id: The inference session key
        :type session_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        :raises HttpResponseError:
        """
        return Status.parse_obj(self._raw_ops.terminate(session_id))

    def token(self, session_id: str, *, expires: Optional[datetime] = None) -> str:
        """Create a session token.

        The session token is a short-lived token that allows the bearer to
        make inferences with the session (via an ``InferenceSessionClient``)
        and to call ``ready()``, ``get()``, and ``terminate()`` on the session.

        :param str session_id: The ID of the session.
        :keyword Optional[datetime] expires: The expiration time of the token.
            Must be < the expiration time of the session. Default: expiration
            time of the session.
        :raises HttpResponseError:
        """
        request = InferenceSessionTokenCreateRequest(expires=expires)
        return str(self._raw_ops.token(session_id, request.dict()))


class MeasurementsOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Measurement` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.measurements`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(
        self, _raw_ops: MeasurementsOperationsGenerated, *, insecure: bool = False
    ):
        self._raw_ops = _raw_ops
        self._insecure = insecure

    def get(self, measurement_id: str) -> Measurement:
        """Get a Measurement by its key.

        :param measurement_id: The Measurement ID
        :type measurement_id: str
        :return: The Measurement with the given ID.
        """
        return Measurement.parse_obj(self._raw_ops.get(measurement_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        method: Optional[str] = None,
        methodName: Optional[str] = None,
        dataset: Optional[str] = None,
        evaluation: Optional[str] = None,
        inferenceService: Optional[str] = None,
        model: Optional[str] = None,
        inputs: Optional[list[str]] = None,
    ) -> list[Measurement]:
        """Get all Measurement entities matching a query. The query is a set of equality
        constraints specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id: Default value is None.
        :paramtype id: str
        :keyword account: Default value is None.
        :paramtype account: str
        :keyword status: Default value is None.
        :paramtype status: str
        :keyword reason: Default value is None.
        :paramtype reason: str
        :keyword labels: Default value is None.
        :paramtype labels: str
        :keyword method: Default value is None.
        :paramtype method: str
        :keyword methodName: Default value is None.
        :paramtype methodName: str
        :keyword dataset: Default value is None.
        :paramtype dataset: str
        :keyword evaluation: Default value is None.
        :paramtype evaluation: str
        :keyword inferenceService: Default value is None.
        :paramtype inferenceService: str
        :keyword model: Default value is None.
        :paramtype model: str
        :keyword inputs: Default value is None.
        :paramtype inputs: str
        :return: Entities matching the query
        :rtype: list[Measurement]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Measurement.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                method=method,
                method_name=methodName,
                dataset=dataset,
                evaluation=evaluation,
                inference_service=inferenceService,
                model=model,
                inputs=(",".join(inputs) if inputs is not None else None),
            )
        ]

    def label(self, measurement_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Measurement with key-value pairs (stored in the
        ``.labels`` field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param measurement_id: The ID of the Measurement to label.
        :type measurement_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(measurement_id, labels)

    def create(self, request: SchemaObject[AnalysisCreateRequest]) -> Measurement:
        """Create a Measurement.

        :param request: The measurement request specification.
        :type request: AnalysisCreateRequest | dict
        :return: A full Meausrement entity with .id and other properties set.
        """
        request = _parse_schema_object(AnalysisCreateRequest, request)
        measurement = _retry_not_found(self._raw_ops.create)(request.dict())
        return Measurement.parse_obj(measurement)

    def downlinks(self, measurement_id: str) -> list[ArtifactURL]:
        """Get a list of signed GET URLs from which Measurement artifacts can be
        downloaded.

        :param measurement_id: The ID of the Measurement.
        :type measurement_id: str
        :return: List of signed GET URLs.
        :rtype: list[ArtifactURL] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return _downlinks(self._raw_ops, measurement_id)

    def download(self, measurement_id: str, destination: Path | str) -> None:
        """Download all of the files in a measurement to a local directory.

        The destination path must not exist. Parent directories will be
        created.

        :param measurement_id: The ID of the Measurement.
        :type measurement_id: str
        :param destination: The destination directory. Must exist and be empty.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``measurements.downlinks(measurement_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download(self, measurement_id, destination, insecure=self._insecure)

    def logs(self, measurement_id) -> Iterable[str]:
        """Stream the logs from the measurement as a sequence of lines.

        :param measurement_id: The ID of the Measurement.
        :type measurement_id: str
        :return: An Iterable over the lines in the logs file. The response is
            streamed, and may time out if it is not consumed quickly enough.
        :rtype: Iterable[str]
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``raw.measurements.logs(measurement_id)`` raises, or if the
            streaming response times out or encounters some other error.
        :raises ValueError: If arguments are invalid
        """
        return _stream_logs(self._raw_ops, measurement_id, insecure=self._insecure)

    def download_logs(self, measurement_id, destination: Path | str) -> None:
        """Download the logs file from the measurement.

        The destination path must not exist. Parent directories will be
        created.

        :param measurement_id: The ID of the Measurement.
        :type measurement_id: str
        :param destination: The destination file. Must not exist, and its
            parent directory must exist.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``raw.measurements.logs(measurement_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download_logs(
            self._raw_ops, measurement_id, destination, insecure=self._insecure
        )


class MethodsOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Method` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.analyses`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(self, _raw_ops: MethodsOperationsGenerated):
        self._raw_ops = _raw_ops

    def get(self, analysis_id: str) -> Method:
        """Get an Method by its key.

        :param analysis_id: The Method id
        :type analysis_id: str
        :return: The Method with the given ID.
        """
        return Method.parse_obj(self._raw_ops.get(analysis_id))

    def delete(self, analysis_id: str) -> Status:
        """Mark an Method for deletion.

        :param analysis_id: The analysis id
        :type analysis_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(analysis_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        name: Optional[str] = None,
        output_kind: Optional[str] = None,
    ) -> list[Method]:
        """Get all Method entities matching a query. The query is a set of equality
        constraints specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]] :keyword id:
            Default value is None.
        :paramtype id: str :keyword account: Default value is None.
        :paramtype account: str :keyword status: Default value is None.
        :paramtype status: str :keyword reason: Default value is None.
        :paramtype reason: str :keyword labels: Default value is None.
        :paramtype labels: dict[str, str] :keyword name: Default value is None.
        :paramtype name: str :keyword output_kind: Default value is None.
        :paramtype output_kind: str
        :return: list of Method entities matching query
        :rtype: list[Method] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Method.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                name=name,
                output_kind=output_kind,
            )
        ]

    def label(self, analysis_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Method with key-value pairs (stored in the ``.labels``
        field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param analysis_id: The ID of the Method to label.
        :type analysis_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(analysis_id, labels)

    def create(self, request: SchemaObject[MethodCreateRequest]) -> Method:
        """Create an Method.

        :param request: The method request specification.
        :type request: MethodCreateRequest | dict
        :return: A full Method entity with .id and other properties set.
        """
        request = _parse_schema_object(MethodCreateRequest, request)
        method = _retry_not_found(self._raw_ops.create)(request.dict())
        return Method.parse_obj(method)

    def documentation(self, method_id: str) -> Documentation:
        """Get the documentation associated with a Method.

        Get the documentation associated with a Method. Raises a 404 error if no entity
        exists with that key.

        :param method_id: The ID of the Method.
        :type method_id: str
        :return: The documentation associated with the Method.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(self._raw_ops.documentation(method_id))

    def edit_documentation(
        self, method_id: str, edit_request: DocumentationEditRequest
    ) -> Documentation:
        """Edit the documentation associated with a Method.

        Edit the documentation associated with a Method. Raises a 404 error if no entity
        exists with that key. Returns the modified Documentation.

        :param method_id: The ID of the Method.
        :type method_id: str
        :param edit_request: Object containing the edits to make.
        :type edit_request: DocumentationEditRequest
        :return: The modified documentation.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(
            # exclude_unset: Users can explicitly set a field to None, but we
            # don't want to overwrite with None implicitly
            self._raw_ops.edit_documentation(
                method_id, edit_request.dict(exclude_unset=True)
            )
        )


class ModelsOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Model` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.models`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(self, _raw_ops: ModelsOperationsGenerated):
        self._raw_ops = _raw_ops

    def get(self, model_id: str) -> Model:
        """Get a Model by its key.

        :param model_id: The inference service id
        :type model_id: str
        :return: The Model with the given key.
        """
        return Model.parse_obj(self._raw_ops.get(model_id))

    def delete(self, model_id: str) -> Status:
        """Mark a Model for deletion.

        :param model_id: The model key
        :type model_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(model_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        name: Optional[str] = None,
    ) -> list[Model]:
        """Get all Models matching a query. The query is a set of equality constraints
        specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword name:
        :paramtype name: str
        :return: list of ``Model`` resources satisfying the query.
        :rtype: list[Model]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Model.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                name=name,
            )
        ]

    def label(self, model_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Model with key-value pairs (stored in the ``.labels``
        field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param model_id: The ID of the Model to label.
        :type model_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(model_id, labels)

    def create(self, request: SchemaObject[ModelCreateRequest]) -> Model:
        """Create a Model.

        .. note::
            This operation will incur compute costs.

        :param request: The model request specification.
        :type request: ModelCreateRequest | dict
        :return: A full Model entity with .id and other properties set.
        """
        request = _parse_schema_object(ModelCreateRequest, request)
        model = _retry_not_found(self._raw_ops.create)(request.dict())
        return Model.parse_obj(model)

    def documentation(self, model_id: str) -> Documentation:
        """Get the documentation associated with a Model.

        Get the documentation associated with a Model. Raises a 404 error if no entity
        exists with that key.

        :param model_id: The ID of the Model.
        :type model_id: str
        :return: The documentation associated with the Model.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(self._raw_ops.documentation(model_id))

    def edit_documentation(
        self, model_id: str, edit_request: DocumentationEditRequest
    ) -> Documentation:
        """Edit the documentation associated with a Model.

        Edit the documentation associated with a Method. Raises a 404 error if no entity
        exists with that key. Returns the modified Documentation.

        :param model_id: The ID of the Model.
        :type model_id: str
        :param edit_request: Object containing the edits to make.
        :type edit_request: DocumentationEditRequest
        :return: The modified documentation.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(
            # exclude_unset: Users can explicitly set a field to None, but we
            # don't want to overwrite with None implicitly
            self._raw_ops.edit_documentation(
                model_id, edit_request.dict(exclude_unset=True)
            )
        )


class ModulesOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Module` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.modules`` attribute of :class:`~dyff.client.Client`.

      `verify_ssl_certifcates` is deprecated, use `insecure` instead.
    """

    def __init__(
        self,
        _raw_ops: ModulesOperationsGenerated,
        *,
        verify_ssl_certificates: bool = True,
        insecure: bool = False,
    ):
        self._raw_ops = _raw_ops

        # verify_ssl_certificates deprecated
        # remove after 10/2024
        insecure = _check_deprecated_verify_ssl_certificates(
            verify_ssl_certificates, insecure
        )

        self._verify_ssl_certificates = not insecure
        self._insecure = insecure

    def get(self, module_id: str) -> Module:
        """Get a Module by its key.

        :param module_id: The dataset key
        :type module_id: str
        :return: The Module with the given key.
        """
        return Module.parse_obj(self._raw_ops.get(module_id))

    def delete(self, module_id: str) -> Status:
        """Mark a Module for deletion.

        :param module_id: The dataset key
        :type module_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(module_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        name: Optional[str] = None,
    ) -> list[Module]:
        """Get all Modules matching a query. The query is a set of equality constraints
        specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword name: Default value is None.
        :paramtype name: str
        :return: list of ``Module`` resources satisfying the query.
        :rtype: list[Module]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Module.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                name=name,
            )
        ]

    def label(self, module_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Module with key-value pairs (stored in the ``.labels``
        field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param module_id: The ID of the Module to label.
        :type module_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(module_id, labels)

    def create(self, request: SchemaObject[ModuleCreateRequest]) -> Module:
        """Create a Module.

        .. note::
            This operation may incur compute costs.

        :param request: The module request specification.
        :type request: ModuleCreateRequest | dict
        :return: A full Module entity with .id and other properties set.
        """
        request = _parse_schema_object(ModuleCreateRequest, request)
        module = _retry_not_found(self._raw_ops.create)(request.dict())
        return Module.parse_obj(module)

    def create_package(
        self, package_directory: Path | str, *, account: str, name: str
    ) -> Module:
        """Create a Module resource describing a package structured as a directory tree.

        Internally, constructs a ``ModuleCreateRequest`` using information
        obtained from the directory tree, then calls ``create()`` with the
        constructed request.

        Typical usage::

            module = client.modules.create_package(package_directory, ...)
            client.modules.upload_package(module, package_directory)

        :param package_directory: The root directory of the package.
        :type package_directory: str
        :keyword account: The account that will own the Module resource.
        :type account: str
        :keyword name: The name of the Module resource.
        :type name: str
        :returns: The complete Module resource.
        :rtype: Module
        """
        package_root = Path(package_directory)
        file_paths = [path for path in package_root.rglob("*") if path.is_file()]
        if not file_paths:
            raise ValueError(f"package_directory is empty: {package_directory}")
        artifact_paths = [
            str(Path(file_path).relative_to(package_root)) for file_path in file_paths
        ]
        artifacts = [
            Artifact(
                # FIXME: Is this a useful thing to do? It's redundant with
                # information in 'path'. Maybe it should just be 'code' or
                # something generic.
                kind="".join(file_path.suffixes),
                path=artifact_path,
                digest=Digest(
                    md5=binary.encode(binary.file_digest("md5", str(file_path))),
                ),
            )
            for file_path, artifact_path in zip(file_paths, artifact_paths)
        ]
        request = ModuleCreateRequest(
            account=account,
            name=name,
            artifacts=artifacts,
        )
        return self.create(request)

    def upload_package(self, module: Module, package_directory: Path | str) -> None:
        """Uploads the files in a package directory for which a Module resource has
        already been created.

        Typical usage::

            module = client.modules.create_package(package_directory, ...)
            client.modules.upload_package(module, package_directory)

        :param module: The Module resource for the package.
        :type module: Module
        :param package_directory: The root directory of the package.
        :type package_directory: str
        """
        if any(artifact.digest.md5 is None for artifact in module.artifacts):
            raise ValueError("artifact.digest.md5 must be set for all artifacts")
        for artifact in module.artifacts:
            assert artifact.digest.md5 is not None
            file_path = Path(package_directory) / artifact.path
            put_url_json = _retry_not_found(self._raw_ops.upload)(
                module.id, artifact.path
            )
            put_url = StorageSignedURL.parse_obj(put_url_json)
            if put_url.method != "PUT":
                raise ValueError(f"expected a PUT URL; got {put_url.method}")
            with open(file_path, "rb") as fin:
                headers = {
                    "content-md5": artifact.digest.md5,
                }
                headers.update(put_url.headers)
                response = httpx.put(
                    put_url.url,
                    content=fin,
                    headers=headers,
                    verify=not self._insecure,
                )
                response.raise_for_status()
        _retry_not_found(self._raw_ops.finalize)(module.id)

    def downlinks(self, module_id: str) -> list[ArtifactURL]:
        """Get a list of signed GET URLs from which Module artifacts can be downloaded.

        :param measurement_id: The ID of the Module.
        :type measurement_id: str
        :return: List of signed GET URLs.
        :rtype: list[ArtifactURL] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return _downlinks(self._raw_ops, module_id)

    def download(self, module_id: str, destination: Path | str) -> None:
        """Download all of the files in a module to a local directory.

        The destination path must not exist. Parent directories will be
        created.

        :param module_id: The ID of the Module.
        :type module_id: str
        :param destination: The destination directory. Must exist and be empty.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``modules.downlinks(module_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download(self, module_id, destination, insecure=self._insecure)

    def documentation(self, module_id: str) -> Documentation:
        """Get the documentation associated with a Module.

        Get the documentation associated with a Module. Raises a 404 error if no entity
        exists with that key.

        :param module_id: The ID of the Module.
        :type module_id: str
        :return: The documentation associated with the Module.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(self._raw_ops.documentation(module_id))

    def edit_documentation(
        self, module_id: str, edit_request: DocumentationEditRequest
    ) -> Documentation:
        """Edit the documentation associated with a Module.

        Edit the documentation associated with a Method. Raises a 404 error if no entity
        exists with that key. Returns the modified Documentation.

        :param module_id: The ID of the Module.
        :type module_id: str
        :param edit_request: Object containing the edits to make.
        :type edit_request: DocumentationEditRequest
        :return: The modified documentation.
        :rtype: Documentation :raises ~azure.core.exceptions.HttpResponseError:
        """
        return Documentation.parse_obj(
            # exclude_unset: Users can explicitly set a field to None, but we
            # don't want to overwrite with None implicitly
            self._raw_ops.edit_documentation(
                module_id, edit_request.dict(exclude_unset=True)
            )
        )


class ReportsOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.Report` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.reports`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(self, _raw_ops: ReportsOperationsGenerated, *, insecure: bool = False):
        self._raw_ops = _raw_ops
        self._insecure = insecure

    def get(self, report_id: str) -> Report:
        """Get a Report by its key.

        :param report_id: The report id
        :type report_id: str
        :return: The Report with the given key.
        """
        return Report.parse_obj(self._raw_ops.get(report_id))

    def delete(self, report_id: str) -> Status:
        """Mark a Report for deletion.

        :param report_id: The report key
        :type report_id: str
        :return: The resulting status of the entity
        :rtype: dyff.schema.platform.Status
        """
        return Status.parse_obj(self._raw_ops.delete(report_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        report: Optional[str] = None,
        dataset: Optional[str] = None,
        evaluation: Optional[str] = None,
        inferenceService: Optional[str] = None,
        model: Optional[str] = None,
    ) -> list[Report]:
        """Get all Reports matching a query. The query is a set of equality constraints
        specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id:
        :paramtype id: str
        :keyword account:
        :paramtype account: str
        :keyword status:
        :paramtype status: str
        :keyword reason:
        :paramtype reason: str
        :keyword labels:
        :paramtype labels: dict[str, str]
        :keyword report:
        :paramtype report: str
        :keyword dataset:
        :paramtype dataset: str
        :keyword evaluation:
        :paramtype evaluation: str
        :keyword inferenceService:
        :paramtype inferenceService: str
        :keyword model:
        :paramtype model: str
        :return: list of ``Report`` resources satisfying the query.
        :rtype: list[Report]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            Report.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                report=report,
                dataset=dataset,
                evaluation=evaluation,
                inference_service=inferenceService,
                model=model,
            )
        ]

    def label(self, report_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified Report with key-value pairs (stored in the ``.labels``
        field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param report_id: The ID of the Report to label.
        :type report_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(report_id, labels)

    def create(self, request: SchemaObject[ReportCreateRequest]) -> Report:
        """Create a Report.

        .. note::
            This operation will incur compute costs.

        :param request: The report request specification.
        :type request: ReportCreateRequest | dict
        :return: A full Report entity with .id and other properties set.
        """
        request = _parse_schema_object(ReportCreateRequest, request)
        report = _retry_not_found(self._raw_ops.create)(request.dict())
        return Report.parse_obj(report)

    def downlinks(self, report_id: str) -> list[ArtifactURL]:
        """Get a list of signed GET URLs from which Report artifacts can be downloaded.

        :param report_id: The ID of the Report.
        :type report_id: str
        :return: List of signed GET URLs.
        :rtype: list[ArtifactURL] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return _downlinks(self._raw_ops, report_id)

    def download(self, report_id: str, destination: Path | str) -> None:
        """Download all of the files in a report to a local directory.

        The destination path must not exist. Parent directories will be
        created.

        :param report_id: The ID of the Report.
        :type report_id: str
        :param destination: The destination directory. Must exist and be empty.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``reports.downlinks(report_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download(self, report_id, destination, insecure=self._insecure)

    def logs(self, report_id) -> Iterable[str]:
        """Stream the logs from the report as a sequence of lines.

        :param report_id: The ID of the Report.
        :type report_id: str
        :return: An Iterable over the lines in the logs file. The response is
            streamed, and may time out if it is not consumed quickly enough.
        :rtype: Iterable[str]
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``raw.reports.logs(report_id)`` raises, or if the
            streaming response times out or encounters some other error.
        :raises ValueError: If arguments are invalid
        """
        return _stream_logs(self._raw_ops, report_id, insecure=self._insecure)

    def download_logs(self, report_id, destination: Path | str) -> None:
        """Download the logs file from the report.

        The destination path must not exist. Parent directories will be
        created.

        :param report_id: The ID of the Report.
        :type report_id: str
        :param destination: The destination file. Must not exist, and its
            parent directory must exist.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``raw.reports.logs(report_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download_logs(
            self._raw_ops, report_id, destination, insecure=self._insecure
        )


class SafetycasesOperations(_PublishMixin):
    """Operations on :class:`~dyff.schema.platform.SafetyCase` entities.

    .. note::

      Do not instantiate this class. Access it through the
      ``.safetycases`` attribute of :class:`~dyff.client.Client`.
    """

    def __init__(
        self, _raw_ops: SafetycasesOperationsGenerated, *, insecure: bool = False
    ):
        self._raw_ops = _raw_ops
        self._insecure = insecure

    def get(self, safetycase_id: str) -> SafetyCase:
        """Get a SafetyCase by its key.

        :param safetycase_id: The SafetyCase ID
        :type safetycase_id: str
        :return: The SafetyCase with the given ID.
        """
        return SafetyCase.parse_obj(self._raw_ops.get(safetycase_id))

    def query(
        self,
        *,
        query: Optional[QueryT] = None,
        id: Optional[str] = None,
        account: Optional[str] = None,
        status: Optional[str] = None,
        reason: Optional[str] = None,
        labels: Optional[dict[str, str]] = None,
        method: Optional[str] = None,
        methodName: Optional[str] = None,
        dataset: Optional[str] = None,
        evaluation: Optional[str] = None,
        inferenceService: Optional[str] = None,
        model: Optional[str] = None,
        inputs: Optional[str] = None,
    ) -> list[SafetyCase]:
        """Get all SafetyCase entities matching a query. The query is a set of equality
        constraints specified as key-value pairs.

        :keyword query:
        :paramtype query: str | dict[str, Any] | list[dict[str, Any]]
        :keyword id: Default value is None.
        :paramtype id: str
        :keyword account: Default value is None.
        :paramtype account: str
        :keyword status: Default value is None.
        :paramtype status: str
        :keyword reason: Default value is None.
        :paramtype reason: str
        :keyword labels: Default value is None.
        :paramtype labels: str
        :keyword method: Default value is None.
        :paramtype method: str
        :keyword methodName: Default value is None.
        :paramtype methodName: str
        :keyword dataset: Default value is None.
        :paramtype dataset: str
        :keyword evaluation: Default value is None.
        :paramtype evaluation: str
        :keyword inferenceService: Default value is None.
        :paramtype inferenceService: str
        :keyword model: Default value is None.
        :paramtype model: str
        :keyword inputs: Default value is None.
        :paramtype inputs: str
        :return: Entities matching the query
        :rtype: list[SafetyCase]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return [
            SafetyCase.parse_obj(obj)
            for obj in self._raw_ops.query(
                query=_encode_query(query),
                id=id,
                account=account,
                status=status,
                reason=reason,
                labels=_encode_labels(labels),
                method=method,
                method_name=methodName,
                dataset=dataset,
                evaluation=evaluation,
                inference_service=inferenceService,
                model=model,
                inputs=(",".join(inputs) if inputs is not None else None),
            )
        ]

    def label(self, safetycase_id: str, labels: dict[str, Optional[str]]) -> None:
        """Label the specified SafetyCase with key-value pairs (stored in the
        ``.labels`` field of the resource).

        Providing ``None`` for the value deletes the label.

        See :class:`~dyff.schema.platform.Label` for a description of the
        constraints on label keys and values.

        :param safetycase_id: The ID of the SafetyCase to label.
        :type safetycase_id: str
        :param labels: The label keys and values.
        :type labels: dict[str, Optional[str]]
        """
        if not labels:
            return
        labels = LabelUpdateRequest(labels=labels).dict()
        self._raw_ops.label(safetycase_id, labels)

    def create(self, request: SchemaObject[AnalysisCreateRequest]) -> SafetyCase:
        """Create a SafetyCase.

        :param request: The safety case request specification.
        :type request: AnalysisCreateRequest | dict
        :return: A full SafetyCase entity with .id and other properties set.
        """
        request = _parse_schema_object(AnalysisCreateRequest, request)
        safetycase = _retry_not_found(self._raw_ops.create)(request.dict())
        return SafetyCase.parse_obj(safetycase)

    def downlinks(self, safetycase_id: str) -> list[ArtifactURL]:
        """Get a list of signed GET URLs from which SafetyCase artifacts can be
        downloaded.

        :param safetycase_id: The ID of the SafetyCase.
        :type safetycase_id: str
        :return: List of signed GET URLs.
        :rtype: list[ArtifactURL] :raises ~azure.core.exceptions.HttpResponseError:
        """
        return _downlinks(self._raw_ops, safetycase_id)

    def download(self, safetycase_id: str, destination: Path | str) -> None:
        """Download all of the files in a safety case to a local directory.

        The destination path must not exist. Parent directories will be
        created.

        :param safetycase_id: The ID of the SafetyCase.
        :type safetycase_id: str
        :param destination: The destination directory. Must exist and be empty.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``safetycases.downlinks(safetycase_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download(self, safetycase_id, destination, insecure=self._insecure)

    def logs(self, safetycase_id: str) -> Iterable[str]:
        """Stream the logs from the safety case as a sequence of lines.

        :param safetycase_id: The ID of the SafetyCase.
        :type safetycase_id: str
        :return: An Iterable over the lines in the logs file. The response is
            streamed, and may time out if it is not consumed quickly enough.
        :rtype: Iterable[str]
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``raw.safetycases.logs(safetycase_id)`` raises, or if the
            streaming response times out or encounters some other error.
        :raises ValueError: If arguments are invalid
        """
        return _stream_logs(self._raw_ops, safetycase_id, insecure=self._insecure)

    def download_logs(self, safetycase_id: str, destination: Path | str) -> None:
        """Download the logs file from the safety case.

        The destination path must not exist. Parent directories will be
        created.

        :param safetycase_id: The ID of the SafetyCase.
        :type safetycase_id: str
        :param destination: The destination file. Must not exist, and its
            parent directory must exist.
        :type destination: Path | str
        :raises ~azure.core.exceptions.HttpResponseError: If
            ``raw.safetycases.logs(safetycase_id)`` raises
        :raises ValueError: If arguments are invalid
        """
        return _download_logs(
            self._raw_ops, safetycase_id, destination, insecure=self._insecure
        )


class _APIKeyCredential(TokenCredential):
    def __init__(self, *, api_key: str):
        self.api_key = api_key

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        **kwargs: Any,
    ) -> AccessToken:
        return AccessToken(self.api_key, -1)


class Client:
    """The Python client for the Dyff Platform API.

    API operations are grouped by the resource type that they manipulate. For
    example, all operations on ``Evaluation`` resources are accessed like
    ``client.evaluations.create()``.

    The Python API functions may have somewhat different behavior from the
    corresponding API endpoints, and the Python client also adds several
    higher-level API functions that are implemented with multiple endpoint
    calls.
    """

    def __init__(
        self,
        *,
        api_key: str,
        endpoint: Optional[str] = None,
        verify_ssl_certificates: bool = True,
        insecure: bool = False,
    ):
        """
        :param str api_key: An API token to use for authentication.
        :param str endpoint: The URL where the Dyff Platform API is hosted.
            Defaults to the UL DSRI-hosted Dyff instance.
        :param bool verify_ssl_certificates: You can disable certificate
            verification for testing; you should do this only if you have
            also changed ``endpoint`` to point to a trusted local server.

            .. deprecated:: 0.2.2
                Use insecure instead
        :param bool insecure: Disable certificate verification for testing.
            you should do this only if you have
            also changed ``endpoint`` to point to a trusted local server.
        """
        if not verify_ssl_certificates:
            warn("verify_ssl_certificates is deprecated", DeprecationWarning)
        # verify_ssl_certificates deprecated
        # remove after 10/2024
        insecure = _check_deprecated_verify_ssl_certificates(
            verify_ssl_certificates, insecure
        )

        if endpoint is None:
            endpoint = "https://api.dyff.io/v0"
        credential = _APIKeyCredential(api_key=api_key)
        authentication_policy = BearerTokenCredentialPolicy(credential)
        self._raw = RawClient(
            endpoint=endpoint,
            credential=credential,
            authentication_policy=authentication_policy,
        )

        # We want the ability to disable SSL certificate verification for testing
        # on localhost. It should be possible to do this via the Configuration object:
        # e.g., config.<some_field> = azure.core.configuration.ConnectionConfiguration(connection_verify=False)
        #
        # The docs state that the ConnectionConfiguration class is "Found in the Configuration object."
        # https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.configuration.connectionconfiguration?view=azure-python
        #
        # But at no point do they say what the name of the field should be! The
        # docs for azure.core.configuration.Configuration don't mention any
        # connection configuration. The field is called 'connection_config' in the
        # _transport member of _pipeline, but _transport will not pick up the
        # altered ConnectionConfiguration if it is set on 'config.connection_config'
        #
        # Example:
        # client._config.connection_config = ConnectionConfiguration(connection_verify=False)
        # [in Client:]
        # >>> print(self._config.connection_config.verify)
        # False
        # >> print(self._pipeline._transport.connection_config.verify)
        # True
        self._raw._client._pipeline._transport.connection_config.verify = (  # type: ignore
            not insecure
        )

        self._datasets = DatasetsOperations(self._raw.datasets, insecure=insecure)
        self._evaluations = EvaluationsOperations(
            self._raw.evaluations, insecure=insecure
        )
        self._inferenceservices = InferenceservicesOperations(
            self._raw.inferenceservices
        )
        self._inferencesessions = InferencesessionsOperations(
            self._raw.inferencesessions,
            insecure=insecure,
        )
        self._measurements = MeasurementsOperations(
            self._raw.measurements, insecure=insecure
        )
        self._methods = MethodsOperations(self._raw.methods)
        self._models = ModelsOperations(self._raw.models)
        self._modules = ModulesOperations(
            self._raw.modules,
            insecure=insecure,
        )
        self._reports = ReportsOperations(self._raw.reports, insecure=insecure)
        self._safetycases = SafetycasesOperations(
            self._raw.safetycases, insecure=insecure
        )

    @property
    def raw(self) -> RawClient:
        """The "raw" API client, which can be used to send JSON requests directly."""
        return self._raw

    @property
    def datasets(self) -> DatasetsOperations:
        """Operations on :class:`~dyff.schema.platform.Dataset` entities."""
        return self._datasets

    @property
    def evaluations(self) -> EvaluationsOperations:
        """Operations on :class:`~dyff.schema.platform.Evaluation` entities."""
        return self._evaluations

    @property
    def inferenceservices(self) -> InferenceservicesOperations:
        """Operations on :class:`~dyff.schema.platform.InferenceService` entities."""
        return self._inferenceservices

    @property
    def inferencesessions(self) -> InferencesessionsOperations:
        """Operations on :class:`~dyff.schema.platform.InferenceSession` entities."""
        return self._inferencesessions

    @property
    def methods(self) -> MethodsOperations:
        """Operations on :class:`~dyff.schema.platform.Method` entities."""
        return self._methods

    @property
    def measurements(self) -> MeasurementsOperations:
        """Operations on :class:`~dyff.schema.platform.Measurement` entities."""
        return self._measurements

    @property
    def models(self) -> ModelsOperations:
        """Operations on :class:`~dyff.schema.platform.Model` entities."""
        return self._models

    @property
    def modules(self) -> ModulesOperations:
        """Operations on :class:`~dyff.schema.platform.Module` entities."""
        return self._modules

    @property
    def reports(self) -> ReportsOperations:
        """Operations on :class:`~dyff.schema.platform.Report` entities."""
        return self._reports

    @property
    def safetycases(self) -> SafetycasesOperations:
        """Operations on :class:`~dyff.schema.platform.SafetyCase` entities."""
        return self._safetycases


__all__ = [
    "Client",
    "InferenceSessionClient",
    "RawClient",
    "HttpResponseError",
]
