import pytest
import random

from smartenough import get_smart_answer, get_supported_providers
from smartenough.llm import UnsupportedProviderException, UnsupportedValidationException


def test_get_smart_answer_with_model_provider():
    result = get_smart_answer("How do you say 'Hello' in French?", model_provider="OpenAI")
    assert "bonjour" in result.lower()


# Test get_supported_providers function
def test_get_supported_providers():
    providers = get_supported_providers()
    assert isinstance(providers, list)
    assert "OpenRouter" in providers
    assert "Random" in providers


# Test UnsupportedModelException
def test_unsupported_provider_exception():
    with pytest.raises(UnsupportedProviderException):
        get_smart_answer("Test", model_provider="UnsupportedModel")


# Test UnsupportedValidationException
def test_unsupported_validation_exception():
    with pytest.raises(UnsupportedValidationException):
        get_smart_answer("Test", validation="unsupported")


# Test URL validation
def test_url_validation_openrouter():
    result = get_smart_answer("Give me a list of some interesting news sites, return only valid urls please", model_provider="OpenRouter", validation="url")
    assert isinstance(result, list)
    
    #Retry one, because OpenRouter sometimes returns empty list
    if result == []:
        result = get_smart_answer("Give me a list of some interesting news sites, return only valid urls please", model_provider="OpenRouter", validation="url")

    #Retry two, because OpenRouter sometimes returns empty list
    if result == []:
        result = get_smart_answer("Give me a list of some interesting news sites, return only valid urls please", model_provider="OpenRouter", validation="url")
    
    #It should be good by now.
    assert all(url.startswith("http") for url in result)


# Test HTML validation
def test_html_validation():
    def generate_html(model_provider):
        result = get_smart_answer("Create a simple HTML page with a title 'Test'", model_provider=model_provider, validation="html")
        assert "<html" in result.lower()
        assert "<title>" in result
        assert "Test" in result
    
    providers = get_supported_providers()
    providers.remove("Random")
    providers.remove("OpenRouter")

    for provider in providers:
        generate_html(provider)


# Test sentiment analysis example
def test_sentiment_analysis():
    def sentiment_analysis(text):
        instructions = f"""
        Classify the sentiment of the following text as 'positive', 'negative', or 'neutral'.
        Return the result in the following JSON format:
        {{
            "sentiment": "<sentiment_label>"
        }}

        Text: {text}
        """
        result = get_smart_answer(instructions, additional_context=text, model_provider="Random", validation="json")
        return result

    positive_text = "I absolutely love this product! It exceeded my expectations."
    negative_text = "The service was terrible. I won't be coming back."

    positive_result = sentiment_analysis(positive_text)
    negative_result = sentiment_analysis(negative_text)

    assert positive_result["sentiment"] == "positive"
    assert negative_result["sentiment"] == "negative"

