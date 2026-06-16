import socket
import threading 

# we are importing the the python library for sockets and threads. Sockets the funcations that will allow for the communicating to occur and threads so the code doesnt get stuck waiting
#for you to type and shows message recieved only after the clients has hit send.

ser_Ip = '127.0.0.1'
port = 65432

#ser_Ip means server ip which is 127.0.0.1 why this number ; is used for loop backs meaning the packet is send to the outside network but is roated 
#(loops back )in the computer operating system. it is safe because you can run tests without  active internet connection and because it it your local network it is also safe.
# if you want to test this on a different computer make host =0.0.0.0 meainig listein to every network interface that is on the laptop(on laptop 1). (on laptop 2) 
#and change ser_Ip to the ip of laptop 1 (run ifconfig to get the ip address)

# This was part one of the code where we created the set up) 
