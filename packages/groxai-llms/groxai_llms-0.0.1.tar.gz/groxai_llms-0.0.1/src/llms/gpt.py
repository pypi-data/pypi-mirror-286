from openai import OpenAI
import os
from llms.logger import logger


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


pricing_details = {
    "gpt-4o": {
        "input_token_price": 5.00 / 1_000_000,
        "output_token_price": 15.00 / 1_000_000,
    },
    "gpt-4o-mini": {
        "input_token_price": 0.150 / 1_000_000,
        "output_token_price": 0.600 / 1_000_000,
    },
    "gpt-4-turbo": {
        "input_token_price": 10.00 / 1_000_000,
        "output_token_price": 30.00 / 1_000_000,
    },
    "gpt-4": {
        "input_token_price": 30.00 / 1_000_000,
        "output_token_price": 60.00 / 1_000_000,
    },
    "gpt-4-32k": {
        "input_token_price": 60.00 / 1_000_000,
        "output_token_price": 120.00 / 1_000_000,
    },
    "gpt-3.5-turbo": {
        "input_token_price": 0.50 / 1_000_000,
        "output_token_price": 1.50 / 1_000_000,
    },
}


def estimate_cost(input_tokens, output_tokens, model_name):
    """
    Estimate the cost of a GPT API call based on the number of input and output tokens.

    Parameters:
    input_tokens (int): Number of input tokens used.
    output_tokens (int): Number of output tokens generated.
    model_name (str): The model name to be used for pricing.

    Returns:
    float: Estimated cost of the API call in dollars.
    """
    pricing = pricing_details.get(model_name)
    if not pricing:
        raise ValueError(f"Pricing details for model '{model_name}' not found.")

    input_token_cost = pricing["input_token_price"]
    output_token_cost = pricing["output_token_price"]

    total_cost = (input_tokens * input_token_cost) + (output_tokens * output_token_cost)
    return total_cost


def gpt_generate(
    model="gpt-4o-mini",
    message_history=[{"role": "system", "content": "You are an polite assitant"}],
    temperature=0.5,
):
    """_summary_
    Generate text using OpenAI's models.

    Parameters:
    model: str, default="gpt-4o-mini", the model to use for text generation
    available models= gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo, gpt-4

    message_history: list of dict- for prompting, default=[{'role': 'system', 'content': 'You are an polite assitant'}]

    temperature: float, default=0.5, the randomness of the generated text


    Output: Dict containing
    response_text: str, the generated text

    input_tokens: int, the number of tokens in the input

    output_tokens: int, the number of tokens in the output

    estimated_cost: float, the estimated cost of the generation

    """
    logger.info(
        f"Generating text using Openai model '{model}' with temperature '{temperature}' for prompt: {message_history}"
    )

    response = client.chat.completions.create(
        model=model, messages=message_history, n=1, stop=None, temperature=temperature
    )

    response_text = response.choices[0].message.content

    logger.info(f"Generated text: {response_text}")

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.total_tokens

    estimated_cost = estimate_cost(input_tokens, output_tokens, model_name=model)

    logger.info(f"Estimated cost of generation: ${estimated_cost}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": estimated_cost,
        "response": response_text,
    }
