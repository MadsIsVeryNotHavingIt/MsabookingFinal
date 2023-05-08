
import sqlite3
import hashlib
import sys
#from flask import Flask, render_template, request
from functions import database_appointments, database_staff





def startup():
    '''user selects a login option. SCRAPPED'''


    print("Select login option: \n 1. Staff member login \n 2. Administrator login")
    login_selection = input("Enter: ")
    if login_selection == '1':
        staff_login()
    elif login_selection == '2':
        admin_login()
        
   #Branches to staff login page or admin login page at the user's choice.


def staff_login():
    '''Login for regular staff members. SCRAPPED'''

    print("\nStaff Login")
    
    forced_login = True    
    for tries in range(0,3):
        print("\nPlease enter your login details:")
        staff_number = input("Staff number: ")
        password = input("Password: ")
        try:
            #cur.execute("SELECT staff_password FROM tblSTAFF WHERE staff_num = (?)", (staff_number))
            #fetches the staff password from the database via searching by staff number
            if cur.fetchall() == password or forced_login == True:
                print("Login successful!")
                menu(admin = False, staff_number = staff_number)
        except:
            print("Incorrect login details.")
            tries = tries + 1
    print("Too many attempts! The program will now shut down.")
    

def admin_login():
    '''Login for administrators. SCRAPPED'''

    tries = 0
    logged_in = False
    print("\n\nAdmin Login\n")
    while tries < 3 and logged_in == False:
        print("Please enter your login details:")
        staff_number = input("Staff number: ")
        password = input("Password: ")

        if staff_number == 'template_number' and password == 'template_password':
            print("Login successful!")
            logged_in = True
            menu(admin = True, staff_number = staff_number)
        
        else:
            print("Incorrect login details.\n")
            tries = tries + 1
    if tries >= 3:
        print("Too many attempts!")
    print("The program will now close.")



def login():
    '''Login for staff members and administrators.'''

    tries = 0
    logged_in = False
    print("\n\nLogin.\n")

    con = sqlite3.connect('msaBooking.db')
    cur = con.cursor()

    while tries < 3 and logged_in == False:

        print("Please enter your login details:")
        staff_number = input("Staff number: ")
        password = input("Password: ")

        

        #admin login
        if staff_number == 'template_number' and password == 'template_password':
            print("Login successful!")
            logged_in = True
            menu(admin = True, staff_number = staff_number)
        
        password_encode = password.encode()
        hashlib_sha1 = hashlib.sha1(password_encode)
        staff_password_hashed = hashlib_sha1.hexdigest()
        #hashes the inputted password value

        cur.execute("SELECT staff_pass FROM tblSTAFF WHERE staff_num = (?)", ((staff_number,)))
        #fetches the staff password from the database via searching by staff number

        if str(cur.fetchall()) == ("[('" + staff_password_hashed + "',)]"):
            print("Login successful!")
            menu(admin = False, staff_number = staff_number)


        else:
            print("Incorrect login details.\n")
            tries = tries + 1

    if tries >= 3:
        print("Too many attempts!")
    print("The program will now close.")
    con.close()



def menu(admin, staff_number):
    '''Main menu for staff members and administrators. Behaviour changes depending on admin variable.'''

    print("\nMain Menu")
    

    con = sqlite3.connect('msaBooking.db')
    cur = con.cursor()

    print("Appointments:")
    cur.execute("""SELECT * FROM tblAPPOINTMENTS""")
    [print(row) for row in cur.fetchall()]

    con.close()

    user_select = ""

    if admin == False:
        while user_select not in range(0,3):
            #validation loop until user enters an interpretable input

            print("\nPlease select a page.")
            print(" 1. Book new appointment ")
            print(" 2. View existing appointment")
            print(" 3. Log out")

            try:
                user_select = int(input("Enter: "))
                
            except ValueError:
                pass

            if user_select == 1:
                print("Launching 'book new apppointment' page.")
                database_appointments.new_appointment(self = "", staff_number = staff_number)
            elif user_select == 2:
                print("Launching 'View existing appointment' page.")
                database_appointments.edit_existing_appointment(self = "", staff_number = staff_number)
            elif user_select == 3:
                sys.exit("Logging out. The program will now close.")
            else:
                print("Error. Please enter a valid input.")
    
    elif admin == True:
        while user_select not in range(1,6):
        #validation loop until user enters an interpretable input

            print("\nPlease select a page. ")
            print(" 1. Book new appointment")
            print(" 2. View existing appointment")
            print(" 3. Create new staff login")
            print(" 4. Create staff table")
            print(" 5. Create appointments table")
            print(" 6. Log out")

            try:
                user_select = int(input("Enter: "))
                
            except ValueError:
                pass

            if user_select == 1:
                print("Launching 'book new apppointment' page.")
                database_appointments.new_appointment(self = "", staff_number = staff_number)

            elif user_select == 2:
                print("Launching 'View existing appointment' page.")
                database_appointments.edit_existing_appointment(self = "", staff_number = staff_number)

            elif user_select == 3:
                database_staff.new_staff_login(self = "")

            elif user_select == 4:
                database_staff.create_staff_table(self = "")

            elif user_select == 5:
                database_appointments.create_appointment_table(self = "")

            elif user_select == 6:
                sys.exit("Logging out. The program will now close.")

            else:
                print("Error. Please enter a number from 1 to 6.")

    #cur.execute('''SELECT ALL cus_name, cus_address, cus_phone, staff_number, date_time FROM tblAPPOINTMENTS ORDER BY date_time DESC''')
    #print(cur.fetchall())

def staff_menu(staff_number):
    '''Main menu for staff members.'''

    #Appointments display goes here.
    print("\nMenu.")
    user_select = ""
    while user_select != '1' and user_select != '2' and user_select != '3':
    #validation loop until user enters an interpretable input

        print("\nPlease select a page. \n 1. Book new appointment \n 2. View existing appointment \n 3. Log out")
        user_select = input("Enter: ")
        if user_select == '1':
            print("Launching 'book new apppointment' page.")
            database_appointments.new_appointment(self = "", staff_number = staff_number)
        elif user_select == '2':
            print("Launching 'View existing appointment' page.")
            database_appointments.view_appointment(self = "")
        elif user_select == '3':
            sys.exit("Logging out. The program will now close.")
        else:
            print("Error. Please enter a valid input.")

    #cur.execute('''SELECT ALL cus_name, cus_address, cus_phone, staff_number, date_time FROM tblAPPOINTMENTS ORDER BY date_time DESC''')
    #print(cur.fetchall())


def admin_menu(staff_number):
    '''Main menu for administrators.'''

    #Appointments display goes here.
    print("\nMenu.")
    user_select = ""
    while user_select not in range(1,6):
    #validation loop until user enters an interpretable input

        print("\nPlease select a page. ")
        print(" 1. Book new appointment")
        print(" 2. View existing appointment")
        print(" 3. Create new staff login")
        print(" 4. Create staff table")
        print(" 5. Create appointments table")
        print(" 6. Log out")

        try:
            user_select = int(input("Enter: "))
            
        except ValueError:
            pass

        if user_select == 1:
            print("Launching 'book new apppointment' page.")
            database_appointments.new_appointment(self = "", staff_number = staff_number)

        elif user_select == 2:
            print("Launching 'View existing appointment' page.")
            database_appointments.view_appointment(self = "")

        elif user_select == 3:
            database_staff.new_staff_login(self = "")

        elif user_select == 4:
            database_staff.create_staff_table(self = "")

        elif user_select == 5:
            database_appointments.create_appointment_table(self = "")

        elif user_select == 6:
            sys.exit("Logging out. The program will now close.")

        else:
            print("Error. Please enter a number from 1 to 6.")

staff_number = '000123'

login()

