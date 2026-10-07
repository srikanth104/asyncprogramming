import asyncio

async def fetch_customer():
    print("Lookup started")

    try:
        await asyncio.sleep(5)
        print("Lookup finished")
        return {"customer_id": "C101"}

    except asyncio.CancelledError:
        print("Lookup received cancellation")
        raise  # Propagate cancellation; don't swallow it
        #return {"customer_id": "C101"}
        
    finally:
        print("Cleanup runs here")

async def main():
    try:
        async with asyncio.timeout(2):
            customer = await fetch_customer()
            print(customer)

    except TimeoutError:
        print("Caller received TimeoutError")

asyncio.run(main())

# When timeout is set to 5 seconds, the fetch_customer set 5

# Lookup started
# Lookup received cancellation
# Cleanup runs here
# Caller received TimeoutError

# When timeout is set to 7 seconds, the fetch_customer set 5
# Lookup started
# Lookup finished
# Cleanup runs here
# {'customer_id': 'C101'}

# The timeout context converts the cancellation it initiated into TimeoutError.
# Python recommends using try/finally for cleanup and generally propagating CancelledError 
# if you catch it. docs.python.org
# Here we catch cancellation only to make it visible. If you only need cleanup, try/finally 
# is enough. The print statement represents cleanup; this example doesn’t hold actual 
# resources.



# except prints "Lookup received cancellation".
# raise starts re-raising CancelledError.
# Before the coroutine exits, finally prints "Cleanup runs here".
# CancelledError propagates out of fetch_customer().
# The timeout context converts it into TimeoutError.
# The caller prints "Caller received TimeoutError".