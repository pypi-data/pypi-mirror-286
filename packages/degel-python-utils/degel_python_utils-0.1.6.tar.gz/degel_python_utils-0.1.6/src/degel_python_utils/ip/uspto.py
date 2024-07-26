"""
USPTO patent API
"""

import asyncio
import httpx

from ..sys_utils.errors import ExternalApiError
from ..sys_utils.log_tools import setup_logger

logger = setup_logger(__name__)


async def fetch_us_patent_application_from_uspto_api(
    application_number: str, kind_code: str = "A1"
) -> dict[str, str]:
    """
    Fetches a US patent application from the USPTO API.

    :param application_number: The patent number to fetch.
    :param kind_code: The kind code of the patent, default is "A1".
    :return: A dictionary containing the patent application details.
    :raises ExternalApiError: If the USPTO API request fails.
    """
    params = {"publicationDocumentIdentifier": f"US{application_number}{kind_code}"}
    return await fetch_from_uspto_api("publications", params)


async def fetch_us_patent_grant_from_uspto_api(patent_number: str) -> dict[str, str]:
    """
    Fetches a granted US patent from the USPTO API.

    :param patent_number: The patent number to fetch.
    :return: A dictionary containing the patent grant details.
    :raises ExternalApiError: If the USPTO API request fails.
    """
    params = {"patentNumber": patent_number}
    return await fetch_from_uspto_api("grants", params)


async def fetch_from_uspto_api(
    endpoint: str, params: dict, num_retries: int = 5
) -> dict[str, str]:
    """
    Helper function to fetch data from the USPTO API with retry logic.

    :param endpoint: The API endpoint to call.
    :param params: The parameters to pass to the API call.
    :return: A dictionary containing the response data.
    :raises ExternalApiError: If the USPTO API request fails.
    """
    base_url = f"https://developer.uspto.gov/ibd-api/v1/application/{endpoint}"

    async with httpx.AsyncClient() as client:
        for attempt in range(num_retries):
            try:
                response = await client.get(base_url, params=params, timeout=60)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as err:
                logger.error(f"RequestException occurred: {err}")
                raise ExternalApiError(
                    f"USPTO API request to {base_url} failed: {str(err)}"
                ) from err
            except httpx.HTTPStatusError as err:
                if err.response.status_code in [429]:
                    backoff_time = 2**attempt
                    logger.warning(
                        f"USPTO API request to {base_url} got"
                        f"status code {err.response.status_code}. "
                        f"Retrying in {backoff_time} seconds..."
                    )
                    await asyncio.sleep(backoff_time)
                else:
                    raise ExternalApiError(
                        f"USPTO API request to {base_url} failed with status "
                        f"code {err.response.status_code}"
                    ) from err
        raise ExternalApiError(
            f"USPTO API request to {base_url} failed after 5 attempts"
        )
