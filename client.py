import socket
import threading 
import sys


'''Importing tkinter for GUI interface'''
import tkinter as tk
from tkinter import scrolledtext, messagebox

'''Global variables for GUI and network handles'''
client_socket=None
root=None
chat_display=None
message_input=None
status_label=None

'''Added Tkinter and responsible global variables for GUI elements''' 

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


def Texting_Chat(text_context): 
    """Safely opens the GUI log window, adds the incoming text, and relocks it."""
    global chat_display
    if chat_display: 
        chat_display.configure(state="normal")
        chat_display.insert(tk.END, text_context + "\n")
        chat_display.configure(state="disabled")
        chat_display.yview(tk.END)


# the receiver
def receive_messages():
  
  '''Addition of global client socket'''
  global client_socket, root
  
  while True:# continuous packet collection loop
    try:
      data = client_socket.recv(1024).decode('utf-8')
      #this blocks the network call. it can read up to 1024 bytes instantly decodes them using utf-8
      if not data:
        Texting_Chat("\n[SYSTEM] connection closed by the server.")
        break
        '''Replaced print function with Texting_Chat function for GUI'''
      
      elif data == "ERR_USER_TAKEN":
        #Intercepts the username duplicate flag. If Kabir is occupied , it alerts you and breaks the loop.
        messagebox.showerror("Error", "That username already exists! Disconnecting...")
        break
        '''Replaced the print statement for messagebox for GUI'''
      else:
            Texting_Chat(data)
            '''Below code was commented and removed to use Texting_chat function for the GUI'''
        #'print(f"\n{data}")#If the server data isn't a handshake flag,it's a real chat message or a system notice! It prints it cleanly
        #on your terminal layout screen.
        #print("> ", end="", flush=True)#Because messages from other clients drop onto your screen 
        #unexpectedly, this forces the terminal text system to draw a clean prompt arrow (> ) without 
        #starting a new newline. This lets you see what you are currently typing.
        
    except Exception as E:
      break
   #Cleans up kills the operation out of the thread loop    
  try:
    client_socket.close()
  except:
    pass
  if root: 
    root.destroy()
  sys.exit()

# the sender 
def send_message(event=None):
    '''Pulls text from the Tkinter text entry area and transmits it to the server.'''
    global client_socket, message_input, root
    
    # Grabs the text out of the GUI input box
    message = message_input.get()
    
    if message.strip() == "":
        return
        
    try:
        # Send the encoded bytes across the network
        client_socket.send(message.encode('utf-8'))
        
        # Clear the input box so you can type your next message
        message_input.delete(0, tk.END)
                           
        if message.strip() == "quit":
            client_socket.close()
            root.destroy()
            sys.exit()
                         
    except Exception as e:
        Texting_Chat(f"[ERROR] Failed to send the message: {e}")



def chat_window(): 
    """Responsible for building the primary visual layout containers using Tkinter."""
    global root, chat_display, message_input, status_label
    
    root = tk.Tk()
    root.title("Chat Client") 
    root.geometry("600x600") 
    root.configure(bg="#f7f7f7") 
    
    status_label = tk.Label(root, text="Connecting to the server...", bg="#615e5e", fg="#ffffff", font=("Courier New", 14))
    status_label.pack(fill=tk.X)
    
    chat_display = scrolledtext.ScrolledText(root, state="disabled", wrap=tk.WORD, bg="#000000", fg="#FFFFFF", font=("Courier New", 13)) 
    chat_display.pack(padx=12, pady=12, fill=tk.BOTH, expand=True) 
    
    input_frame = tk.Frame(root, bg="#2f3136") 
    input_frame.pack(padx=10, pady=10, fill=tk.X)
    
    message_input = tk.Entry(input_frame, bg="#F7F7F9", fg="#000000", insertbackground="black", font=("Courier New", 13))
    message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
    message_input.focus_set() 
    message_input.bind("<Return>", send_message) 
    
    send_button = tk.Button(input_frame, text="Send", command=send_message, bg="#CCFF00", fg="black", font=("Courier New", 8, "bold"), relief=tk.FLAT, padx=15)
    send_button.pack(side=tk.RIGHT, padx=(10,0))

# execution code and assigning cilents 
def start_client():
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #matches the sever network settings exactly uses IPv4 and TCP stram bassed connection 
  try:
    client_socket.connect((ser_Ip,port))# fires of the TCP Three way handshake with the server machine
    print(f"[VICTORY] Connected to the server at {ser_Ip}:{port}")

    ser_flag = client_socket.recv(1024).decode('utf-8')# the handshake happence here first

    if ser_flag == "CMD_REQQ_USER": #this checks if the message just recived from the server matches the contol flag string.
      username = input("Enter your username: ").strip()#type a username
      client_socket.send(username.encode('utf-8'))
      
  except Exception as e:
    print(f"[CRITICAL] Could not connect with the server: {e}")
    return
  
  receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
  #this code creates our separate sub-thread pathway. We assign target= to our inbound message listener function and pass the connected socket interval into its parameters using args=                                  
  receive_thread.daemon = True 
  #this flags the sub-thread as a daemon worker. This means it depends on the lifecycle of the main thread. When you quit or close the client app, 
  #the os automatically terminates this background thread rather than letting it sit alone in your computer ram.

  receive_thread.start() #Wakes up the sub-thread and tells it to begin running by itself in the background.

  send_message(client_socket)#aunches our keyboard monitoring input loop immediately on the foreground main thread.

if __name__ == "__main__":
  start_client()




