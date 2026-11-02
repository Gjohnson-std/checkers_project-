import websockets
import asyncio
import json
import random

WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 2


#store player data
players = {}
next_player_id = 1
clients = set()

async def handle_client(websocket, path):
    global next_player_id
    player_id = next_player_id
    next_player_id += 1

    # Store the new player in the players dictionary
    players[player_id] = {
        "id": player_id,
        "x": random.randint(0, WIDTH - PLAYER_SIZE),
        "y": random.randint(0, HEIGHT - PLAYER_SIZE),
        "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    }

    # Add the websocket to the clients set
    clients.add(websocket)

    try:
        # Send the initial state of all players to the new client
        await websocket.send(json.dumps({"type": "init", "players": list(players.values())}))

        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "move":
                # Update the player's position
                players[player_id]["x"] = data["x"]
                players[player_id]["y"] = data["y"]

                # Broadcast the updated position to all connected clients
                update_message = json.dumps({"type": "update", "player": players[player_id]})
                await asyncio.wait([client.send(update_message) for client in clients])
    finally:
        # Remove the player from the players dictionary and clients set when they disconnect
        del players[player_id]
        clients.remove(websocket)