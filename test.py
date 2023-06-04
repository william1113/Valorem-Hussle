import asyncio

async def print_B(): #Simple async def
    print("B")

async def main_def():
    print("A")
    await asyncio.gather(print_B())
    print("C")
asyncio.run(main_def())