# smartenough

Effortlessly convert inexpensive (and sometimes free) Large Language Models (LLMs) into efficient, validated API calls. Designed for speed, stability, and simplicity, making it ideal for routing individual calls to low-cost LLMs and ensuring validated outputs.

![](https://codeberg.org/Medusa-Intelligence-Corp/smartenough/media/branch/main/smartenough.png)

*I'm good enough, I'm smart enough, and doggone it, people like me!*

## Project Goals

- Be lightweight and easy to use
- Be very fast in implementing the latest models
- Don't lock ourselves into any one model provider
- Save money by using the cheapest models available

## Opinionated

Smartenough is 'opinionated' in that it chooses the newest, cheapest, and best models for you from each provider (see details in code [here](https://codeberg.org/Medusa-Intelligence-Corp/smartenough/src/branch/main/src/smartenough/llm.py#L215)). This saves you from having to think about the details. Smartenough is designed to be simple and easy to use, and to provide the best results for the lowest cost.

Note that if you are installing ```openai```, ```anthropic```, ```mistralai```, or ```google-generativeai``` packages yourself by hand, and hard-coding version numbers, then things might break. Smartenough will only support the latest versions of the packages. Use old versions at your own risk.

## Current Provider Details

Smartenough is designed to be cheap to use. We will push regular updates to select the cheapest model from the available providers that gets the job done. This means that you can use the best model for your needs without having to worry about the cost. Below are the current details for each provider:

| Provider | Model Name | Parameters | Quality Index | Pricing | License | Languages | Context Window | API Key | Docs |
|----------|------------|------------|---------------|---------|---------|-----------|----------------|---------|------|
| **OpenRouter** | Various free models [🔗](https://openrouter.ai/models?order=top-weekly&max_price=0) | 3-7B | ~50 | Free | 🆓 | 🌍 | ~32,000 | [Sign Up](https://www.openrouter.ai/) and set ```OPENROUTER_API_KEY``` |  [OpenRouter Docs](https://openrouter.ai/docs/quick-start) |
| **Mistral** | ```open-mistral-nemo-2407``` [🔗](https://mistral.ai/news/mistral-nemo/)  | 12B | 64 |$0.30/$0.30 |  🆓 | 🌍 | 128,000 | [Sign-Up](https://mistral.ai/news/la-plateforme/) and set ```MISTRAL_API_KEY``` | [Mistral Docs](https://docs.mistral.ai/) |
| **Meta** | ```llama-3.1-8b-instruct``` [🔗](https://ai.meta.com/blog/meta-llama-3-1/)  | 8B | 66 |$0.09/$0.09 | 🤝 | 🌍🌏 | 128,000 | [Sign Up](https://www.openrouter.ai/) and set ```OPENROUTER_API_KEY``` | [LLama 3.1 @ OpenRouter](https://openrouter.ai/models/meta-llama/llama-3.1-8b-instruct) |
| **OpenAI** | ```gpt-4o-mini``` [🔗](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/) | Est. 200B | 88 | $0.15/$0.60 |  🔒 | 🌍🌏 | 128,000 | [Sign Up](https://platform.openai.com/signup) and set  ```OPENAI_API_KEY``` | [OpenAI Docs](https://platform.openai.com/docs/guides/text-generation) |
| **Anthropic** | ```claude-3-haiku-20240307``` [🔗](https://www.anthropic.com/news/claude-3-haiku)  | Est. 20B | 74 | $0.25/$1.25 | 🔒 | 🌍🌏 | 200,000 | [Sign Up](https://console.anthropic.com/) and set ```ANTHROPIC_API_KEY``` | [Anthropic Docs](https://docs.anthropic.com/en/api/messages) |
| **Google** | ```gemini-1.5-flash``` [🔗](https://ai.google.dev/pricing)  | Est. 400B | 84 | $0.35/$1.05 | 🔒 | 🌍🌏🌎 | 1,048,576 | [Sign Up](https://ai.google.dev/gemini-api/docs/api-key) and set ```GOOGLE_API_KEY``` | [Google Docs](https://ai.google.dev/gemini-api/docs/text-generation?lang=python) |


- Quality Index is from [Artificial Analysis](https://artificialanalysis.ai/leaderboards/models) and is a rough estimate of the quality.
- Pricing is in USD per 1 Million Input/Output Tokens, it changes frequently so check the provider's website for the latest pricing.
- 🆓: Open Source License (Apache, MIT, etc.)
- 🤝: "Community" License (Fair Use, Research, etc.)
- 🔒: Proprietary License
- 🌍: Good at Indo-European Languages
- 🌏: Good at Sino-Tibetan Languages
- 🌎: Good at Other Languages

## Installation

You can install the package using pip:

```sh
pip install smartenough
```

### API Keys

Smartenough requires a valid API key for each provider you plan on using. To set up the API keys, follow these steps:

1. Obtain the necessary API keys from the following platforms (see table above) **Note that you only need to obtain API keys for the services you plan to use.**

2. Set the API keys as environment variables. You can do this by running the following commands in your terminal:

   ```sh
   export OPENAI_API_KEY="your_openai_api_key"
   export ANTHROPIC_API_KEY="your_anthropic_api_key"
   export MISTRAL_API_KEY="your_mistral_api_key"
   export GOOGLE_API_KEY="your_google_api_key"
   export OPENROUTER_API_KEY="your_openrouter_api_key"
   ```

   Replace ```your_openai_api_key```, ```your_anthropic_api_key```, ```your_mistral_api_key```, ```your_google_api_key```, and ```your_openrouter_api_key``` with your actual API keys.

For more information on setting up API keys, refer to the [OpenAI Platform Quickstart](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key) guide. The process is similar for all the mentioned services.


### Importing

```python
from smartenough import get_smart_answer 
```

### ```get_smart_answer```

smartenough has one main function, ```get_smart_answer``` that takes a question and returns an answer. The function has the following signature:

```python
get_smart_answer(instructions, additional_context="", model_provider="OpenRouter", validation=None):
```

The function takes the following arguments:
- ```instructions```: a string containing the question you want to ask
- ```additional_context```: a string containing additional context for the question (optional)
- ```model_provider```: a string specifying the model provider to use (default is "OpenRouter") you can also import the ```get_supported_providers``` function that'll return a list of supproted providers. As of this writing they are ```['Anthropic', 'OpenAI', 'Mistral', 'Meta', 'Google', 'OpenRouter', 'Random']``` where ```Random``` will randomly select a provider for you. (optional)
- ```validation```: if you are asking for output in a specific format, we'll validate ```json```, ```url``` (for a list of valid URLs), and ```html``` (for valid html) (optional)

## Example Usage

### Example 1: Ask a question and get an answer

Use the defaults and just ask a question, OpenRouter is the default provider

```python
>>> from smartenough import get_smart_answer
>>> get_smart_answer("In your opinion what are the most important news sources in the world?")
" As an AI, I don't have personal opinions, but based on relevance, reach, and credibility, important news sources in the world often include:\n\n1. BBC News - Recognized globally for comprehensive news coverage.\n2. CNN - Known for breaking news coverage, especially in the United States.\n3. Al Jazeera - Offers extensive news coverage, with a focus on Middle East and international news.\n4. The New York Times - Respected for in-depth reporting and analysis of domestic and international news.\n5. The Guardian - Known for in-depth investigative reporting, particularly on social issues and human rights.\n6. Reuters - Highly regarded for fast and accurate business and financial news.\n7. The Economist - Provides global economic and political analysis and commentary.\n\nThese are just a few among countless sources. For local news, consider sources relevant to your specific region such as your national or local newspapers, public broadcasters, and regional news outlets. Always remember to cross-verify information for accuracy."
```

### Example 2: Ask a question and get an answer in a format you like

```python
>>> from smartenough import get_smart_answer
>>> get_smart_answer("In your opinion what are the most important news sources in the world? Return only valid urls", validation="url")
['https://www.bbc.com/news', 'https://www.cnn.com/', 'https://www.nytimes.com/', 'https://www.theguardian.com/international', 'https://www.reuters.com/topics/world', 'https://apnews.com', 'https://www.washingtonpost.com/world/', 'https://www.nbcnews.com/news/world', 'https://www.wsj.com/worldnews']
```

### Example 3: Ask a question and get an answer from a specific provider

```python
>>> from smartenough import get_smart_answer
>>> get_smart_answer("write me a kid-friendly joke in Japanese", model_provider="Google")
'なんでパンダは白黒なの？ \n\n> なんで？\n\nだって、パンダは「パン」ダから「ダ」を取ると「パン」になるから！ \n\n(Why is a panda black and white? \n\n> Why?\n\nBecause if you take the "da" from "panda" you get "pan"!) \n'
```

### Example 4: Ask a question and add some additonal context for the model

```python
>>> from smartenough import get_smart_answer
>>> writing_sample = """ Welcome to the HYPE THREAD, a place to share your excitement about in-game achievements, brag about success, and get hyped for upcoming events. CAPS LOCK IS OPTIONAL IF IT HELPS YOU GET YOUR HYPE ON!
... 
... This is a chance to post about your successes. Our rules against self-promotion and most low-quality content, including shiny Pokemon pics, are relaxed in these threads--please talk all you like about your luck and accomplishments!
... 
... This thread is meant to be pretty positive, so please think twice before downvoting someone! Rude and negative comments will be removed -- please report them if you see them :D """
>>> 
>>> get_smart_answer("How old do you think the person was that wrote this?  Writing Sample:",additional_context=writing_sample)
' Based on the casual and enthusiastic tone of the writing sample, as well as the use of gaming terms like "achievements," "brag about success," and "in-game achievements," it\'s likely that the person who wrote this is a young person, possibly in their late teens or early 20s, who is passionate about gaming and enjoys engaging with a community of like-minded individuals.'
```

### Example 5: Everything all at once

```python
>>> from smartenough import get_smart_answer
>>> get_smart_answer("Translate this sentence to Hungarian and put it in a basic webpage, return only vaild html", additional_context="Hello World, welcome to Brad's Website!",model_provider="Anthropic",validation="html")
"""<html>
  <head>
  <title>Brad's Website</title>
  </head>
  <body>
    <h1>Szia Világ, üdvözlünk Brad weboldalán!</h1>
  </body>
</html>"""
```

### Example 6: Creating instant APIs

The ```smartenough``` package can be used to create a universal classifier API for various use cases. By leveraging the power of large language models, you can build an API that accepts input data and returns classified results based on the provided instructions.

Here's an example of how you can create a sentiment analysis API using ```smartenough```:

```python
from smartenough import get_smart_answer

def sentiment_analysis(text):
    instructions = f"""
    Classify the sentiment of the following text as 'positive', 'negative', or 'neutral'.
    Return the result in the following JSON format:
    {{
        "sentiment": "<sentiment_label>"
    }}

    Text: {text}
    """
    result = get_smart_answer(instructions, additional_context=text, validation="json")
    return result

# Example usage
text1 = "I absolutely love this product! It exceeded my expectations."
text2 = "The service was terrible. I won't be coming back."

print(sentiment_analysis(text1))
# Output: {"sentiment": "positive"}
print(sentiment_analysis(text2))
# Output: {"sentiment": "negative"}
```

In this example, the ```sentiment_analysis``` function takes a text input and constructs an instruction string that asks the model to classify the sentiment. The text input is provided as ```additional_context``` to give the model more information to work with. The desired output format is specified in the instructions using JSON.

The ```get_smart_answer``` function is called with the instructions, additional context, and the ```validation``` parameter set to ```"json"``` to ensure that the returned result is a valid JSON string. The classified result is then returned.

You can extend this concept to build APIs for various classification tasks such as topic classification, intent recognition, spam detection, and more. Simply modify the instructions and provide the appropriate input data to adapt it to your specific use case.

Here's another example of a topic classification API:

```python
from smartenough import get_smart_answer

def topic_classification(text):
    instructions = f"""
    Classify the topic of the following text into one of these categories: 'politics', 'sports', 'technology', 'entertainment', or 'other'.
    Return the result in the following JSON format:
    {{
        "topic": "<topic_label>"
    }}

    Text: {text}
    """
    result = get_smart_answer(instructions, additional_context=text, validation="json")
    return result

# Example usage
text1 = "The new smartphone model features a high-resolution camera and 5G connectivity."
text2 = "The actor won the prestigious award for their outstanding performance in the movie."

print(topic_classification(text1))
# Output: {"topic": "technology"}
print(topic_classification(text2))
# Output: {"topic": "entertainment"}
```

In this example, the ```topic_classification``` function takes a text input and constructs an instruction string that asks the model to classify the topic into predefined categories. The text input is provided as ```additional_context```, and the desired output format is specified using JSON.

Now, let's explore a more esoteric example - a dream interpretation API:

```python
from smartenough import get_smart_answer

def interpret_dream(dream_description):
    instructions = f"""
    Interpret the following dream description and provide insights into its potential symbolic meanings.
    Return the result in the following JSON format:
    {{
        "interpretation": "<dream_interpretation>",
        "key_symbols": ["<symbol1>", "<symbol2>", ...]
    }}

    Dream description: {dream_description}
    """
    result = get_smart_answer(instructions, additional_context=dream_description, validation="json")
    return result

# Example usage
dream = "I was flying high in the sky, soaring above the clouds. Suddenly, I found myself in a strange, surreal landscape filled with talking animals and peculiar objects."

print(interpret_dream(dream))
# Output:
# {
#     "interpretation": "Flying in dreams often symbolizes a sense of freedom, liberation, and transcendence. The strange, surreal landscape with talking animals and peculiar objects suggests a journey into the subconscious mind, where the dreamer encounters aspects of their psyche in symbolic form. The dream may represent a desire for escapism, a need to break free from limitations, or a quest for self-discovery and personal growth.",
#     "key_symbols": ["flying", "clouds", "strange landscape", "talking animals", "peculiar objects"]
# }
```

In this imaginative example, the ```interpret_dream``` function takes a dream description as input and constructs an instruction string that asks the model to interpret the dream and provide insights into its potential symbolic meanings. The dream description is provided as ```additional_context```, and the desired output format is specified using JSON, including the interpretation and key symbols found in the dream.

This example showcases how ```smartenough``` can be used to build APIs for more unconventional and creative use cases, leveraging the power of large language models to generate insightful and thought-provoking responses.

Feel free to let your imagination run wild and create APIs for various niche or esoteric domains using ```smartenough```. The possibilities are endless!

## Projects Using ```smartenough```

* [TranslateTribune](https://github.com/Medusa-Intelligence-Corp/TranslateTribune/)
* [LLMmMm](https://github.com/Medusa-Intelligence-Corp/LLMmMm)
* [DigitalPrejudice](https://codeberg.org/Medusa-Intelligence-Corp/DigitalPrejudice)

## Contributing

Feel free! Submit a PR! We are always looking for ways to improve the package.

## Frequently Asked Questions

**What about function calling?**

Some models allow for function calling, but not all, especially not all cheap ones. Check [this leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) for more detailed information on model capabilities.

**What about the latest cheap models?**

Smartenough should have the latest cheap models available within a day or so of their release. If a new model is missing, just ask and it will likely be added quickly!

**I want more features! I want to chat and write lots of code!**

This project is probably not the right fit for you then. You could try [LangChain](https://www.langchain.com/) for more advanced functionality, though we don't necessarily recommend it.

**I really need more control and customization**

We suggest reading through the smartenough source code, it's concise and won't take long. [View it on Codeberg](https://codeberg.org/Medusa-Intelligence-Corp/smartenough/src/branch/main/src/smartenough/llm.py). From there you can either fork and extend it, or use the underlying provider libraries directly.

**I need to use an old version of a smartenough dependency and am getting errors. What should I do?**

You can try installing the old package version you need, but be aware that smartenough only officially supports the latest versions. Our focus is on integrating good cheap models quickly. To use old dependency versions, install smartenough with ```pip install --no-dependencies smartenough```, then separately install the old package version you need, e.g. ```pip install openai==1.8.0```. Use this workaround at your own risk.


