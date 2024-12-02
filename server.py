import socket
from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

class TreeNode:
    def __init__ (self, key, data):
        self.key = key
        self.data = [data]
        self.left = None
        self.right = None

class BinaryTree:
    def __init__ (self):
        self.root = None
    
    def insert(self, key, data):
        if self.root is None:
            self.root = TreeNode(key, data)
        else:
            self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, data)
            else:
                self._insert(node.left, key, data)
        
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, data)
            else:
                self._insert(node.right, key, data)

        else:
            node.data.append(data)

    def search(self, key):
        if self.root is None:
            return None
        else:
            return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        elif key < node.key:
            return self._search(node.left, key)
        elif key > node.key:
            return self._search(node.right, key)
        else:
            return node.data

def relative_moisture_process(data):
    max_val = 999

    raw_moisture = float(data["payload"]["Moisture Meter - Moisture1"])
    relative_moisture = (raw_moisture / max_val) * 100
    return relative_moisture

def water_flow_gallons_process(data):
    max_flow_rate_lpm = 10
    
    raw_water_flow = float(data["payload"].get("WaterFlow1", 0))
    flow_rate_lpm = (raw_water_flow / 100) * max_flow_rate_lpm

    flow_rate_gpm = flow_rate_lpm * 0.264172

    gallons = flow_rate_gpm * 60

    return gallons

    

# The function to start the server on the server side
def start_server():

    # Try and catch, in case of a value error when entering the server ip or server port making sure the server port
    # is an integer
    try:

        # Server ip and port from the user input
        server_ip = input("Enter server IP address: ")
        # turning the server port into an integer after from the user input
        server_port = int(input("Enter the port number (has to be the same number for the client): "))

        # using AF_INET for the host and port where the host is a string and the port is a integer specified for ipv4
        # SOCK_STREAM is for when we want to use TCP instead of UDP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binding the server socket to the server ip and port, basically tells the server to listen for any
        # incoming connections
        server_socket.bind((server_ip, server_port))

        # listening for the actual connections
        server_socket.listen(1)

        # if it successfully connects then it will print where the ip is and what port it is connected to
        print(f"Listening in server IP: {server_ip} and port: {server_port}")

        # Infinite loop to keep grabbing the connection
        while True:

            # wait for the client to connect
            conn, addr = server_socket.accept()

            # if it successfully connects then it will print connected.
            print("Connected")

            # Infinite loop to keep receiving up to a certain amount of bytes of data 
            # from the client
            while True:

                # Receive about 1024 bytes of data
                data = conn.recv(1024)
                if not data:
                    # if there is no data we close it and break the infinite loop.
                    break

                # Print if we receive the data and what its content is
                connection_string = "mongodb+srv://CECS327:PlumBeast69@cluster0.bhxu6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
                client = MongoClient(connection_string)

                current_time = datetime.now()
                cutoff = current_time - timedelta(hours=3)

                print(f"Received data from client: {data.decode()}")
                # Conver the data to uppercase as required to be later sent back to the client.
                
                request = data.decode()
                try :
                    db = client["test"]
                    collection = db["Table1_virtual"]

                    # tree = BinaryTree()

                    # for data in collection.find():
                    #     key = data["payload"]["parent_asset_uid"]
                    #     tree.insert(key, data)

                    data = defaultdict(list)

                    for rec in collection.find():
                        data[rec["payload"]["parent_asset_uid"]].append(rec)
                    
                    match request:
                        case "1":
                            # moisture_recs = collection.find({
                            #     "payload.parent_asset_uid": "080-729-mk9-61n",
                            #     "time": {"$gte": cutoff}
                            # })
                            # moisture_values = [relative_moisture_process(data) for data in moisture_recs]
                            # for data in collection.find():
                            #     if data["payload"]["parent_asset_uid"] == "080-729-mk9-61n":
                            #         time_rec = data["time"]
                            #         if time_rec > cutoff:
                            #             moisture_values.append(relative_moisture_process(data))

                            key = "1003"
                            # records = tree.search(key)
                            records = data.get(key, [])
                            moisture_values = []

                            current_time = datetime.now()
                            cutoff = current_time - timedelta(hours=3)  
                            for r in records:
                                print(r)
                                if r["time"] > cutoff:
                                    relative_moisture_process(r)
                                    moisture_values.append(relative_moisture_process(r))

                            if moisture_values:
                                average_moisture = sum(moisture_values) / len(moisture_values)
                                print(f"Average moisture: {average_moisture}")
                                conn.sendall(f"The average moisture is: {average_moisture}".encode())
                                

                        case "2":

                            # water_recs = collection.find({
                            #     "payload.parent_asset_uid": "989bbfbe-f5d8-4f58-9eb2-72fdb2e3117b"
                            # })
                            
                            # for data in water_recs:
                            #      water_flow_value = data.get("payload", {}).get("WaterFlow1", "Key not found")
                            #      print(f"WaterFlow1 value: {water_flow_value}")
                            # water_flow_values = [water_flow_gallons_process(data) for data in water_recs]

                            key = "1001"
                            # records = tree.search(key)
                            records = data.get(key, [])
                            water_flow_values = []

                            for r in records:
                                print(r)
                                water_flow_values.append(water_flow_gallons_process(r))

                            if water_flow_values:
                                average_water_flow = sum(water_flow_values) / len(water_flow_values)
                                print(f"Average water flow: {average_water_flow}")
                                conn.sendall(f"The average water flow is: {average_water_flow}".encode())
                                
                            

                except Exception as e:
                    print(e)

            # Close the connection
            conn.close()
            print("Connection closed.")
            
    # Except for if the user enters an invalid port number
    except ValueError:
        print(("Error: Invalid port number. Please enter an integer."))

    # Except for if there is a socket error
    except socket.error as e:
        print(f"Socket error: {e}")

# Main function to immediately start server
if __name__ == "__main__":
    start_server()