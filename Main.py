import mysql.connector
from mysql.connector import Error
from Functions import *

if __name__ == "__main__":

    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Enter the user password
        'database': 'world'
    }

    try:
        connection = mysql.connector.connect(**config)
        print('The database connection has been established successfully.')
    except Error as err:
        print(err)
    else:
        choice = 0

        while choice != 5:
            print("\n 1. Output Query ")
            print("2. Insert Data ")
            print("3. Update Data ")
            print("4. Start Transaction ")
            print("5. Exit from the system ")
            choice = int(input())

            if choice == 1:
                Show_Results(connection)
            elif choice == 2:
                insert(connection)
            elif choice == 3:
                update(connection)
            elif choice == 4:
                transaction(connection)

        connection.close()
        print('The connection has been ended.')
