import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from time import perf_counter

@dataclass(frozen=True)
class Success:
    tool: str
    data: str

@dataclass(frozen=True)
class Timedout:
    tool: str
    timedout: float

@dataclass(frozen=True)
class DeadlineExceeded:
    tool: str

async def get_balnce() -> str:
    await asyncio.sleep(1)
    return "Available balance: INR 25,000"

async def get_transaction_history() -> str:
    try: 
        await asyncio.sleep(5)
        return "Last transaction: INR 500 debit"
    finally:   
        print("Transactions: cleanup")

async def run_tool(
        name: str,
        operation: Awaitable[str],
        timeout_seconds: float
) -> Success | Timedout :
    try:
        async with asyncio.timeout(timeout_seconds):
            data = await operation
            return Success(name, data)
    except asyncio.TimeoutError:
        return Timedout(tool = name,
                        timedout = timeout_seconds)

async def main():
    started = perf_counter()

    tasks = {
        asyncio.create_task(run_tool("Balance", get_balnce(), 2)): "Balance",
        asyncio.create_task(run_tool("Transaction History", get_transaction_history(), 4)): "Transaction",
    }

    try: 
        done, pending = await asyncio.wait(tasks.keys(), timeout=2)
    finally:
        for task in tasks :
            if not task.done():
                task.cancel()

        await asyncio.gather(*tasks.keys(), return_exceptions=True)

    for task, name in tasks.items():
        if task in done:
            print(task.result())
        else:
            print(DeadlineExceeded(tool=name))

    print(f"Elapsed: {perf_counter() - started:.1f}s")

asyncio.run(main())