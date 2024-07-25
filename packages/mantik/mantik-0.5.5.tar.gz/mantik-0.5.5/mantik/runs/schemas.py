import dataclasses
import typing as t
import uuid


@dataclasses.dataclass
class RunConfiguration:
    name: str
    experiment_repository_id: uuid.UUID
    code_repository_id: uuid.UUID
    branch: t.Optional[str]
    commit: t.Optional[str]
    data_repository_id: t.Optional[uuid.UUID]
    mlflow_mlproject_file_path: str
    entry_point: str
    mlflow_parameters: dict
    backend_config: dict
    mlflow_run_id: t.Optional[uuid.UUID] = None
    data_version: t.Optional[str] = None

    def to_post_payload(self) -> dict:
        return {
            "name": self.name,
            "experimentRepositoryId": str(self.experiment_repository_id),
            "codeRepositoryId": str(self.code_repository_id),
            "branch": self.branch,
            "commit": self.commit,
            "dataRepositoryId": str(self.data_repository_id)
            if self.data_repository_id is not None
            else None,
            "dataVersion": self.data_version if self.data_version else None,
            "mlflowMlprojectFilePath": self.mlflow_mlproject_file_path,
            "entryPoint": self.entry_point,
            "mlflowParameters": self.mlflow_parameters,
            "backendConfig": self.backend_config,
            "mlflowRunId": str(self.mlflow_run_id),
        }
