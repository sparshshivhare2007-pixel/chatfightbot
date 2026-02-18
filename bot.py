import uvloop
import asyncio
from core.app import create_app

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == "__main__":
    app = create_app()
    app.run()
