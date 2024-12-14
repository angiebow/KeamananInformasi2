import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")

        # Connected clients dropdown
        self.client_label = tk.Label(self.root, text="Connected Clients:")
        self.client_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.client_dropdown = ttk.Combobox(self.root, state="readonly", values=["Broadcast"])
        self.client_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.client_dropdown.current(0)  # Default to "Broadcast"
        self.client_dropdown.bind("<<ComboboxSelected>>", self.update_chat_display)

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', height=20, width=50)
        self.chat_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Message entry field
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.grid(row=2, column=0, padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=1, padx=10, pady=5)

        # Simulated clients (for demonstration purposes)
        self.conversations = {"Broadcast": []}  # Stores messages for each client or broadcast
        self.update_clients(["Client1", "Client2", "Client3"])

    def update_clients(self, clients):
        for client in clients:
            self.conversations[client] = []
        self.client_dropdown["values"] = ["Broadcast"] + clients
        self.client_dropdown.current(0)  # Reset to "Broadcast"
        self.update_chat_display()

    def update_chat_display(self, event=None):
        target = self.client_dropdown.get()
        self.chat_area.config(state='normal')
        self.chat_area.delete(1.0, tk.END)
        for sender, message in self.conversations[target]:
            self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')

    def send_message(self, event=None):
        message = self.message_entry.get()
        target = self.client_dropdown.get()
        if message.strip():
            if target == "Broadcast":
                self.conversations[target].append(("You (Broadcast)", message))
            else:
                self.conversations[target].append(("You", message))
            self.update_chat_display()
            # Simulate a reply for now (you can replace this with actual server communication later)
            self.root.after(1000, lambda: self.receive_message(target, f"Echo: {message}"))
        self.message_entry.delete(0, tk.END)

    def receive_message(self, sender, message):
        if sender in self.conversations:
            self.conversations[sender].append((sender, message))
        self.update_chat_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
