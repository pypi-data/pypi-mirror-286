import os
import google.generativeai as genai
from llms.logger import logger


genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


model = genai.GenerativeModel(model_name="gemini-pro")


def gemini_generate(message="Hello how are you?"):
    """
        Generate text using Google's models.

        Parameters:

        message: string- for prompting, default="Hello how are you?"]


        Output: Dict containing
    response_text: str, the generated text

    input_tokens: int, the number of tokens in the input

    output_tokens: int, the number of tokens in the output

    estimated_cost: float, the estimated cost of the generation
    """
    response = model.generate_content(message)
    logger.info(f"Generating text using Google gemini model for prompt: {message}")

    response_text = response.text
    logger.info(f"Generated text: {response_text}")

    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    estimated_cost = 0.0

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": estimated_cost,
        "response": response_text,
    }
