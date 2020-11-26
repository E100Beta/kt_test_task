import asyncio
import uvloop
import worker.worker

# For consistency with server import paths
uvloop.install()
asyncio.run(worker.worker.setup_task())
