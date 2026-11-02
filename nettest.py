from network import Network
import threading
import time

network = Network()

# Host / Join selection test
choice = input("Host or Join? (h/j): ").lower().strip()
if choice == "h":
    network.host()
    print("Server started. Waiting for someone to join...")
elif choice == "j":
    host_ip = input("Enter the host IP address: ").strip()
    network.join(host_ip)
    print("Connecting to host...")
else:
    print("ERROR: Invalid Choice")
    exit()

# Sending Message Test
def send_messages():
    while network.running:
        if network.connected:
            text = input("\nYou: ")
            if text.lower() == "quit":
                network.close()
                break
            network.send({
                "type": "chat",
                "message": text
            })
        else:
            time.sleep(0.1)
threading.Thread(
    target=send_messages,
    daemon=True
).start()

# Receive Message Test
try:
    while network.running:
        for message in network.poll():
            if message["type"] == "connected":
                print("\nSuccessfully connected!")
            elif message["type"] == "message":
                if message["data"]["type"] == "chat":
                    print("\nOpponent:", message["data"]["message"])
            elif message["type"] == "disconnected":
                print("\nOpponent disconnected.")
            elif message["type"] == "error":
                print("\nNetwork error:", message["message"])
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    network.close()