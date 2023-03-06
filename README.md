# Database-Application-with-Transaction-Management-and-Triggers.

This is a program that allows the user to interact with a MySQL database. 

The program has four main functionalities: querying, inserting data, updating data, and starting a transaction.

In the main.py file, the program establishes a connection to the database using the credentials provided, 

and then it presents a menu to the user where they can choose one of the functionalities. 

Depending on the choice, the program calls the appropriate function from the Functions.py file.

The Functions.py file contains several functions that interact with the database. 

The search function takes in a connection object, a table name, a column to select, a condition, and a value to search for,

and it returns the first value found in the column that matches the condition. 

The insert function takes in a connection object, and it prompts the user to input data for either a country or a city. 

If the user chooses to insert a city, the function calls the search function to get the country code, and then it inserts the data into the city table. The fetch function takes in a connection object and a country name and returns the code of the country. The update function takes in a connection object and prompts the user to choose between updating a country or a city. If the user chooses to update a city, the function calls the fetch function to get the country code, and then it updates the data in the city table.

Overall, this program provides a  interface for interacting with a MySQL database, allowing the user to query, insert, and update data, 

as well as start a transaction if necessary. 
