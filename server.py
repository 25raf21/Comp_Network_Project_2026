import socket 
import threading 

host = '0.0.0.0'
port = 65432

# host will tells which network interface is the served allowed to listein to. if host is 127.0.0.1 meaning you have a local network meaning you are communication using on device your 
# client and server file are on one computer, if host 0.0.0.0 is used meaning the communication is happening between two computers and you will have to change the ser_ip to the ip 
# address of the computer where the server file is.here the serever only listeins to port 65432 ( write for client file too)

clients = {}

#As the network sockets are anonymos and blind (because the operating system sees only the raw connections streams and donest know who the connections belongds to who he wants to talk to i.e
#we need to know that one of your client i.e kabir is wants to talk to someone in room backrooms). the clients command will help us tell us who sent the packet did the clients
#connection got disconnected or when a message.
#to assign clients write inside curly brackets client_sock_N(number): 'Username you want to assign the client'
# and a room by "name":[] in the room curly brackets (client_sock_N1: "kabir")

rooms = {
  "publicroom":[],
  "backrooms":[],
  "privateroom":[]
}

# helps the socket programme group the clients together to join a goup type "/join group name"

# phase 1 completed: the goal ws to first create a setup then as we are not using a database we need to use the RAM to store and track the information.
#(who is online and which room the conversation is going on )

#now in Phase 2 i have to create a routing mechanism which can duplicate and send the clients message into his specific room it in.

# we define the function broadcast_room with three parameters, the first being message the string of text the client whats to send, room_class will tell the computer where should the 
# message go and the third parameter is the network socket of the person who send the message, we set it to None because server itself needs to blast a system message to everyone, 
#there is no original sender to skip. the third line checks if a room like this exists or not.line four tell rooms[room_class] tells us how many clients are in the given room 
# the fifth line helps the user to see that they wrote rather then the app echoing your the message to you. line 7 and 8 try  is used so the server doesnt crash if the a network error 
#occurs then client_socket.send(...) physically pushes the data out over the internet card to that specific client.and .encode('utf-8') because network sockets cannot transmit Python 
# string so this translates the characters into 0s and 1s using UTF-8 formatting.

def broadcast_room(message, room_class, sender_socket=None):
  if room_class in rooms:
    for client_socket in rooms[room_class]:
      if client_socket != sender_socket:
        try:
          client_socket.send(message.encode('utf-8'))
        except:
          pass
#Phase 3: client handleing codes( multi threading core) meaning ask for user names, chekc for dupilcate username, add them to defalult chat room and listeining of their message.

def client_manag(client_socket):
  current_room = "publicroom"
  username = ""
# current_room = "publicroom":sets the default room destination string.Every user starts from here 
# username = "": creates a blank variable so that our finally:so it doent crsh if a user disconnets before finishing registration
  try:
    client_socket.send("CMD_REQQ_USER".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8').strip()
#application hanshake protocol: asks the clinet to identify themselfs. client_socket.send("CMD_REQQ_USER".encode('utf-8')): sends a unique control flag string to the client.this tells the client programm 
#"the server is waiting for you ot enter your username".
#username = client_socket.rev(1024).decode('utf-8').strip(): stops all thread execution until the client doesnt respomd wiht their useranme string.
    
    if username in clients.values() or username == "":
      client_socket.send("ERR_USER_TAKEN".encode('utf-8'))
      client_socket.close()
      return
#if username in clients.values():: Loops through our clients state dictionary to ensure that every user has a unique name and dont share an identical active nickname. 
#If they do, it shoots back ERR_USER_TAKEN and drops the line immediately.
      
    clients[client_socket] = username #changes the slient dict.
    rooms[current_room].append(client_socket) #changes this socket into the active list inside room{"piblicroom"}. 
    
    print(f"[LOG] {username} enrollment was successfull and the User has entered '{current_room}'.")
    broadcast_room(f"SYSTEM: {username} has joined the room.", current_room)
#this block of helps register the state of the program by saving the socket and adding it to the default room 

#packet proccessing loop
    while True:
      data = client_socket.recv(1024).decode('utf-8')
      # wait for data from this client 
      if not data:
        break # break if data is empty 
#data = client_socket.recv(1024): untill a singler pushes a transmission packet it stays blocked and if the connection breaks recv() returns empty bytes(b''),
#hitting our if not data: break safty net 

# commands to join rooms:
      if data.startswith("join "):# checks if incomeing text has a management command instead of a normal caht sentence 
        new_room = data.split(" ")[1].strip() #splices the input test message string at the blank space character to extract the room target name
        
        # this code helps user make there own room and then adds it into the room dictionary
        if new_room not in rooms:
          rooms[new_room] = []
          print(f"[LOG] custom room created: '{new_room}' by user '{username}'")
          client_socket.send(f"SYSTEM: User requested '{new_room}' has been created...".encode('utf-8'))
          
        if new_room in rooms:
    # remove the client that requested the change from the old room list
          rooms[current_room].remove(client_socket)
          broadcast_room(f"SYSTEM: {username} left the room.", current_room)
  
    # adds the client in the requested new room list.
          current_room =new_room
          rooms[current_room].append(client_socket)
  
    #an indicator that confirms to the user that they have switched rooms and to other people in the room
          client_socket.send(f"SYSTEM: Switch to room '{current_room}'".encode('utf-8'))
          broadcast_room(f"SYSTEM: {username} entered the room.", current_room, client_socket)
        else:
          client_socket.send("SYSTEM_ERR: Invalid Room!".encode('utf-8'))

          # these codes helps clients to invite each other to rooms 
      elif data.startswith("invite "):
        try:
          # the command format for inviting the username
          target_user = data.split(" ")[1].strip()
          
          # the code makes it so that we search trough the memory to track dictionary to locate the target socket
          target_socket = None
          for sock, name in clients.items():
            if name == target_user:
              target_socket = sock
              break
              
          if target_socket:
            # Delivers the invite control string to the specific user across the network 
            invite_mess = f"\n[NOTIFICATION] {username} has invited you to join '{current_room}'. Please enter 'join {current_room}' if you want to accpet the invite and join the room ."
            target_socket.send(invite_mess.encode('utf-8'))
            client_socket.send(f"SYSTEM: Invitation safely transmitted to '{target_user}'.".encode('utf-8'))
          else:
            client_socket.send(f"SYSTEM_ERR: User '{target_user}' is currently offline or invalid.".encode('utf-8'))
        except:
          client_socket.send("SYSTEM_ERR: Invalid instruction format. Use 'invite <username>'".encode('utf-8'))
          
    #leave block 
      elif data.strip() == "leave":# the command to exit 
            if current_room != "publicroom":# this funtion checks if the client is in the coustome chat room or in the defalut lobby
                
                print(f"[ROOM CHANGE] {username} left '{current_room}' and fell back to 'publicroom'")
                # this indicates that the user has re-entered the default lobby after leaving the room  
                
                rooms[current_room].remove(client_socket)# removes the client form recieving the messages from that room 
                broadcast_room(f"SYSTEM: {username} left the room.", current_room)
                
                current_room = "publicroom"# moves the client back to the publicroom rather then quiting the whole application 
                rooms[current_room].append(client_socket)# it switches the clients channel to recive only meassages that are written in the public lobby 
                
                # Notify the user and the public room
                client_socket.send(f"SYSTEM: Returned to '{current_room}'".encode('utf-8'))
                broadcast_room(f"SYSTEM: {username} returned to the room.", current_room, client_socket)
            else:
                # If they are already in publicroom, break the loop to disconnect completely
                break
      else:
  # chat routing:fromats the message and broadcasting it 
        formatted_mesg = f"[{current_room}] {username}: {data}"
        broadcast_room(formatted_mesg, current_room, client_socket)

  except Exception as E:
    print(f"[Error] connection crash for user '{username}': {E}")

  finally:# this used as a clean up and terminate routining 
    if client_socket in clients:
      del clients[client_socket]
    if client_socket in rooms[current_room]:
      rooms[current_room].remove(client_socket)
#finally:the code guaranteed to execute by the Python runtime machine no matter what—whether the user typed
#quit, shut down their client window cleanly, or completely lost power. It deletes 
#keys using del to avoid memory leakage and safely executes .close().

    client_socket.close()
    print(f"[LOG] Connection is terminated for {username}.")
    broadcast_room(f"SYSTEM: {username} has disconnected.",current_room)
    
#Phase 4: Core listeining loop 

def start_server():
  #unparameterized python function that wraps our server startup sequence.
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #tells the os that weare using IPv4 addressing criteria(socket.AF_INET, And socket.SOCK_STREAM tells the os to use TCP as the transport-layer protocol.
  server.bind((host, port))
  #allows the server to only listein to the specificed address and port combinations and no other application can be used when this application is running
  server.listen()
  print(f"[RUNNING] Server listening on {host}:{port}")
  # makes the server listien and show it is listening 
  while True:
   #the loop will run forever untill contrl c is not pressed 
    client_socket, client_address = server.accept()
   # this is a blocking call meaning it will cut all executions of and waits for the client to .connect(). once the client connects meaning the three way TCP handshake is complete 
   #the .accept() wakes up and return the client_socket: a socket that will point to a specific client.the client_address contain the clients ip and oport whihc is used to login 
    print(f"[NEW NODE] Connection formed from {client_address}")
# showe textual the login was successful  
    client_thread = threading.Thread(target=client_manag, args=(client_socket,))
    client_thread.start()
#this is where the multi-threading magc occurs that satisfies  the requirmnet to support three or more users 
#threading.Thread(...)builds a new thread. We point target=to our Phase 3 function ( client_manag), and pass the specific client socket we received in line 9 as an argument via 
#args=..start()physically kicks off the thread execution in the background.

if __name__ == "__main__":
    start_server()

          
