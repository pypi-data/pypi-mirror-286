import os

from dotenv import find_dotenv, load_dotenv
from lastmile_eval.common.types import APIToken

# TODO: Pull out other common utils from rag/debugger and move here


def get_lastmile_api_token(lastmile_api_token: str | None = None) -> APIToken:
    return (
        APIToken(lastmile_api_token)
        if lastmile_api_token is not None
        else APIToken(api_token_from_dot_env("LASTMILE_API_TOKEN"))
    )


def api_token_from_dot_env(key: str) -> str:
    load_dotenv_from_cwd()
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Environment variable '{key}' not found. Check your .env file."
        )

    return value


def load_dotenv_from_cwd() -> bool:
    """
    Helper method needed to ensure that when we load the .env file, we load it
    from user's current cwd, not the published package location, which could
    otherwise lead to error since we wil lbe unable to detect an .env file.
    """
    dotenv_path = find_dotenv(usecwd=True)
    return load_dotenv(dotenv_path=dotenv_path)
