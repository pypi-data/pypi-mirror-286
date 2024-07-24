import pytest
from unittest.mock import patch, MagicMock
from lastmile_eval.text.metrics import (
    calculate_relevance_score,
    calculate_faithfulness_score,
    calculate_toxicity_score,
    calculate_qa_score,
    calculate_summarization_score,
    calculate_human_vs_ai_score,
    calculate_custom_llm_metric_example_sentiment,
    calculate_custom_llm_metric_example_semantic_similarity,
)
from lastmile_eval.api.evaluations import EvaluationMetric

LASTMILE_API_TOKEN = "test_token"


@pytest.fixture
def mock_get_evaluation_score():
    with patch("lastmile_eval.text.metrics._get_evaluation_score") as mock:
        yield mock


def test_calculate_relevance_score(mock_get_evaluation_score):
    outputs = ["output1", "output2"]
    inputs = ["input1", "input2"]

    mock_get_evaluation_score.return_value = [0.8, 0.9]

    result = calculate_relevance_score(inputs, outputs, LASTMILE_API_TOKEN)

    mock_get_evaluation_score.assert_called_once_with(
        metric=EvaluationMetric.RELEVANCE,
        ground_truth_values=None,
        inputs=inputs,
        outputs=outputs,
        lastmile_api_token=LASTMILE_API_TOKEN,
    )
    assert result == [0.8, 0.9]


def test_calculate_faithfulness_score(mock_get_evaluation_score):
    outputs = ["output1", "output2"]
    ground_truth = ["truth1", "truth2"]
    inputs = ["input1", "input2"]

    mock_get_evaluation_score.return_value = [0.7, 0.8]

    result = calculate_faithfulness_score(
        outputs, ground_truth, inputs, LASTMILE_API_TOKEN
    )

    mock_get_evaluation_score.assert_called_once_with(
        EvaluationMetric.P_FAITHFUL,
        ground_truth,
        inputs,
        outputs,
        LASTMILE_API_TOKEN,
    )
    assert result == [0.7, 0.8]


def test_calculate_toxicity_score(mock_get_evaluation_score):
    outputs = ["output1", "output2"]

    mock_get_evaluation_score.return_value = [0.1, 0.2]

    result = calculate_toxicity_score(outputs, LASTMILE_API_TOKEN)

    mock_get_evaluation_score.assert_called_once_with(
        EvaluationMetric.TOXICITY,
        None,
        None,
        outputs,
        LASTMILE_API_TOKEN,
    )
    assert result == [0.1, 0.2]


def test_calculate_qa_score(mock_get_evaluation_score):
    outputs = ["output1", "output2"]
    ground_truth = ["truth1", "truth2"]
    inputs = ["input1", "input2"]

    mock_get_evaluation_score.return_value = [0.6, 0.7]

    result = calculate_qa_score(
        outputs, ground_truth, inputs, LASTMILE_API_TOKEN
    )

    mock_get_evaluation_score.assert_called_once_with(
        EvaluationMetric.QA,
        ground_truth,
        inputs,
        outputs,
        LASTMILE_API_TOKEN,
    )
    assert result == [0.6, 0.7]


def test_calculate_summarization_score(mock_get_evaluation_score):
    outputs = ["output1", "output2"]
    ground_truth = ["truth1", "truth2"]

    mock_get_evaluation_score.return_value = [0.5, 0.6]

    result = calculate_summarization_score(
        outputs, ground_truth, LASTMILE_API_TOKEN
    )

    mock_get_evaluation_score.assert_called_once_with(
        EvaluationMetric.SUMMARIZATION,
        ground_truth,
        None,
        outputs,
        LASTMILE_API_TOKEN,
    )
    assert result == [0.5, 0.6]


def test_calculate_human_vs_ai_score(mock_get_evaluation_score):
    outputs = ["output1", "output2"]
    ground_truth = ["truth1", "truth2"]
    inputs = ["input1", "input2"]

    mock_get_evaluation_score.return_value = [0.4, 0.5]

    result = calculate_human_vs_ai_score(
        outputs, ground_truth, inputs, LASTMILE_API_TOKEN
    )

    mock_get_evaluation_score.assert_called_once_with(
        EvaluationMetric.HUMAN_VS_AI,
        ground_truth,
        inputs,
        outputs,
        LASTMILE_API_TOKEN,
    )
    assert result == [0.4, 0.5]


@patch("lastmile_eval.text.metrics.make_llm_score_function")
def test_calculate_custom_llm_metric_example_sentiment(
    mock_make_llm_score_function,
):
    outputs = ["Happy text", "Sad text"]
    mock_scorer = MagicMock()
    mock_scorer.return_value = [0.8, 0.2]
    mock_make_llm_score_function.return_value = mock_scorer

    result = calculate_custom_llm_metric_example_sentiment(outputs)

    mock_make_llm_score_function.assert_called_once()
    mock_scorer.assert_called_once_with(outputs)
    assert result == [0.8, 0.2]


@patch("lastmile_eval.text.metrics.make_llm_score_function")
def test_calculate_custom_llm_metric_example_semantic_similarity(
    mock_make_llm_score_function,
):
    outputs = ["Similar text", "Different text"]
    ground_truth = ["Reference 1", "Reference 2"]
    mock_scorer = MagicMock()
    mock_scorer.return_value = [0.9, 0.3]
    mock_make_llm_score_function.return_value = mock_scorer

    result = calculate_custom_llm_metric_example_semantic_similarity(
        outputs, ground_truth
    )

    mock_make_llm_score_function.assert_called_once()
    mock_scorer.assert_called_once_with(outputs, ground_truth)
    assert result == [0.9, 0.3]
