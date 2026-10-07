import asyncio
import time

async def fetch_customer():
    await asyncio.sleep(1)  # Simulate a slow dependency
    return {"customer_id": "C101"}

async def main():
    start = time.perf_counter()

    try:
        async with asyncio.timeout(2):
            customer = await fetch_customer()
            print(customer)

    except TimeoutError:
        print("Customer lookup timed out")

    print(f"Elapsed: {time.perf_counter() - start:.1f}s")

asyncio.run(main())

# Lookup duration	        Timeout	Expected outcome
# 1 second	2 seconds	Customer returned after ~1 second
# 5 seconds	2 seconds	TimeoutError after ~2 seconds
