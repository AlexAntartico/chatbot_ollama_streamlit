import streamlit as st
import requests


DEEPINFRA_API_URL = "https://api.deepinfra.com/v1/chat/completions"


def get_deepinfra_response(messages, model):
    """
    Sends a request to the DeepInfra API and returns the response.

    Args:
        messages (list): A list of message dictionaries for conversation history.
        model (str): The name of the model to use for the completion.

    Returns:
        str: The content of the assistant's response message.
    """
    try:
        api_key = st.secrets["DEEPINFRA_API_KEY"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Use the model passed as an argument in the payload
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }

        response = requests.post(DEEPINFRA_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred with the API request: {e}")
        return "Sorry, I couldn't connect to the DeepInfra service."
    except KeyError:
        st.error("DeepInfra API key not found. Please add it to your Streamlit secrets.")
        return "API key is missing."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."

