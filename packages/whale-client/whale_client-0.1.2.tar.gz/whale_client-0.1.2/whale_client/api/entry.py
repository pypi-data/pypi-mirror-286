import json
from typing import Optional
import requests
from dotenv import load_dotenv

import os

import logging

from whale_client.models.api.entry import PostApplicationRequest, PostApplicationResponse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


load_dotenv()
BASE_URL = os.getenv("BACKEND_ENDPOINT")
SERVICE_ENDPOINT = "application"


def post_application(input: PostApplicationRequest) -> Optional[PostApplicationResponse]:
    try:
        response = requests.post(
            f"{BASE_URL}/{SERVICE_ENDPOINT}", json=input.model_dump()
        )
        response.raise_for_status()
        application_response = PostApplicationResponse.model_validate(json.loads(response.text))
        return application_response
    except TypeError as e:
        log.error(
            f"Failed to parse the response id of application from server: {e}"
        )
        return None
    except requests.RequestException as e:
        log.error(f"Failed to fetch response for application: {e}")
        return None
    except Exception as e:
        log.error(f"Unknown error for posting of application occurred: {e}")
        return None
