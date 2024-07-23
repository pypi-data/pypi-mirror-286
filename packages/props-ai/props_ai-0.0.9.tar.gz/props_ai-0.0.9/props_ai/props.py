import requests
from typing import Dict, Any, Optional
import logging

class PropsAI:
    def __init__(self, api_key: str, providers_keys: Optional[Dict[str, Optional[str]]] = None):
        self.api_key = api_key
        self.base_url = "https://props-api.propsai.workers.dev/"
        self.providers_keys = providers_keys or {
            "openai": None,
            "groq": None,
            "anthropic": None,
            "google": None,
        }

    def generate_headers(
        self,
        api_key: Optional[str] = None,
        provider: str = "openai",
        metadata: Optional[Dict[str, str]] = None,
        session_id: Optional[str] = None,
        experiment_id: Optional[str] = None
    ) -> Dict[str, str]:
        headers = {
            "x-props-key": api_key or self.api_key,
            "x-props-provider": provider
        }
        
        if metadata:
            headers["x-props-metadata"] = str(metadata)
        
        if session_id:
            headers["x-props-session-id"] = session_id
        
        if experiment_id:
            headers["x-props-experiment-id"] = experiment_id
        
        for provider_key, key in self.providers_keys.items():
            if key:
                headers[f"x-props-{provider_key}-key"] = key

        return headers

    def send_feedback(
        self,
        experiment_id: str,
        context_id: str,
        metric_id: str,
        value: str
    ) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        for provider, key in self.providers_keys.items():
            if key:
                headers[f"x-props-{provider}-key"] = key

        data = {
            "experimentId": experiment_id,
            "contextId": context_id,
            "metricId": metric_id,
            "value": value,
        }

        try:
            response = requests.post(f"{self.base_url}/experiments/{experiment_id}/feedback", headers=headers, json=data)
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "response_text": response.text,
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending feedback: {e}")
            return {
                "status_code": 500,
                "response_text": str(e),
            }

# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    props_ai = PropsAI(
        api_key="api_key",
        providers_keys={
            "openai": "<TEST_PYTHON_SDK_OPENAI_KEY>",
            "groq": "<TEST_PYTHON_SDK_GROQ_KEY>",
            "anthropic": "<TEST_PYTHON_SDK_ANTHROPIC_KEY>",
            "google": "<TEST_PYTHON_SDK_GOOGLE_KEY>",
        }
    )

    headers = props_ai.generate_headers(
        api_key="api_key",
        provider="openai",
        metadata={"user": "test_user"},
        session_id="test_session_id"
    )
    print(f"Generated headers: {headers}")

    post_response = props_ai.send_feedback(
        experiment_id="<TEST_PYTHON_SDK_EXPERIMENT_ID>",
        context_id="<TEST_PYTHON_SDK_CONTEXT_ID>",
        metric_id="metricIdTest",
        value="feedbackValueTest"
    )
    
    print(f"POST response status: {post_response['status_code']}")
    print(f"POST response body: {post_response['response_text']}")
