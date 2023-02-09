import socket #socket is an IP address coupled with a port number e.g., '172.00.1 on port 80' = socket
#e.g., google
target_host = "google.com"
target_port = 80

#create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the client to target 
client.connect((target_host, target_port))

# Send some data
client.send(b"GET / HTTP/1.1\r\nHOST:google.com\r\n\r\n")

#Receive data 
response = client.recv(4096)

print(response)
