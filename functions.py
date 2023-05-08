import sqlite3
import sys

import hashlib


class database_appointments:

    def create_appointment_table(self):
        '''Admin function for creating an appointments table.'''
        print("\n\nCreate Appointments Table\n")

        file_created = False
        confirmation = ""
        con = sqlite3.connect('msaBooking.db')
        cur = con.cursor()
        while confirmation != '2' or file_created is not True :
        #Validation: while loop repeats until user gives an interpreted response.

            try:
                cur.execute('''CREATE TABLE tblAPPOINTMENTS (
                    cus_name text, 
                    cus_address text, 
                    cus_phone text, 
                    staff_number text, 
                    date_time text
                )''')
                con.commit()
                con.close()
                print("Appointments file created.")
                file_created = True
                return

            except sqlite3.OperationalError:
                print("An appointments table may already exist. Would you like to overwrite it? \n 1. Confirm \n 2. Cancel")
                confirmation = input("Enter:")

                if confirmation == '1':
                    cur.execute('''DROP TABLE tblAPPOINTMENTS''')
                    con.commit()
                elif confirmation == '2':
                    return
                else:
                    print("Please enter a valid input.")


    def new_appointment(self, staff_number):
        '''Function for creating new appointments.'''

        print("\n\nCreate new appointment\n")

        print("Please enter new appointment data.")
        cus_name = input("Customer name: ")
        cus_address = input("Address: ")
        cus_phone = input("Phone: ")
        date_time = input("Date of appointment (dd/mm/yyyy): ")

        con = sqlite3.connect('msaBooking.db')
        cur = con.cursor()

        try:
            cur.execute("""INSERT INTO tblAPPOINTMENTS
                         VALUES ((?), (?), (?), (?), (?))""", (cus_name, cus_address, cus_phone, staff_number, date_time)
                    )
            
            con.commit()
            con.close()
            print("New appointment booked.")

        except sqlite3.OperationalError:
            print("Error: Table not found. Please contact an administrator to create or recover the table.")

        except:
            print("Error")

    def edit_existing_appointment(self, staff_number):
        print("\n\nEdit existing Appointments. \n")

        #get old data
        print("Please enter the customer name and the original date of the appointment you want to edit.")
        cus_name_original = input("Enter name: ")
        date_time_original = input("Enter date: ")


        con = sqlite3.connect('msaBooking.db')
        cur = con.cursor()

        cur.execute("""SELECT * FROM tblAPPOINTMENTS 
        WHERE cus_name = (?) and date_time = (?)
        """, (cus_name_original, date_time_original))
        print(cur.fetchall())

        #get new data
        print("Please enter new appointment data.")
        cus_name = input("Customer name: ")
        cus_address = input("Address: ")
        cus_phone = input("Phone: ")
        date_time = input("Date of appointment (dd/mm/yyyy): ")


        #change database entry to new information
        cur.execute("""UPDATE tblAPPOINTMENTS 
                        SET cus_name = ?, cus_address = (?), cus_phone = (?), staff_number = (?), date_time = (?) 
                        WHERE cus_name = (?) AND date_time = (?) 
                        """, (cus_name, cus_address, cus_phone, staff_number, date_time, cus_name_original, date_time_original))


        #cur.execute("""DELETE FROM tblAPPOINTMENTS WHERE cus_name = (?) AND date_time = (?)
        #        """)
        
        con.commit()
        con.close()
        
        print("Update successful!")
        
        


class database_staff:

    #ADMIN FUNCTIONS
    def create_staff_table(self):
        '''Admin function for creating a staff table.'''
        print("\n\nCreate Staff Table\n")

        file_created = False
        confirmation = ""
        con = sqlite3.connect('msaBooking.db')
        cur = con.cursor()
        while confirmation != '2' or file_created is not True :
        #Validation: while loop repeats until user gives an interpreted response.

            try:
                cur.execute('''CREATE TABLE tblSTAFF (
                    staff_num text,
                    staff_name text,
                    staff_pass text
                )''')
                con.commit()
                con.close()
                print("Staff file created.")
                file_created = True
                return

            except sqlite3.OperationalError:
                print("A staff table may already exist. Would you like to overwrite it? \n 1. Confirm \n 2. Cancel")
                confirmation = input("Enter:")

                if confirmation == '1':
                    cur.execute('''DROP TABLE tblSTAFF''')
                    con.commit()
                elif confirmation == '2':
                    return
                else:
                    print("Please enter a valid input.")
        


    def new_staff_login(self):
        '''Admin function for creating new staff member logins.'''

        print("\n\nCreate new staff login")
    
        valid = False
        while valid is not True:
        

            print("\nPlease enter new user data.")
            staff_number = input("Please enter your staff number: ")

            if len(staff_number) == 6:
                staff_name = input("Please enter your name: ")
                staff_password = input("Please enter a password: ").encode()
                valid = True
            
            else:
                print("Please enter a staff number which is 6 characters long.")

        hashlib_sha1 = hashlib.sha1(staff_password)
        staff_password_hashed = hashlib_sha1.hexdigest()
        #Encodes the staff passwords and returns a hash value

        con = sqlite3.connect('msaBooking.db')
        cur = con.cursor()

        try:
            cur.execute("INSERT INTO tblSTAFF VALUES((?), (?), (?))", (staff_number, staff_name, staff_password_hashed))
            con.commit()
            con.close()
            print("New login created.")

        except sqlite3.OperationalError:
            print("Error: Table not found. Please contact an administrator to create or recover the table.")



