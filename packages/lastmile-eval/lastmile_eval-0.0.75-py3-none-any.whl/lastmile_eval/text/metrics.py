import json
import logging
from textwrap import dedent
from typing import Any, Sequence, Optional

# Bleu
from evaluate import EvaluationModule, load  # type: ignore[fixme]

from lastmile_eval.text.metrics_lib import make_llm_score_function
from lastmile_eval.api.auth_config import RealAuthenticationConfig
from lastmile_eval.api.evaluations import (
    DEFAULT_EVALUATIONS_API as EVALUATIONS_API,
    EvaluationMetric,
)
from lastmile_eval.common.utils import get_lastmile_api_token

logger = logging.getLogger(__name__)
logging.basicConfig()


def calculate_bleu_score(
    outputs: Sequence[str], ground_truth: Sequence[str]
) -> list[float]:
    """
    Calculate BLEU scores for a set of hypotheses against corresponding GT.


    Args:
        outputs (Sequence[str]): The generated outputs to evaluate.
        ground_truth (Sequence[Sequence[str]]):
        The reference outputs for evaluation.
        Each set of ground_truth corresponds to one text.

    Returns:
        list[float]: A list of BLEU scores for each text-reference pair.

    Raises:
        ValueError: If the number of outputs and the number of sets of ground_truth are not equal.
    """

    if len(outputs) != len(ground_truth):
        raise ValueError(
            f"Number of predictions ({len(outputs)}) and ground_truth ({len(ground_truth)}) must be equal."
        )

    bleu_metric: EvaluationModule = load("bleu")

    def _score_pair(text: str, reference: str) -> float:
        results: dict[Any, Any] = bleu_metric.compute(  # type: ignore[fixme]
            predictions=[text], references=[[reference]]
        )
        return results["bleu"]

    return [
        _score_pair(text, reference)
        for text, reference in zip(outputs, ground_truth)
    ]


def calculate_exact_match_score(
    outputs: Sequence[str], ground_truth: Sequence[str]
) -> list[float]:
    """
    Calculate Exact Match score for a set of hypotheses against corresponding sets of reference outputs.


    Args:
        outputs (Sequence[str]): The generated outputs to evaluate.
        ground_truth (Sequence[str]):
        The reference outputs for evaluation.
        Each set of ground_truth corresponds to one text.

    Returns:
        list[float]: A list of Exact Match scores for each text-reference pair.

    Raises:
        ValueError: If the number of outputs and the number of sets of ground_truth are not equal.
    """

    if len(outputs) != len(ground_truth):
        raise ValueError(
            f"Number of predictions ({len(outputs)}) and ground_truth ({len(ground_truth)}) must be equal."
        )

    def _score_pair(text: str, reference: str) -> float:
        name = "exact_match"
        metric = load(name)
        out = metric.compute(predictions=[text], references=[reference])  # type: ignore[no-untyped-call]
        return out[name]  # type: ignore[no-member]

    return [
        _score_pair(text, reference)
        for text, reference in zip(outputs, ground_truth)
    ]


def calculate_rouge1_score(
    outputs: Sequence[str], ground_truth: Sequence[Sequence[str]]
) -> list[float]:
    """
    Calculate Rouge-1 score for a set of hypotheses against corresponding sets of reference outputs.


    Args:
        outputs (Sequence[str]): The generated outputs to evaluate.
        ground_truth (Sequence[Sequence[str]]):
        The reference outputs for evaluation.
        Each set of ground_truth corresponds to one text.

    Returns:
        list[float]: A list of Rouge-1 scores for each text-reference pair.

    Raises:
        ValueError: If the number of outputs and the number of sets of ground_truth are not equal.
    """

    if len(outputs) != len(ground_truth):
        raise ValueError(
            f"Number of predictions ({len(outputs)}) and ground_truth ({len(ground_truth)}) must be equal."
        )

    bleu_metric: EvaluationModule = load("rouge")

    def _score_pair(text: str, reference: Sequence[str]) -> float:
        results: dict[Any, Any] = bleu_metric.compute(
            predictions=[text], references=[reference]
        )  # type: ignore[no-untyped-call]
        return results["rouge1"]

    return [
        _score_pair(text, reference)
        for text, reference in zip(outputs, ground_truth)
    ]


def _get_evaluation_score(
    metric: EvaluationMetric,
    ground_truth_values: Optional[Sequence[str]],
    inputs: Optional[Sequence[str]],
    outputs: Optional[Sequence[str]],
    lastmile_api_token: str | None = None,
) -> list[float]:
    """
    Get the evaluation score for a given metric

    :param metric:
    :param ground_truth_values:
    :param inputs:
    :param outputs:
    :param lastmile_api_token:
    :return:
    """
    lastmile_api_token = get_lastmile_api_token(lastmile_api_token)
    auth_config = RealAuthenticationConfig(lastmile_api_token)
    http_response = EVALUATIONS_API.get_evaluations(
        metric,
        ground_truth_values,
        inputs,
        outputs,
        auth_config,
    )
    if http_response.status_code != 200:
        # TODO (rossdan): Add retry policies
        raise ValueError(
            f"Error in evaluation http responses: {http_response.text}"
        )

    evals_result: dict[str, list[float]] = json.loads(http_response.text)
    return evals_result[metric]


def calculate_relevance_score(
    inputs: Sequence[str],
    outputs: Sequence[str],
    lastmile_api_token: str | None = None,
    model_name: str | None = None,
) -> list[float]:
    """
    Evaluates the relevance of output strings against input strings using a specific evaluation model,
    and returns a list of float scores representing the relevance of each input-reference pair.

    Args:
        inputs: (Sequence[str]): A sequence of input strings to evaluate the outputs against.
        outputs (Sequence[str]): A sequence of output strings to be evaluated.
        lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        model_name (str | None, optional): Deprecated. Name of the model to use for evaluation.

    Returns:
        List[float]: A list of float scores indicating the relevance of each input-reference pair,
                     where 1.0 denotes 'relevant' and 0.0 denotes otherwise.
    """
    if model_name is not None:
        logger.warning(
            "Deprecation Notice: `model_name` no longer configurable"
        )

    return _get_evaluation_score(
        metric=EvaluationMetric.RELEVANCE,
        ground_truth_values=None,
        inputs=inputs,
        outputs=outputs,
        lastmile_api_token=lastmile_api_token,
    )


def calculate_faithfulness_score(
    outputs: Sequence[str],
    ground_truth: Sequence[str],
    inputs: Sequence[str],
    lastmile_api_token: str | None = None,
) -> list[float]:
    """
    Calculate faithfulness score for a set of outputs against corresponding ground truth and inputs.

    Args:
        outputs (Sequence[str]): The generated outputs to evaluate.
        ground_truth (Sequence[str]): The reference outputs for evaluation.
        inputs (Sequence[str]): The input prompts used to generate the outputs.
        lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens

    Returns:
        list[float]: A list of faithfulness scores.

    Raises:
        ValueError: If the lengths of ground_truth, inputs, and outputs are not equal.
    """
    query_length = len(inputs)
    if len(ground_truth) != query_length or len(outputs) != query_length:
        raise ValueError(
            "Length of ground_truth, inputs, and outputs arrays must all be equal."
        )

    # Note: be careful of argument order rearrangement
    return _get_evaluation_score(
        EvaluationMetric.P_FAITHFUL,
        ground_truth,
        inputs,
        outputs,
        lastmile_api_token,
    )


def calculate_toxicity_score(
    outputs: Sequence[str],
    lastmile_api_token: str | None = None,
    model_name: str | None = None,
) -> list[float]:
    """
    Calculate toxicity scores for a set of outputs.

    Args:
        outputs (Sequence[str]): A sequence of input strings to be evaluated.
        lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        model_name (str | None, optional): Deprecated. Name of the model to use for evaluation.

    Returns:
        List[float]: A list of toxicity scores.
    """
    if model_name is not None:
        logger.warning(
            "Deprecation Notice: `model_name` no longer configurable"
        )

    return _get_evaluation_score(
        EvaluationMetric.TOXICITY,
        None,
        None,
        outputs,
        lastmile_api_token,
    )


def calculate_qa_score(
    outputs: Sequence[str],
    ground_truth: Sequence[str],
    inputs: Sequence[str],
    lastmile_api_token: str | None = None,
    model_name: str | None = None,
) -> list[float]:
    """
    Calculate QA scores for a set of outputs against corresponding ground truth and inputs.

    Args:
        outputs (Sequence[str]): A sequence of output strings to be evaluated.
        ground_truth (Sequence[str]): A sequence of reference strings to evaluate the inputs against.
        inputs (Sequence[str]): A sequence of input questions.
        lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        model_name (str | None, optional): Deprecated. Name of the model to use for evaluation.

    Returns:
        List[float]: A list of QA scores.
    """
    if model_name is not None:
        logger.warning(
            "Deprecation Notice: `model_name` no longer configurable"
        )

    return _get_evaluation_score(
        EvaluationMetric.QA,
        ground_truth,
        inputs,
        outputs,
        lastmile_api_token,
    )


def calculate_summarization_score(
    outputs: Sequence[str],
    ground_truth: Sequence[str],
    lastmile_api_token: str | None = None,
    model_name: str | None = None,
) -> list[float]:
    """
    Calculate summarization scores for a set of outputs against corresponding ground truth.

    Args:
        outputs (Sequence[str]): A sequence of output strings to be evaluated.
        ground_truth (Sequence[str]): A sequence of reference strings to evaluate the inputs against.
        lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        model_name (str | None, optional): Deprecated. Name of the model to use for evaluation.

    Returns:
        List[float]: A list of summarization scores.
    """
    if model_name is not None:
        logger.warning(
            "Deprecation Notice: `model_name` no longer configurable"
        )

    return _get_evaluation_score(
        EvaluationMetric.SUMMARIZATION,
        ground_truth,
        None,
        outputs,
        lastmile_api_token,
    )


def calculate_human_vs_ai_score(
    outputs: Sequence[str],
    ground_truth: Sequence[str],
    inputs: Sequence[str],
    lastmile_api_token: str | None = None,
    model_name: str | None = None,
) -> list[float]:
    """
    Calculate human vs AI scores for a set of outputs against corresponding ground truth and inputs.

    Args:
        outputs (Sequence[str]): Model outputs to evaluate.
        ground_truth (Sequence[str]): Presumably human reference responses.
        inputs (Sequence[str]): Prompts which the above are intended answers to.
                lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        lastmile_api_token (str | None, optional): The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        model_name (str | None, optional): Deprecated. Name of the model to use for evaluation.

    Returns:
        List[float]: A list of human vs AI scores.
    """
    if model_name is not None:
        logger.warning(
            "Deprecation Notice: `model_name` no longer configurable"
        )

    return _get_evaluation_score(
        EvaluationMetric.HUMAN_VS_AI,
        ground_truth,
        inputs,
        outputs,
        lastmile_api_token,
    )


def calculate_custom_llm_metric_example_sentiment(
    outputs: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """

    Args:
        outputs (Sequence[str]): The generated texts to evaluate.
        model_name (str): The name of the evaluation model to use.

    Returns:
        list[float]: A list of custom sentiment scores for each text.
    """

    prompt_template = dedent(
        """
        How happy is the following text on a scale of 0 to 1?
        {text_to_evaluate}
        """
    )

    input_names = ["text_to_evaluate"]
    scorer = make_llm_score_function(prompt_template, model_name, input_names)
    return scorer(outputs)


def calculate_custom_llm_metric_example_semantic_similarity(
    outputs: Sequence[str],
    ground_truth: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """

    Args:
        outputs (Sequence[str]): The generated texts to evaluate.
        ground_truth (Sequence[str]): The reference texts to evaluate against.
        model_name (str): The name of the evaluation model to use.

    Returns:
        list[float]: A list of custom similarity scores for each text.
    """

    prompt_template = dedent(
        """
        How similar is the following text to the reference on a scale of 0 to 1
        
        Text: {text_to_evaluate}         
        Reference: {reference}
        """
    )

    input_names = ["text_to_evaluate", "reference"]
    scorer = make_llm_score_function(prompt_template, model_name, input_names)
    return scorer(outputs, ground_truth)
