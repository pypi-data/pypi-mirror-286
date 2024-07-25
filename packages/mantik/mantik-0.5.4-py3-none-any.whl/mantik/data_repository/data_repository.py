import logging
import os
import pathlib
import subprocess
import typing as t
import uuid

import git

import mantik.authentication.tokens as tokens
import mantik.utils.env_vars as env_vars
import mantik.utils.mantik_api.connection
import mantik.utils.mantik_api.data_repository
import mantik.utils.other as utils_other

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def data_download(
    project_id: t.Optional[uuid.UUID] = None,
    data_repository_id: t.Optional[uuid.UUID] = None,
    version: t.Optional[str] = None,
    target_dir: t.Optional[pathlib.Path] = None,
    mantik_access_token: t.Optional[str] = None,
) -> str:
    """Downloads a GIT based data repository, along with its DVC files.

    Is meant to be used in the training script.
    `import mantik`
    `mantik.data_download()`
    """
    try:
        project_id = project_id or os.environ[env_vars.PROJECT_ID_ENV_VAR]
        data_repository_id = (
            data_repository_id
            or os.environ[env_vars.DATA_REPOSITORY_ID_ENV_VAR]
        )
        target_dir = target_dir or pathlib.Path(
            os.environ[env_vars.TARGET_DIR_ENV_VAR]
        )
        mantik_access_token = (
            mantik_access_token
            or os.environ[env_vars.MANTIK_ACCESS_TOKEN_ENV_VAR]
        )
    except KeyError as e:
        raise RuntimeError(
            f"mantik.data_download() requires environment variable {e}"
        )

    version = version or os.getenv(env_vars.DATA_REPOSITORY_VERSION_ENV_VAR)
    return download_data_repository(
        project_id=project_id,
        data_repository_id=data_repository_id,
        version=version,
        target_dir=target_dir,
        token=mantik_access_token,
    )


def download_data_repository(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    version: t.Optional[str],
    target_dir: pathlib.Path,
    token: str,
) -> str:
    """Downloads a GIT based data repository, along with its DVC files."""
    data_repository_details = mantik.utils.mantik_api.data_repository.get_one(
        project_id=project_id,
        data_repository_id=data_repository_id,
        token=token,
    )
    desired_git_commit_hash = None
    if version is not None:
        available_versions = list(data_repository_details.versions.keys())

        if version not in available_versions:
            raise ValueError(
                f"Invalid version '{version}' specified. Available "
                f"data versions: '{available_versions}'"
            )

        desired_git_commit_hash = data_repository_details.versions[version]

    git_clone_with_commit_hash(
        git_uri=data_repository_details.uri,
        git_commit_hash=desired_git_commit_hash,
        target_dir=target_dir,
    )

    if (
        not data_repository_details.is_dvc_enabled
        or not data_repository_details.dvc_connection_id
    ):
        return f"Cloned to {target_dir}"

    connection = mantik.utils.mantik_api.connection.get(
        user_id=uuid.UUID(tokens.get_user_id_from_token(token)),
        connection_id=data_repository_details.dvc_connection_id,
        token=token,
    )

    if connection.connection_provider == "S3":
        dvc_pull_with_aws_credentials(
            aws_access_key_id=connection.login_name,
            aws_secret_access_key=connection.password,
            target_dir=target_dir,
        )
    else:
        raise ValueError(
            "Connection provider not supported by our DVC backend."
        )

    return f"Cloned to {target_dir} with DVC"


def git_clone_with_commit_hash(
    git_uri: str, git_commit_hash: str, target_dir: pathlib.Path
):
    """Make target folder, git clone, and checkout a specific commit."""

    # clone the git repository
    logger.info("Cloning the git data repository...")
    target_dir.mkdir(parents=True, exist_ok=True)
    repo = git.Repo.clone_from(git_uri, target_dir)

    # checkout desired version
    if not git_commit_hash:
        return

    with utils_other.temp_chdir(target_dir):
        repo.git.checkout(git_commit_hash)


def dvc_pull_with_aws_credentials(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    target_dir: t.Optional[pathlib.Path] = None,
):
    """Perform DVC pull using S3 as a DVC backend"""
    verify_dvc_is_installed()
    logger.info("Pulling files from the DVC backend...")

    with utils_other.temp_chdir(target_dir or os.getcwd()):
        subprocess.run(
            ["dvc", "pull"],
            env={
                "PATH": os.environ["PATH"],
                "AWS_ACCESS_KEY_ID": aws_access_key_id,
                "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
            },
        )


def verify_dvc_is_installed():
    try:
        logger.info("Verifying dvc installation...")
        subprocess.run(["dvc", "--version"])
    except FileNotFoundError:
        raise RuntimeError(
            "DVC is not installed. Please refer to https://dvc.org/doc/install"
        )
    else:
        logger.info("DVC is installed.")
