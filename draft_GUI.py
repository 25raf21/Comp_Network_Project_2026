chat_display=None
message_input=None
status_label=None

# Function below is responsible for making the visual graphical interface by using Tkinter
def chat_window(): 
    global root, chat_display, message_input, status_label
    
    root = tk.Tk()
    root.title("Chat Client") 
    root.geometry("600x600") #Decides the size of the GUI window
    root.configure(bg="#f7f7f7") 
    
    #It displays the status bar above the GUI Chat window
    status_label = tk.Label(root, text="Connecting to the server...", bg="#615e5e", fg="#ffffff", font=("Courier New", 18))
    status_label.pack(fill=tk.X)
    
    #It displays the Chatlog 
    chat_display = scrolledtext.ScrolledText(root, state="Disabled", wrap=tk.WORD, bg="#000000", fg="FFFFFF", font=("Courier New", 13)) 
    chat_display.pack(padx=12, pady=12, fill=tk.BOTH, expand=True) 
    
    #Displays the input text area along with focusing the text cursor onto the text box
    message_input = tk.Entry(input_frame, bg="#F7F7F9", fg="#FFFFFF", insertbackground="black", font=("Courier New", 13))
    message_input.pack(side=tk.LEFT, fill=tk.tk.X, expand=True, ipady=4)
    message_input.focus_set() 
