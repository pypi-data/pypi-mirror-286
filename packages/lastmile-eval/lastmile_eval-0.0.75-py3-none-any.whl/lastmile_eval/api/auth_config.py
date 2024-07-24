from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RealAuthenticationConfig:
    api_token: str


@dataclass(frozen=True)
class MockAuthenticationConfig:
    post_fn: Any  # TODO type this


AuthenticationConfig = RealAuthenticationConfig | MockAuthenticationConfig
