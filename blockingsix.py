import asyncio
import time
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


async def get_balance() -> str:
    try:
        await asyncio.sleep(1)
        return "Available balance: INR 25,000"
    finally:
        print("Balance: cleanup")


def blocking_transaction_history() -> str:
    print("Worker: started")
    time.sleep(5)  # Blocks the worker thread.
    print("Worker: finished AFTER cancellation")
    return "Last transaction: INR 500 debit"


async def get_transaction_history() -> str:
    try:
        return await asyncio.to_thread(blocking_transaction_history)
    finally:
        print("Transactions: coroutine cleanup")


async def run_tool(
    name: str,
    operation: Awaitable[str],
    timeout_seconds: float,
) -> Success | Timedout:
    try:
        async with asyncio.timeout(timeout_seconds):
            data = await operation
            return Success(tool=name, data=data)
    except TimeoutError:
        return Timedout(tool=name, timedout=timeout_seconds)


async def main():
    started = perf_counter()

    tasks = {
        asyncio.create_task(
            run_tool("Balance", get_balance(), 2)
        ): "Balance",
        asyncio.create_task(
            run_tool("Transaction History", get_transaction_history(), 4)
        ): "Transaction History",
    }

    try:
        done, pending = await asyncio.wait(tasks, timeout=2)
    finally:
        # Also runs when the caller cancels main().
        for task in tasks:
            if not task.done():
                task.cancel()

        # Wait for coroutine cleanup.
        await asyncio.gather(*tasks, return_exceptions=True)

    # Caller cancellation propagates before reaching this section.
    for task, name in tasks.items():
        if task in done:
            print(task.result())
        else:
            print(DeadlineExceeded(tool=name))

    print(f"Elapsed: {perf_counter() - started:.1f}s")


async def test_caller_cancellation():
    request = asyncio.create_task(main())

    await asyncio.sleep(0.2)
    print("Caller: cancelling request")
    request.cancel()

    try:
        await request
    except asyncio.CancelledError:
        print("Caller: cancellation propagated")
    else:
        raise AssertionError("Request did not propagate cancellation")

    assert request.cancelled()


if __name__ == "__main__":
    asyncio.run(test_caller_cancellation())

