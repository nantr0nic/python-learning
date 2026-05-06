import asyncio
import time


async def greet_after_delay(name):
    print(f"Starting {name}...")
    await asyncio.sleep(2)
    print(f"Hello, {name}!")


async def fetch_number(n):
    print("Fetching a number")
    await asyncio.sleep(1)
    return n * 10


async def main():
    start = time.perf_counter()

    await asyncio.gather(
        greet_after_delay("Alice"),
        greet_after_delay("Andy"),
        greet_after_delay("Dennis the Cat"),
    )

    results = await asyncio.gather(
        fetch_number(1),
        fetch_number(2),
        fetch_number(3),
    )
    print(results)

    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.2f} seconds")


asyncio.run(main())
