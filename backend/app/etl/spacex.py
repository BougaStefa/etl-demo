import httpx
import logging
from datetime import datetime
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class SpaceXAPI:
    BASE_URL = "https://api.spacexdata.com/v4"
    
    def __init__(self):
        self.client = httpx.Client(timeout=30.0)
    
    def __del__(self):
        self.client.close()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_launches(self) -> List[Dict[Any, Any]]:
        try:
            response = self.client.get(f"{self.BASE_URL}/launches")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching launches: {str(e)}")
            raise
