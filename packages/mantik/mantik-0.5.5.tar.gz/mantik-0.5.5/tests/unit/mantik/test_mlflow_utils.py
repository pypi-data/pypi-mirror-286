import mantik.utils.mlflow as mlflow_utils


def test_overwrite_entrypoint_command() -> None:
    original_command = "python train.py"
    expected_command = (
        "export VAR_1='VALUE_1' VAR_2='VALUE_2' && python train.py"
    )
    env_vars = {"VAR_1": "VALUE_1", "VAR_2": "VALUE_2"}

    assert (
        mlflow_utils.overwrite_entrypoint_command(
            original_command=original_command, env_vars=env_vars
        )
        == expected_command
    )
