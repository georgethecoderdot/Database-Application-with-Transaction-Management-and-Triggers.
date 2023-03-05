from mysql.connector import Error, errorcode


def search(connection, table, select, condition, where):
    try:
        cursor = connection.cursor()
        cursor.execute(f'SELECT {select} FROM {table} WHERE {where}="{condition}";')
        country_code = cursor.fetchone()
    except Error as err:
        print(err)
        cursor.close()
        return None
    else:
        cursor.close()
        return country_code[0]



def insert(connection, transaction_mode=False, transaction_table_choice=-1):
    if transaction_mode is False:
        choice = int(input("\nPress 0 to insert a country.\nPress 1 to insert a city.\n"))
    else:
        choice = transaction_table_choice

    if choice == 0:
        code = input("Press the code of country : ")
        name = input("Press the name of country : ")
        code2 = input("Press the next code of country : ")
        query = f'INSERT INTO country (Code, Name, Code2) VALUES("{code}", "{name}", "{code2}");'

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            print(f'\nCountry {name}  successfully added.\n')
        except Error as err:
            connection.rollback()
            print(err)
        finally:
            cursor.close()
    
    elif choice == 1:
        cityname = input("Press the name of the city: ")
        countryname = input("Press the name of the country: ")
        district = input("Press the name of district: ")
        countrycode = search(connection, "country", "Code", countryname, "Name")
        query = f'INSERT INTO city (Name, CountryCode, District) VALUES("{cityname}", "{countrycode}", "{district}");'
        
        if countrycode is not None:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                print(f'\nCity {cityname}  successfully added.\n')
            except Error as err:
                connection.rollback()
                print(err)
            finally:
                cursor.close()
        else:
            print("The country is not present in the database.")


def fetch(connection, country_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f'SELECT Code FROM country WHERE Name="{country_name}";')
        res = cursor.fetchone()
    except Error as err:
        print(err)
        cursor.close()
        return None
    finally:
        return res[0]

def update(connection, mode=False, tablechoice = -1):
    if mode is False:
        choice = int(input("\n Press 0 to modify a country's information in the database\n "
                           "Press 1 to modify a city's information in the database\n"))
    else:
        choice = tablechoice


    if(choice == 0):
        country = input("please input the name of the country whose record you want to modify: ")
        if search(connection, "country", "Name", country, "Name") is not None:
            countryname = input("Press the  name of the new country : ")
            countrycode = input("Press the new code of the  country: ")
            countrycode2 = input("Press the new second  code of the country: ")

            try:
                cursor = connection.cursor()
                cursor.execute(f'UPDATE country SET Name="{countryname}", Code="{countrycode}", Code2="{countrycode2}" WHERE Name="{country}";')
                connection.commit()
                print(f'\n{country}  successfully modified .\n')
            except Error as err:
                connection.rollback()
                print(err)
            finally:
                cursor.close()
        else:
            print("Country you want to modify do not found.")
    else:
        city = input("please input the name of city whose record you want  to update: ")

        if search(connection, "city", "Name", city, "Name") is not None:
            cityname = input("Press the name of the new city: ")
            citydistrict = input("Press the name of the new district: ")
            countryname = input("Please Specify the name of the country that the city is part of: ")
            citycode = fetch(connection, countryname) 

            if citycode is not None:

                try:
                    cursor = connection.cursor()
                    cursor.execute(f'UPDATE city SET Name="{cityname}", District="{citydistrict}", CountryCode="{citycode}" WHERE Name="{city}";')
                    connection.commit()
                    print(f'\n{city}  successfully modified.\n')
                except Error as err:
                    connection.rollback()
                    print("The Update process was unsuccessful.")
                    print(err)
                finally:
                    cursor.close()
            else:
                print(f'The Country {countryname} do not found')
        else:
            print("City you want to modify do not found.")


def transaction(connection):
    
    choice = int(input("Press  1 to initiate  a transaction for insertion , "
                       "or enter 0 to initiate a transaction for updating: "))
    table = input("Please select the table for which you want to start a transaction: ")

    try:
        cursor = connection.cursor()
        if table == "country":
            query = f'LOCK TABLE country WRITE;'
        else:
            query = f'LOCK TABLE city WRITE, country READ;'
            
        cursor.execute(query)
    except Error as err:
        cursor.close()
        print(err)
    finally:
        if choice == 1:
            insert(connection, True, (0 if table == "country" else 1))
        else:
            update(connection, True, (0 if table == "country" else 1))

        cursor.close()
        
    try:
        cursor = connection.cursor()
        cursor.execute(f'UNLOCK TABLES;')
    except Error as err:
        cursor.close()
        print(err)
    finally:
        cursor.close()
        print(f'Table {table} unlocked successfully.')

def Show_Results(connection):
	choice = int(input("\n Press 0 to search for a country \n Press 1 to search for a city\n"))

	if choice == 0:
		name = input("Press name of country: ")
		query = f'SELECT * FROM country WHERE Name="{name}";'

		try:
			cursor = connection.cursor()
			cursor.execute(query)
			row = cursor.fetchone()
			while row is not None:
				print(row)
				row = cursor.fetchone()
			print()
		except Error as err:
			print(err)
			cursor.close()
		finally:
			cursor.close()

	elif choice == 1:
		name = input("Press name of city: ")
		query = f'SELECT * FROM city WHERE Name="{name}";'

		try:
			cursor = connection.cursor()
			cursor.execute(query)
			row = cursor.fetchone()
			while row is not None:
				print(row)
				row = cursor.fetchone()
			print()
		except Error as err:
			print(err)
			cursor.close()
		finally:
			cursor.close()
