import sqlite3

class NoteShare:
    def __init__(self):
        self.conn = sqlite3.connect('notes.db')
        self.c = self.conn.cursor()
        self.c.execute('create table if not exists users (user_id integer primary key autoincrement, username text, password text)')
        self.c.execute('create table if not exists notes (note_id integer primary key autoincrement, note text)')
        self.c.execute('create table if not exists sharing (note_id integer, user_id integer, foreign key(note_id) references notes(note_id), foreign key(user_id) references users(user_id), primary key(user_id, note_id))')
        self.conn.commit()

    def create_user(self, username, password):
        self.c.execute('insert into users (username, password) values (?, ?)', (username, password))
        self.conn.commit()
        print(f"New user '{username}' has been added to system.")

    def create_note(self, user_id, note):
        self.c.execute('insert into notes (note) values (?)', (note,))
        self.conn.commit()
        
        note_id = self.c.lastrowid
        self.c.execute('insert into sharing values (?, ?)', (note_id, user_id))
        self.conn.commit()
        print(f"New note '{note}' has been added to system.")

    def share_notes(self, note_id, new_user_id):
        self.c.execute('insert into sharing values(?, ?)', (note_id, new_user_id))
        self.conn.commit()

    def authenticate(self, username, password):
        self.c.execute('select * from users where username = ? and password = ?', (username, password))
        return bool(self.c.fetchall())

    def update_notes(self, note_id, note):
        self.c.execute('update notes set note = ? where note_id = ?', (note, note_id))
        self.conn.commit()
        print(f"Node '{note}' has been updated.")

    def get_user_id(self, username, password):
        self.c.execute('select * from users where username = ? and password = ?', (username, password))
        user_id = self.c.fetchone()
        if user_id:
            return True, user_id[0]
        else: 
            return False, None
        
    def get_friend_id(self, username):
        self.c.execute('select * from users where username = ?', (username,))
        user_id = self.c.fetchone()
        if user_id:
            return True, user_id[0]
        else: 
            return False, None
        
    def get_note_id(self, note):
        self.c.execute('select * from notes where note = ?', (note, ))
        note_id = self.c.fetchone()
        if note_id:
            return True, note_id[0]
        else:
            return False, None
        
    def get_note_from_user_id(self, user_id):
        self.c.execute('select note_id from sharing where user_id = ?', (user_id, ))
        note_ids = self.c.fetchall()
        # print("Note ids: ", note_ids)
        notes = []
        for note_id_tuple in note_ids:
            note_id = note_id_tuple[0]
            self.c.execute('select note from notes where note_id = ?', (note_id, ))
            note = self.c.fetchone()
            # print("note: ", note)
            if note:
                notes.append(note[0])
        return notes

    def delete_note(self, note_id, user_id):
        self.c.execute('delete from sharing where note_id = ? and user_id = ?', (note_id, user_id))
        self.conn.commit()

    
def main():
    noteShare = NoteShare()
    if not noteShare.authenticate("user1", "password1"):
        noteShare.create_user("user1", "password1")
    if not noteShare.authenticate("user2", "password2"):
        noteShare.create_user("user2", "password2")
    if not noteShare.authenticate("user3", "password3"):
        noteShare.create_user("user3", "password3")
    noteShare.conn.commit()

    auth_status_user1, user1_id = noteShare.get_user_id("user1", "password1")
    auth_status_user2, user2_id = noteShare.get_user_id("user2", "password2")
    print(user1_id)

    
    note = "It is a sunny day"
    # noteShare.create_note(user1_id, note)
    # noteShare.share_notes(1, user2_id)
    auth_status_notes, note_id = noteShare.get_note_id(note)
    print(note_id)
    notes_user1 = noteShare.get_note_from_user_id(user1_id)
    print("Notes for User 1:", notes_user1)
    notes_user2 = noteShare.get_note_from_user_id(user2_id)
    print("Notes for User 2:", notes_user2)

if __name__ == '__main__':
    main()

    


    
    
