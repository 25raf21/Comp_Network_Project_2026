import socket 
import threading 

host = '0.0.0.0'
port = '65432'

# host will tells which network interface is the served allowed to listein to. if host is 127.0.0.1 meaning you have a local network meaning you are communication using on device your 
# client and server file are on one computer, if host 0.0.0.0 is used meaning the communication is happening between two computers and you will have to change the ser_ip to the ip 
# address of the computer where the server file is.here the serever only listeins to port 65432 ( write for client file too)

clients = {}

#As the network sockets are anonymos and blind (because the operating system sees only the raw connections streams and donest know who the connections belongds to who he wants to talk to i.e
#we need to know that one of your client i.e kabir is wants to talk to someone in room backrooms). the clients command will help us tell us who sent the packet did the clients
#connection got disconnected or when a message.
#to assign clients write inside curly brackets client_sock_N(number): 'Username you want to assign the client'
# and a room by "name":[] in the room curly brackets

rooms = {
  "publicroom":[]
  "backrooms":[]
  "privateroom":[]
}

# helps the socket programme group the clients together to join a goup type "/join group name"

# phase 1 completed: the goal ws to first create a setup then as we are not using a database we need to use the RAM to store and track the information.
#(who is online and which room the conversation is going on )


