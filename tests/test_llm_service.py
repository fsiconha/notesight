import os
import pytest
from unittest.mock import patch, MagicMock
from huggingface_hub.utils import HfHubHTTPError

from diary.services.llm_service import get_insights_from_notes, extract_insights

# Dummy note class for testing.
class DummyNote:
    def __init__(self, title, content):
        self.title = title
        self.content = content

def test_extract_insights_with_marker():
    response = "Algum texto irrelevante. Insights: Aqui estão alguns insights acionáveis."
    result = extract_insights(response)
    assert result == "Aqui estão alguns insights acionáveis."

def test_extract_insights_without_marker():
    response = "Apenas um texto simples sem marcador."
    result = extract_insights(response)
    assert result == "Apenas um texto simples sem marcador."

@patch("diary.services.llm_service.HuggingFaceHub")
@patch("diary.services.llm_service.LLMChain")
def test_get_insights_from_notes_success(mock_llmchain, mock_huggingfacehub):
    # Ensure the environment variable is set.
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "dummy_token"

    # Create a dummy chain instance that returns a known output.
    dummy_chain = MagicMock()
    # Simulate a response that contains the marker "Insights:".
    dummy_chain.run.return_value = (
        "Algum texto de preâmbulo. Insights: Sugestão prática: priorize tarefas importantes."
    )
    mock_llmchain.return_value = dummy_chain

    # Create a list of dummy notes.
    notes = [
        DummyNote("Meeting", "Discutir prazos e alocação de recursos."),
        DummyNote("Reflexão", "Preciso organizar melhor minhas tarefas diárias.")
    ]

    result = get_insights_from_notes(notes)
    # Check that the fallback marker text is removed and the actionable insight is present.
    assert "Sugestão prática: priorize tarefas importantes." in result
    # And that the final message is formatted as expected.
    assert result.startswith("Insights from your indexed notes:")

@patch("diary.services.llm_service.HuggingFaceHub")
@patch("diary.services.llm_service.LLMChain")
def test_get_insights_from_notes_error(mock_llmchain, mock_huggingfacehub):
    # Set the environment variable.
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "dummy_token"

    # Create a dummy chain instance that raises an HfHubHTTPError.
    dummy_chain = MagicMock()
    dummy_chain.run.side_effect = HfHubHTTPError("Simulated connection error")
    mock_llmchain.return_value = dummy_chain

    # Create dummy notes.
    notes = [DummyNote("Error Note", "This note will trigger an error.")]

    # The function should catch the error and return the fallback message.
    result = get_insights_from_notes(notes)
    assert "Sorry, the LLM service is currently unavailable" in result
