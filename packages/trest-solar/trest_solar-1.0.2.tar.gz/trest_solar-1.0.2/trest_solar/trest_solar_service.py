import json 

import aiohttp 
from trest_identity import TrestIdentityService
from .solar_profile import SolarHistory

class CloudSolarTrestService:
    """The class representing the Api of the Cloud Solar Trest application."""

    def __init__(self, username: str, password: str) -> None:
        """Init the class."""
        self.base_url = "https://cloud.solar.trest.se:443"
        self.trest_identity_service = TrestIdentityService(username, password)

    async def get_latest_solar_history_async(self) -> SolarHistory:
        """Get the latest solar history from the Api."""
        await self.trest_identity_service.renew_token_async()

        headers = {"X-Token": self.trest_identity_service.token}

        async with aiohttp.ClientSession() as session, session.get(
            self.base_url + "/api/v1/solar/getlatesthistory",
            headers=headers,
            timeout=3,
        ) as response:
            response_text = await response.text()

            return SolarHistory(json.loads(response_text))
