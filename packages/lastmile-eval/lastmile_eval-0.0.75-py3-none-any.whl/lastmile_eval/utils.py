"""
Simple utils wrapper for evaluation framework.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from lastmile_eval.api.evaluations import EvaluationMetric
from lastmile_eval.text.metrics import calculate_faithfulness_score

logger = logging.getLogger(__name__)
logging.basicConfig()


@dataclass(frozen=True)
class RagEvalConfig:
    """
    The evaluation configuration to tell our endpoint how to evaluate
    the request
    """

    model_names: list[str] = field(default_factory=lambda: ["p-faithful-v0"])


def get_rag_eval_scores(
        queries: list[str],
        data: list[str],
        responses: list[str],
        api_token: str,
        config: RagEvalConfig | None = None,
        # TODO (rossdan): Add options for batch and retry policies
        # TODO: try to type this better than `Any`.
        # However, it's better to underpromise structure than overpromise, if we need to change it.
) -> dict[str, Any]:
    """
    Get faithfulness scores for a batch of N LLM's outputs in relation to the data
    provided as well as the queries. The queries, data, and responses
    must all be lists of length N.

    @param queries (list[str]): Queries that were passed to the LLM
    @param data (list[str]): Ground truth upon which we will evaluate the
        LLM's outputs (for example, you can use the data that was given to
        the LLM along with the queries)
    @param responses (list[str]): Output of the LLM when given the queries
    @param api_token (str): API key for the LastMile evaluation endpoint.
        Get it from here: https://lastmileai.dev/settings?page=tokens
    @param model_endpoint_id (str): enum for which model to use in the endpoint

    @return dict: JSON responses containing faithfulness scores and any relevant metadata.

    Example
    Input:
        queries = ["what color is the sky?", "what color is the sky?"]
        statement1 = "the sky is red"
        statement2 = "the sky is blue"
        data = [statement1, statement1]
        responses = [statement1, statement2]
        get_rag_eval_scores(queries, data, responses, api_token)
    Output:
        {'p_faithful': [0.9956, 6.857e-05]}
    """
    if config is not None:
        logger.warning("Deprecation Notice: `config` no longer configurable on `get_rag_eval_scores`. Ignoring.")

    return {
        EvaluationMetric.P_FAITHFUL: calculate_faithfulness_score(responses, data, queries, api_token)
    }
