import tkinter as tk
from tkinter import messagebox
from backend import NoteShare

class NoteShareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Share")
        self.noteshare = NoteShare()
        self.create_login_ui()

    def create_login_ui(self):
        self.username_label = tk.Label(self.root, text = "Username: ")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text = "Password: ")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text = "Login", command = self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.noteshare.authenticate(username, password):
            auth_bool, user_id = self.noteshare.get_user_id(username, password)
            self.show_notes(user_id, username)
        else:
            messagebox.showerror('Error', 'Invalid username or password')
    
    def show_notes(self, user_id, username):
        note_window = tk.Toplevel(self.root)
        note_window.title('Notes')
        note_label = tk.Label(note_window, text = "Notes for " + username)
        note_label.pack()

        create_label = tk.Label(note_window, text = "Want to add new note?")
        create_label.pack()
        create_entry = tk.Entry(note_window)
        create_entry.pack()

        def create_new_note():
            create_note = create_entry.get()
            self.noteshare.create_note(user_id, create_note)
            note_window.update()

        create_button = tk.Button(note_window, text = "Create New Note", command = create_new_note)
        create_button.pack()

        



        notes = self.noteshare.get_note_from_user_id(user_id)
        for note in notes:
            
            note_label_var = tk.StringVar()
            note_label_var.set(note)
            note_label = tk.Label(note_window, textvariable=note_label_var)
            note_label.pack()

            edit_entry = tk.Entry(note_window, text = "If you want to edit, you can update note here...")
            edit_entry.pack()
            note_auth, note_id = self.noteshare.get_note_id(note)

            def update_note(note = note):
                
                new_note = edit_entry.get()
                self.noteshare.update_notes(note_id, new_note)   
                note_label_var.set(new_note)

            edit_button = tk.Button(note_window, text = "Modify note", command = update_note)
            edit_button.pack()

            friend_label = tk.Label(note_window, text = "Want to share notes with friend?")
            friend_label.pack()
            friend_entry = tk.Entry(note_window)
            friend_entry.pack()

            def share_note(note = note):
                friendname = friend_entry.get()
                friend_bool, friend_id = self.noteshare.get_friend_id(friendname)
                print(friend_id)
                if friend_bool:
                    # friend_id = int(friend_id)
                    self.noteshare.share_notes(int(note_id), int(friend_id))
                    messagebox.showinfo('Succress', f'Successfully added {friendname}')
                else:
                    messagebox.showinfo('Succress', f'Successfully added {friendname}')
                
            def delete_note(note = note):
                self.noteshare.delete_note(note_id, user_id)
                messagebox.showinfo('Succress', 'Successfully deleted')

            
            
            share_button = tk.Button(note_window, text = "Add friend", command = share_note)
            share_button.pack()
            share_button = tk.Button(note_window, text = "delete", command = delete_note)
            share_button.pack()





    
if __name__ == '__main__':
    root = tk.Tk()
    app = NoteShareGUI(root)
    root.mainloop()
