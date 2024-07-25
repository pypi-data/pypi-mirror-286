"""MLflow-related util functions.

This source file contains code from [MLflow](https://github.com/mlflow/mlflow)
licensed under Apache-2.0 license, see
[here](https://github.com/mlflow/mlflow/blob/1eef4641df6f605b7d9faa83b0fc25e65877dbf4/LICENSE.txt)  # noqa: E501
for the original license.

Changes made to the original source code are denoted as such with comments.
"""
import typing as t

from ruamel.yaml import YAML

import mantik.utils.env as env

TRACKING_URI_ENV_VAR = "MLFLOW_TRACKING_URI"
TRACKING_TOKEN_ENV_VAR = "MLFLOW_TRACKING_TOKEN"
TRACKING_USERNAME_ENV_VAR = "MLFLOW_TRACKING_USERNAME"
TRACKING_PASSWORD_ENV_VAR = "MLFLOW_TRACKING_PASSWORD"
EXPERIMENT_NAME_ENV_VAR = "MLFLOW_EXPERIMENT_NAME"
EXPERIMENT_ID_ENV_VAR = "MLFLOW_EXPERIMENT_ID"
ACTIVE_RUN_ID_ENV_VAR = "ACTIVE_RUN_ID"

CONFLICTING_ENV_VARS = (
    TRACKING_USERNAME_ENV_VAR,
    TRACKING_PASSWORD_ENV_VAR,
)

DEFAULT_TRACKING_URI = "https://api.cloud.mantik.ai/tracking/"


def unset_conflicting_env_vars() -> None:
    env.unset_env_vars(CONFLICTING_ENV_VARS)


def overwrite_entrypoint_command(
    original_command: str, env_vars: t.Dict
) -> str:
    export_command = "export " + " ".join(
        [f"{key}='{value}'" for key, value in env_vars.items()]
    )
    return f"{export_command} && {original_command}"


def update_mlproject_yaml_with_env_vars_for_entrypoint(
    mlproject_yaml_file: str, env_vars: t.Dict, entrypoint: str = "main"
) -> None:
    yaml = YAML()
    yaml.preserve_quotes = True

    # Read the existing YAML file
    with open(mlproject_yaml_file) as file:
        data = yaml.load(file)

    # Update the command in the entry_points section
    data["entry_points"][entrypoint]["command"] = overwrite_entrypoint_command(
        original_command=data["entry_points"][entrypoint]["command"],
        env_vars=env_vars,
    )

    # Write the updated YAML back to the file
    with open(mlproject_yaml_file, "w") as file:
        yaml.dump(data, file)
