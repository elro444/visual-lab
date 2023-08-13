import time
import asyncio

def real_fetch_data_single():
    print("Starting to fetch...")
    # "Busy" IO
    time.sleep(5)
    print("Fetch finished!")

async def fetch_data_periodic():
    loop = asyncio.get_event_loop()

    while True:
        await loop.run_in_executor(None, real_fetch_data_single)
        await asyncio.sleep(5)
