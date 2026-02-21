import os
import httpx
import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://athena-core:8000/api/v1/webhook/event")

async def dispatch_webhook(event_type: str, entity_type: str, entity_id: str, changed_fields: Dict[str, Any], source: str = "system", metadata: Optional[Dict[str, Any]] = None):
    # Prepare payload according to FR-01.6 and 8.1
    import uuid
    from datetime import datetime

    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "changed_fields": changed_fields,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": source,
    }
    if metadata:
        payload["metadata"] = metadata

    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Firing webhook to {WEBHOOK_URL} for {entity_type} {entity_id}")
            # Retry policy 3 retries (1s, 2s, 4s) could be added here
            response = await client.post(WEBHOOK_URL, json=payload, timeout=10.0)
            response.raise_for_status()
            logger.info(f"Webhook delivered: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to dispatch webhook to {WEBHOOK_URL}: {e}")
