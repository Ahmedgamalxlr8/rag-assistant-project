import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Read backend URL from environment variable per rubric rules
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

class BackendAPIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def check_health(self) -> dict:
        """Verifies backend connectivity and indexed chunks count."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "unreachable", "error": str(e)}

    def send_query(self, question: str) -> dict:
        """Sends user question to POST /query endpoint."""
        try:
            response = requests.post(
                f"{self.base_url}/query",
                json={"question": question},
                timeout=60
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Cannot reach backend server. Please verify FastAPI is running on port 8000."
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "The request timed out while generating an answer. Please try again."
            }
        except requests.RequestException as e:
            return {"success": False, "error": f"API error: {str(e)}"}

api_client = BackendAPIClient()