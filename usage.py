import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi_bgtasks_dashboard import mount_bg_tasks_dashboard
import httpx

app = FastAPI()

# Add dashboard for background tasks
mount_bg_tasks_dashboard(app=app)

def simple_task(name: str):
    import time
    print(f"Started task for {name}")
    time.sleep(20)
    print(f"Finished task for {name}")



# The inner async function that fetches data from an external service
async def _fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()  # Non-blocking request

# The FastAPI endpoint that calls the inner function
@app.get("/call_other_service")
async def call_other_service():
    data = await _fetch()  # Call the async inner function
    return data
# Synchronous function for CPU-intensive computation
def _factorize(n: int):
    """Return the prime factors of n using trial division."""
    factors = []
    divisor = 2

    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1

    if n > 1:
        factors.append(n)

    return factors

@app.get("/factorize")
async def factorize(n: int):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, _factorize, n)
    return {"number": n, "factors": result}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/hello/{name}")
async def say_hello(name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(simple_task, name)
    return {"message": f"Hello {name}, task started in background!"}
