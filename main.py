import os
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def _home(r):
 return web.json_response({"Hello": "World from aioHTTP"}, content_type="application/json", status=200)

async def _exec(code: str):
  process = await asyncio.create_subprocess_shell(
        code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
  stdout, stderr = await process.communicate()
  return stdout.decode().strip(), stderr.decode().strip()

@routes.get("/shell")
async def _shell(r):
 try:
   code = r.rel_url.query["code"]
 except:
   code = "echo 'No Code Provided'"
 out, err = await _exec(code)
 resp = {"result": {"stdout": str(out), "stderr": str(err)}}
 return web.json_response(resp, content_type="application/json", status=200)

async def start_server():
    port = int(os.environ.get("PORT"))
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()


# Server Startup
asyncio.get_event_loop().run_until_complete(start_server())
print("Web Server Started.")
