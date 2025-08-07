# Copyright (c) 2025- MAGO

import json
import requests
from typing import Optional
from pydantic import BaseModel, Field

from .config import PRODUCTION_URL, TIMEOUT
from .core.logs import get_logger
from .helper.utils import get_media_type

logger = get_logger(__name__)

class BaseAudionConfig(BaseModel):
    api_key: str = Field(..., description="The API key of the server")
    base_url: str = Field(default=PRODUCTION_URL, description="The base URL of the server")
    timeout: int = Field(default=TIMEOUT, description="The timeout of the server")


class BaseAudionClient(BaseAudionConfig):
    """
    Base class for all Audion clients.
    """
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        # Use default values if None is provided
        base_url = base_url or PRODUCTION_URL
        timeout = timeout or TIMEOUT

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )
        logger.info(f"Initialized Audion client with base URL: {self.base_url}")

    def flow(
        self,
        flow: str,
        input_type: str,
        input: str,
    ):
        """
        Call the API with the given flow, input type, and input.

        Args:
            flow: The flow to call.
            input_type: The type of the input.
            input: The input to the flow.
        """
        # Set Authorization header with api_key
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        # Define url
        url = f"{self.base_url}/flow"
        print(url)

        response = None
        try:
            # If input is a file, upload the file to the server
            if input_type == "file":
                logger.info(f"Uploading file: {input}")
                media_type = get_media_type(input)
                print(media_type, input)

                response = requests.post(
                    url,
                    headers=headers,
                    data={
                        "flow": flow,
                        "input_type": input_type,
                        "input": input,
                    },
                    files={
                        "file": (input, open(input, "rb"), media_type)
                    },
                )
                print(response.json())
            elif input_type == "url":
                response = requests.post(
                    url,
                    headers=headers,
                    data={
                        "flow": flow,
                        "input_type": input_type,
                        "input": input,
                    },
                )
            else:
                raise ValueError(f"Unsupported input type: {input_type}")

            if response and response.status_code != 200:
                # Save the response to a file
                with open("rsp.json", "w") as f:
                    json.dump(response.json(), f)

            return response.json() if response else None
        except Exception as e:
            logger.error(f"Failed to call the API: {e}")
            raise e
            
