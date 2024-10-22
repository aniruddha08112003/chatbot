import tkinter as tk
from tkinter import font as tkFont
from chatbot import chatbot_response

def send():
    msg = entry_box.get("1.0", 'end-1c').strip()
    entry_box.delete("0.0", tk.END)

    if msg != '':
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {msg}\n\n")
        chat_log.config(foreground="#442265", font=("Helvetica", 12))

        res = chatbot_response(msg)
        chat_log.insert(tk.END, f"Bot: {res}\n\n")

        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)

root = tk.Tk()

# Set window size to mimic a mobile screen (approximately 6.1-inch display)
root.geometry("375x667")  # 375x667 pixels is close to a typical mobile resolution
root.configure(bg="#E8F5E9")  # Soft green background

# Chat log styling
chat_log = tk.Text(root, bd=0, bg="#FFFFFF", height="25", width="50", font=("Helvetica", 12), wrap=tk.WORD)
chat_log.config(state=tk.DISABLED)

scrollbar = tk.Scrollbar(root, command=chat_log.yview)
chat_log['yscrollcommand'] = scrollbar.set

# Send button styling
send_button = tk.Button(root, font=("Helvetica", 12, 'bold'), text="Send", width=10, height=1, 
                        bd=0, bg="#81C784", activebackground="#66BB6A", fg='#ffffff', command=send)

# Entry box styling with a distinct background color
entry_box = tk.Text(root, bd=0, bg="#F1F8E9", width=29, height=5, font=("Helvetica", 12))

# Layout adjustments
scrollbar.place(x=360, y=50, height=580)  # Adjust height for scrollbar
chat_log.place(x=6, y=50, height=580, width=350)  # Height for chat log adjusted to fit
entry_box.place(x=6, y=615, height=50, width=290)  # Height for entry box adjusted to fit
send_button.place(x=300, y=615, height=50)  # Height for send button adjusted to fit

# Optional: Add a label at the top for branding
header_label = tk.Label(root, text="🌸 Flower Shop Chatbot 🌸", font=("Helvetica", 16, 'bold'), bg="#E8F5E9", fg="#442265")
header_label.pack(pady=10)

# Set minimum window size to maintain layout
root.minsize(375, 667)

root.mainloop()
