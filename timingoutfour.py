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

    results = await asyncio.gather(
        run_tool("Balance", get_balnce(), 2), 
        run_tool("Transaction History", get_transaction_history(), 2),)

    for result in results:
        print(result)

    print(f"Elapsed: {perf_counter() - started:.1f}s")

asyncio.run(main())

# Let’s focus only on when each tool starts.
# These are two different numbers in the code:
# await asyncio.sleep(1)               # Balance takes 1 secondasyncio.timeout(2)                   # Allow up to 2 seconds


# Balance does not wait for 2 seconds. It needs only 1 second.
# Here is the execution:
# 1. Balance starts. It reaches await asyncio.sleep(1) and pauses. The event loop can now run another task.
# 2. Transactions starts immediately afterward. It reaches await asyncio.sleep(5) and pauses.
# 3. Both are now waiting. Their waiting periods overlap.
# 4. After 1 second, balance resumes and returns Success.
# 5. After 2 seconds from starting, transactions reaches its timeout. Cleanup runs, and its wrapper returns TimedOut.
# Think of placing two food orders together:
# - One dish is ready after 1 minute.
# - The other takes 5 minutes, but you cancel that order after 2 minutes.
# - You still keep the first dish.
# The key correction to your explanation: transactions starts when balance pauses at await, not after balance’s 2-second timeout.


# To get both balances 
# reduce the timeout for transactions to 1 second.
# and increase the timeout for balance to 3 seconds.


# operation: Awaitable[str]
#means: “Pass an awaitable whose result is expected to be a str.”



# It is not deep immutability. 
# If a frozen dataclass contains a list, 
# the list can still be modified; frozen=True
# prevents reassigning the field, not modifying the object stored in it.


# Success | TimedOut | DeadlineExceeded | ToolFailed
# we can add more but issue with readablity 