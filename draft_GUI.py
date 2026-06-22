import tkinter as tk
from tkinter import scrolledtext, messagebox

root=None
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
    
    
    send_button = tk.Button(input_frame, text="Send", bg="#CCFF00", fg="white", font=("Courier New", 8, "bold"), relief=tk.FLAT, padx=15)
    send_button.pack(side=tk.RIGHT, padx=(10,0))
    
# Texting_Chat function safely opens the GUI window, adds the text and relocks it back
def Texting_Chat(text_context): 
    
    global chat_display
    if chat_display: 
        chat_display.configure(state="normal") #Unlocks the chat
        chat_display.insert(tk.END, text_context + "\n") #Pushes the text
        chat_display.configure(state="disabled") #Locks it back up
        chat_display.yview(tk.END) #Snaps the scrollbar back to the bottom

def fetch_username_popup(on_submit):
    
    global root
    
    popup = tk.Toplevel(root)
    popup.title("Identity Setup") 
    popup.geometry("400x400") 
    popup.configure(bg="#FFFFFF") 
    popup.transient(root) 
    popup.grab_set()
    
    label = tk.Label(popup, text="Enter your Username: ", bg="#000000", fg="whtie") 
    label.pack(pady=12) 
    
    entry = tk.Entry(popup, font="Courier News", bg="#000000", fg="white") 
    label.pack(pady=12)
    
    entry = tk.Entry(popup, font=("Courier News", 13)) 
    entry.pack(padx=18, pady=6, fill=tk.X) 
    entry.focus_set()
    def handle_click(): 
        chosen_name = entry.get().strip()
        if chosen_name: 
            popup.destroy()
            on_submit(chosen_name)
        else: 
            messagebox.showwarning("Warning", "Username cannot be empty!") 
    Button = tk.Button(popup, text="Join room", command=handle_click, bg="#F7F7F7", fg="white", font=("Courier News", 10, "bold"))
    Button.bind("<Return>", lambda e: handle_click())

    
