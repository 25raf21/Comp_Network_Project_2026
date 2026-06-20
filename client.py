import socket
import threading 
import sys

# we are importing the the python library for sockets and threads. Sockets the funcations that will allow for the communicating to occur and threads so the code doesnt get stuck waiting
#for you to type and shows message recieved only after the clients has hit send. we use the sys library because it instantly kills the entire multi-threaded program if a connection drops 
#which prevents the terminal window from freezing up on a blocked keyboard input.

ser_Ip = '127.0.0.1'
port = 65432

#ser_Ip means server ip which is 127.0.0.1 why this number ; is used for loop backs meaning the packet is send to the outside network but is roated 
#(loops back )in the computer operating system. it is safe because you can run tests without  active internet connection and because it it your local network it is also safe.
# if you want to test this on a different computer make host =0.0.0.0 meainig listein to every network interface that is on the laptop(on laptop 1). (on laptop 2) 
#and change ser_Ip to the ip of laptop 1 (run ifconfig to get the ip address)

# This was part one of the code where we created the set up) 

# the receiver
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
  client_socket.close()
  sys.exist()#Cleans up and kills the client application 
  #execution immediately if the loop crashes or ends

# the sender 
def send_message(client_socket):# Transmission function wrapper
  while Ture:
    try:
      message = input("> ")#this blocks the keyboard call when you are typing a meassage or executing a commands to switch the chat rooms
      if message.strip() == "":# if you enter a empty string this code makes it so it is ignored to not waste resources 
         continue
      
      client_socket.send(message.encode('utf-8'))#turns text into binary bytes and pushes them out through the local network 
      #card onto the wire toward the server host.
                         
       if message.strip() == "/quit":
             break #if /quit, the loops is exits
                         
       except Exception as e :
          print(f"[ERROR] Falied to send the message: {e}")
          break

client_socket.close()
sys.exit()


def start_client():
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #matches the sever network settings exactly uses IPv4 and TCP stram bassed connection 
  try:
    client_socket.connect((ser_Ip,port))# fires of the TCP Three way handshake with the server machine
    print(f"[] Connected to the server at {host}:{port}")
  except Exception as e:
    print(f"[CRITICAL] Could not connect with the server: {e}")
    return
  recieve_thread = threading.Thread(target=receive_messages, args=(client_socket,))
  #this code creates our separate sub-thread pathway. We assign target= to our inbound message listener function and pass the connected socket interval into its parameters using args=                                  
    receive_thread.daemon = True 
  #this flags the sub-thread as a daemon worker. This means it depends on the lifecycle of the main thread. When you quit or close the client app, 
  #the os automatically terminates this background thread rather than letting it sit alone in your computer ram.

    receive_thread.start() #Wakes up the sub-thread and tells it to begin running by itself in the background.

    send_message(client_socket)#aunches our keyboard monitoring input loop immediately on the foreground main thread.

if __name__ == "__main__":
  start_client()




