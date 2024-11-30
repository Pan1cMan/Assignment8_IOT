import socket

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
                print(f"Received data from client: {data.decode()}")
                # Conver the data to uppercase as required to be later sent back to the client.
                response = data.decode().upper()
                # Send the data back to the client
                conn.sendall(response.encode())
                # Print the info and the data that we are sending to the client.
                print(f"Sent data to the client: {response}")

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