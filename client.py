import socket

def tcp_client():
    try:
        # Server IP and port
        server_ip = input("Enter server IP address: ")
        server_port = int(input("Enter the server port number: "))

        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Connecting to server at {server_ip}:{server_port}...")

            # Connect to the server
            client_socket.connect((server_ip, server_port))
            print("Connected to the server.")

            # Infinite loop to keep sending requests
            while True:
                # Input request from the user
                message = input("Enter a request (or type 'exit' to quit): ")

                # Exit if the user types 'exit'
                if message.lower() == "exit":
                    print("Closing the connection.")
                    break

                # Send the request to the server
                client_socket.sendall(message.encode())

                # Wait for the server's response
                response = client_socket.recv(1024)

                # Print the response from the server
                print(f"Response from server: {response.decode()}")

    except ValueError:
        print("Error: Invalid port number. Please enter an integer.")
    except socket.error as e:
        print(f"Socket error: {e}")

# Main function to start the client
if __name__ == "__main__":
    tcp_client()
