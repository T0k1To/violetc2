import aiohttp
from json import dumps, loads
from sys import exit
from aiohttp import web
from handler.persist_data import Agents
from menus.utils import *

agentsDatabase = Agents()

class C2Server:
	async def agentList(request):
		agents = agentsDatabase.loadAgents()

		return web.json_response(data = agents)

	async def webSocket(request):
		Print.good("Starting websocket")

		# Open websocket
		ws = web.WebSocketResponse()

		# Prepare websocket for connections
		await ws.prepare()

		# Listen for messages
		async for msg in ws:
			if msg.type == aiohttp.WSMsgType.TEXT:
				# Response for command execution
				if msg.data:
					await ws.close()
			
			# Close connection
			elif msg.type == aiohttp.WSMsgType.ERROR:
				Print.bad(f"WSError: {ws.exception()}")

	async def addAgent(request):
		data  = await request.json()
		
		# Just an basic check
		try:
			listening_ip = data['listening_ip']
			listening_pt = data['listening_pt']
			name 		 = data['name']

		except:
			return web.json_response(data = {
				"sucess"  : 1,
				"error"   : "Cannot add an empty agent."
			})

		# Create an instance for errors handling
		agent = agentsDatabase.addAgent(data["listening_ip", "listening_pt"], data["name"])

		if agent[0] != 0:
			Print.bad(f"Can\'t add agent, error: {agent[1]}")
			
			return web.json_response(data = {
				"sucess"  : 1,
				"error"   : agent[1]
			})

		return web.json_response(data = {
				"sucess"  : 0,
			})
		
def main():
	Print.good("Initializing the database")
	
	# Initialize the database and create an instance
	app = web.Application()
	
	# Check for database errors
	if agentsDatabase.createAgentsDatabase()[0] != 0:
		Print.bad(f"Cant create the database, error: {agentsDatabase.createAgentsDatabase()[1]}")
		exit()

	# Add routes to app
	Print.good("Initializing routes")
	app.add_routes([
		web.get('/agents', C2Server.agentList),
		web.get('/communicate', C2Server.webSocket),
		
		web.post('/agent/add', C2Server.addAgent),
	])

	# Run the app
	Print.good("Routes ok")
	web.run_app(app)


if __name__ == '__main__':
	main()