import socket
import threading 
import sys

# we are importing the the python library for sockets and threads. Sockets the funcations that will allow for the communicating to occur and threads so the code doesnt get stuck waiting
#for you to type and shows message recieved only after the clients has hit send.

ser_Ip = '127.0.0.1'
port = 65432

#ser_Ip means server ip which is 127.0.0.1 why this number ; is used for loop backs meaning the packet is send to the outside network but is roated 
#(loops back )in the computer operating system. it is safe because you can run tests without  active internet connection and because it it your local network it is also safe.
# if you want to test this on a different computer make host =0.0.0.0 meainig listein to every network interface that is on the laptop(on laptop 1). (on laptop 2) 
#and change ser_Ip to the ip of laptop 1 (run ifconfig to get the ip address)

# This was part one of the code where we created the set up) 


def receive_messages(client_socket):
  while True:# continuous packet collection loop
    try:
      data = client_socket.recv(1024).decode('utf-8')
      #this blocks the network call. it can read up to 1024 bytes instantly decodes them using utf-8
      if not data:
        print("\n[SYSTEM] connection closed by the server.")
        break
      # if the connection breaks or drops recv()= returns completely empty bytes(b''). this helps to cleanly breakout loop execution if the server shut down.
      if data == "CMD_REQQ_USER":
        username = input("Enter your username: ").strip()
        client_socket.send(username.encode('utf-8'))
        #this heklps implement the Application Layer Handshake. The client intercepts this string from the server. Instead of showing it to the user, it triggers 
      #an input() code asking you for your username, wraps it in bytes using .encode('utf-8'), and sends it straight back up the line.
      elif data == "ERR_USER_TAKEN":
        #Intercepts the username duplicate flag. If Kabir is occupied , it alerts you and breaks the loop.
        PRINT("[ERROR] That username already exists! Disconnecting...")
        break
      else:
        print(f"\n{data}")#If the server data isn't a handshake flag,it's a real chat message or a system notice! It prints it cleanly
        #on your terminal layout screen.
        print("> ", end =="", flush=True)#Because messages from other clients drop onto your screen 
        #unexpectedly, this forces the terminal text system to draw a clean prompt arrow (> ) without 
        #starting a new newline. This lets you see what you are currently typing.
    except Exception as E:
      print(f"\n[ERROR] connection lost: {E}")
      break
  cleint_socket.close()
  sys.exist()#Cleans up and kills the client application 
  #execution immediately if the loop crashes or ends


