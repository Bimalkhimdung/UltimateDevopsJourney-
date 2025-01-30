import aiohttp
import asyncio
import logging

# get zone id from 
#curl -X GET "https://api.cloudflare.com/client/v4/zones" \
#    -H "Authorization: Bearer API KEY " \
#    -H "Content-Type:application/json"

CLOUDFLARE_API_TOKEN = "api token form cloudflare"
CLOUDFLARE_ZONE_ID = "zone id"  
CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cloudflare_setup.log"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

async def create_dns_record():
    """Create an A record in Cloudflare"""
    data = {
        "type": "A",
        "name": "sub domain name",  
        "content": "public ip",  
        "ttl": 120,
        "proxied": True
    }

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(CLOUDFLARE_API_URL, json=data, headers=headers) as response:
                response_data = await response.json()
                logger.info(f"Cloudflare Response: {response.status} - {response_data}")

                if response.status == 200 and response_data.get("success"):
                    logger.info("DNS Record created successfully!")
                else:
                    logger.error(f"Failed to create DNS record: {response_data}")

        except Exception as e:
            logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(create_dns_record())
