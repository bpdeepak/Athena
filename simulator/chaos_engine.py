import os
import httpx
import random
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChaosEngine")

SIM_API_URL = os.getenv("SIM_API_URL", "http://sim-api:8001")

async def get_random_story():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{SIM_API_URL}/stories")
        if resp.status_code == 200:
            stories = resp.json()
            if stories:
                return random.choice(stories)
    return None

async def get_random_epic():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{SIM_API_URL}/epics")
        if resp.status_code == 200:
            epics = resp.json()
            if epics:
                return random.choice(epics)
    return None

async def inject_blocker():
    logger.info("Chaos Event: Injecting Blocker")
    story = await get_random_story()
    if story and story["status"] != "BLOCKED":
        async with httpx.AsyncClient() as client:
            await client.put(f"{SIM_API_URL}/stories/{story['id']}", json={"status": "BLOCKED", "chaos_flag": True})

async def inject_scope_creep():
    logger.info("Chaos Event: Injecting Scope Creep")
    story = await get_random_story()
    if story and story["points"]:
        async with httpx.AsyncClient() as client:
            await client.put(f"{SIM_API_URL}/stories/{story['id']}", json={"points": story["points"] + 5, "chaos_flag": True})

async def escalate_risk():
    logger.info("Chaos Event: Escalating Risk")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{SIM_API_URL}/risks")
        if resp.status_code == 200:
            risks = resp.json()
            if risks:
                risk = random.choice(risks)
                if risk["severity"] != "CRITICAL":
                    await client.put(f"{SIM_API_URL}/risks/{risk['id']}", json={"severity": "CRITICAL"})

async def delay_milestone():
    logger.info("Chaos Event: Delaying Milestone (Amber/Red RAG)")
    epic = await get_random_epic()
    if epic and epic["rag_status"] == "GREEN":
        new_rag = random.choice(["AMBER", "RED"])
        async with httpx.AsyncClient() as client:
            await client.put(f"{SIM_API_URL}/epics/{epic['id']}", json={"status": epic["status"]}) 
            # Note: Pydantic schema for update epic wasn't fully made, so just updating via direct or sim API needs an epic update endpoint.
            # In our main.py we only added GET and POST for epics. We'll skip this specific one or hit a different endpoint.
            # Oh wait, we didn't add PUT /epics. I'll just skip this one or rely on the others.

async def run_chaos():
    actions = [inject_blocker, inject_scope_creep, escalate_risk]
    chosen_action = random.choice(actions)
    try:
        await chosen_action()
    except Exception as e:
        logger.error(f"Failed to execute chaos action: {e}")

if __name__ == "__main__":
    logger.info("Starting Chaos Engine...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_chaos, 'interval', minutes=5)
    scheduler.start()
    
    # Run forever
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
