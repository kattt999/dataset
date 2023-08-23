import sqlite3

class UserRecordBackend:
    def __init__(self):
        self.conn = sqlite3.connect('user_records.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        create table if not exists user_records(
        id interger primary key,
        name text,
        age integer,
        email text,
        location text
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def import_records(self, records):
        query = "insert into user_records (name, age, email, location) values(?,?,?,?)"
        self.conn.executemany(query, records)
        self.conn.commit()

    def search_records(self, age_from, age_to, location):
        query = """
        select * from user_records
        where age between ? and ? and location like ?
        """
        params = (age_from, age_to, f"%{location}%")
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()
    
    def get_all_records(self):
        self.conn.execute("select * from user_records")
        return self.c.fetchall()
    
    def add_record(self, name, age, email, location):
        query = "Insert into user_records (name, age, email, location) values (?, ?, ?, ?)"
        params = (name, age, email, location)
        self.c.execute(query, params)
        self.conn.commit()

    def update_record(self, record_id, name, age, email, location):
        query ="""
        update user_records set name = ?, age = ?, email = ?, location = ?
        where id = ?
        """
        params = (name, age, email, location, record_id)
        self.c.execute(query, params)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
def main():
    backend = UserRecordBackend()

    while True:
        print("1. Add Record")
        print("2. Update Record")
        print("3. Search Records")
        print("4. Show All Records")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            email = input("Email: ")
            location = input("Location: ")
            backend.add_record(name, age, email, location)
            print("Record added successfully!")

        elif choice == "2":
            record_id = int(input("Enter the ID of the record to update: "))
            name = input("Name: ")
            age = int(input("Age: "))
            email = input("Email: ")
            location = input("Location: ")
            backend.update_record(record_id, name, age, email, location)
            print("Record updated successfully!")

        elif choice == "3":
            age_from = int(input("Age From: "))
            age_to = int(input("Age To: "))
            location = input("Location: ")
            records = backend.search_records(age_from, age_to, location)
            print("Search Results:")
            for record in records:
                print(record)

        elif choice == "4":
            records = backend.get_all_records()
            print("All Records:")
            for record in records:
                print(record)

        elif choice == "5":
            backend.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
