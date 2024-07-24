import json
import logging
import os
from enum import Enum
from typing import Any, Optional, Sequence

import requests

from lastmile_eval.api.auth_config import AuthenticationConfig, MockAuthenticationConfig, RealAuthenticationConfig

_DEFAULT_EVALUATIONS_API_BASE_URL = "https://lastmileai.dev"
EVALUATIONS_API_BASE_URL_ENV_VAR = "EVALUATIONS_API_BASE_URL"
EVALUATIONS_API_BASE_URL = os.environ.get(EVALUATIONS_API_BASE_URL_ENV_VAR, _DEFAULT_EVALUATIONS_API_BASE_URL)

logger = logging.getLogger(__name__)
logging.basicConfig()


class EvaluationMetric(str, Enum):
    P_FAITHFUL = "p_faithful"
    RELEVANCE = "relevance"
    TOXICITY = "toxicity"
    QA = "qa"
    SUMMARIZATION = "summarization"
    HUMAN_VS_AI = "human_vs_ai"


class EvaluationsApi:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get_evaluations_endpoint_url(self):
        return f"{self.base_url}/api/evaluation"

    def get_evaluations(  # pylint: disable=too-many-arguments
            self,
            metric: EvaluationMetric,
            ground_truth_values: Optional[Sequence[str]],
            inputs: Optional[Sequence[str]],
            outputs: Optional[Sequence[str]],
            authentication_config: AuthenticationConfig,

    ) -> requests.Response:
        """
        Call the LastMile endpoint to perform evaluation on a granular segment
        of data. This is a low-level function that is unaware on how the infra
        surrounding this call (ex: batch + retry policy) was handled.
        """

        # TODO: type the payload better
        payload: Any = {
            "ground_truth": ground_truth_values,
            "input": inputs,
            "output": outputs,
        }
        evaluations_url = self._get_evaluations_endpoint_url()

        if metric:
            payload["modelEndpointId"] = metric

        logger.debug(f"Evaluating:\nPOST {evaluations_url}\n{json.dumps(payload, indent=2)}")
        result = None
        match authentication_config:
            case RealAuthenticationConfig(api_token=api_token):
                result = requests.post(
                    evaluations_url,
                    headers={"Authorization": f"Bearer {api_token}"},
                    json=payload,
                    # TODO (rossdan): Add timeout and retry policies
                    timeout=60,
                )
            case MockAuthenticationConfig(post_fn=post_fn):
                result = post_fn(
                    _data=payload,
                )

        if result and result.ok:
            logger.debug(f"Result:\n{json.dumps(result.json(), indent=2)}")
        else:
            logger.debug(f"Result: {result.status_code}")

        return result


DEFAULT_EVALUATIONS_API = EvaluationsApi(EVALUATIONS_API_BASE_URL)
