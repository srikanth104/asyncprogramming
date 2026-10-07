import asyncio
import time

async def investigate():
    print("Investigation started")
    await asyncio.sleep(1) # This is in seconds 
    print("Investigation finished")

async def main():
    result = investigate()  #Coroutine is created but not awaited
    print("Request received")
    await result # It executes the

#asyncio.run(main1())

async def main2():
    result = await investigate()  
    print(result) # Results printed is none
    print("Request Completed")

#asyncio.run(main2())

async def main3():
    print("Request received")
    await investigate()

#asyncio.run(main3())

async def main4():
    print("Request received")
    investigate()
    print("Request Completed")

#asyncio.run(main4())

async def main5():
    await investigate()
    await investigate()

# asyncio.run(main5())

#  Investigation started
# Investigation finished
# Investigation started
# Investigation finished


# main() waits for the first investigation to finish before proceeding.
# During await asyncio.sleep(1), the event loop can run other ready tasks. We haven’t scheduled a second investigation as a separate task here.


async def main6():
    task1 = asyncio.create_task(investigate())
    task2 = asyncio.create_task(investigate())
    await task1
    await task2

#asyncio.run(main6())


async def investigate2(name : str):
    print(f"{name}: started")
    time.sleep(1) # This is in seconds 
    print(f"{name}: finished")


async def main7():
    start = time.perf_counter()
    task1 = asyncio.create_task(investigate2("Investigation 1"))
    task2 = asyncio.create_task(investigate2("Investigation 2"))
    await task1
    await task2
    print(f"Elapsed: {time.perf_counter() - start:.2f} seconds")

#asyncio.run(main7())

# Investigation 1: started
# Investigation 1: finished
# Investigation 2: started
# Investigation 2: finished
# Elapsed: 2.00 seconds

# time.sleep() is a blocking call, which means it blocks the event loop and 
# prevents other tasks from running concurrently. As a result, 
# the second investigation cannot start until the first one finishes, 
# leading to a total elapsed time of 2 seconds.

# One precision that matters: await is a potential suspension point,
# not a guaranteed task switch. If the awaited operation completes immediately,
# execution can continue without yielding to another task. 
# asyncio.sleep() explicitly suspends the current task

async def imeediate():
    return 42

async def main8():
    result = await imeediate()
    print(result)

#asyncio.run(main8())

# await asyncio.sleep(0) suspends the current task and yields control
# to the event loop, allowing other ready tasks or callbacks to run.
# It introduces no intentional timed delay.

async def wait_for_response(start):
    print(f"{time.perf_counter() - start:.1f}s: Request sent")

    await asyncio.sleep(3)

    print(f"{time.perf_counter() - start:.1f}s: Response processed")

async def blocking_work(start):
    print(f"{time.perf_counter() - start:.1f}s: Blocking work started")
    #time.sleep(5) 
    # It completes the task in 8 seconds, it will improve the user experience if time.sleep(5)
    #await asyncio.sleep(5) # Simulates occupying the event-loop thread

    await asyncio.to_thread(time.sleep, 5)
    # Wait for its completion while allowing the event loop to run other tasks

    print(f"{time.perf_counter() - start:.1f}s: Blocking work finished")

async def main10():
    start = time.perf_counter()

    response_task = asyncio.create_task(wait_for_response(start))
    work_task = asyncio.create_task(blocking_work(start))

    await response_task
    await work_task

asyncio.run(main10())

# await.sleep(5)  completes in 5 seconds both calls  


# A worker thread is a separate thread in your application’s process that executes work assigned to it.
# In our example, there are two threads with different responsibilities:
# Thread	                    Responsibility
# Event-loop            thread	Runs your async tasks and handles their suspension and resumption
# Worker thread	        Executes the blocking function passed to to_thread()

# “Worker” describes the thread’s job; it isn’t a special kind of Python thread.
# The default executor uses a pool of threads that can be reused across calls, 
# rather than necessarily creating a new thread for each operation.

# Also, a task and a thread are different: create_task() schedules a coroutine on 
# the event loop; to_thread() moves a function’s execution to a separate thread.

