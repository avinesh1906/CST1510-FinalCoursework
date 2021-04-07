# import libraries
import mysql.connector
import socket
import pickle
from _thread import *
from datetime import datetime

HOST = '127.0.0.1'  # <-- insert the HOST of the database
PORT = 3306  # <-- insert the PORT of the database

mydb = mysql.connector.connect(
    user='root',  # <-- insert the username
    password='Cm3tc7At',  # <-- insert the user password
    host=HOST,
    database='sushi',  # <-- insert the database name here
    port=PORT,
    raise_on_warnings=True,  # whether warnings should raise exceptions.
)


# function to keep the connection active
def connection_Thread(client_Socket):
    # Cursor is used to execute statements to communicate with the MYSQL database
    # buffered=True enable to execute different queries
    database = mydb.cursor(buffered=True)

    # exception handling
    try:
        # infinite loop to prevent the connection from closing
        while True:
            # Retrieve the categories name from MyDb
            database.execute("SELECT * FROM categories ")
            categories_data = database.fetchall()

            # Retrieve the categories name from MyDb
            database.execute("SELECT * FROM food ")
            food_data = database.fetchall()

            # Retrieve the categories name from MyDb
            database.execute("SELECT * FROM platters ")
            platter_data = database.fetchall()

            # Retrieve the categories name from MyDb
            database.execute("SELECT * FROM products ")
            products_data = database.fetchall()

            database_list = [categories_data, food_data, platter_data, products_data]

            '''Send data to the client'''
            # pickle will allow to send a list to the client
            server_message = pickle.dumps(database_list)
            client_Socket.send(server_message)

            '''receive the order.csv from the client'''
            order_details = pickle.loads(client_Socket.recv(1024))

            for orders in order_details:

                '''store each transaction in transaction.txt'''
                with open('files/transaction.txt', 'a') as transaction_file:
                    transaction_file.writelines(f"DATE OF PURCHASE: {datetime.date(datetime.now())} "
                                                f"ITEM PURCHASED: {orders[0]} QUANTITY PURCHASED: {orders[1]}\n")

                # check whether to extract from food or platters according to categoryID
                if int(orders[3]) <= 29:
                    # sql to retrieve the qty from food table
                    currentStockSQL = """SELECT qty FROM food WHERE FoodID = %s"""
                    # tuple to store the categoryID
                    stockLevel_Tuple = (orders[3],)
                    # execute the query
                    database.execute(currentStockSQL, stockLevel_Tuple)

                    for row in database:
                        # calculate the new stock level
                        newStock = row[0] - int(orders[1])
                        # sql to update food table
                        stockControl_SQL = " UPDATE food SET qty = %s WHERE FoodID = %s"

                else:
                    # sql to retrieve the qty from platters table
                    currentStockSQL = """SELECT qty FROM platters WHERE plattersID = %s"""
                    # tuple to store the categoryID
                    stockLevel_Tuple = (orders[3],)
                    # execute the query
                    database.execute(currentStockSQL, stockLevel_Tuple)
                    for row in database:
                        # calculate the new stock level
                        newStock = row[0] - int(orders[1])
                        # sql to update platter table
                        stockControl_SQL = " UPDATE platters SET qty = %s WHERE plattersID = %s"
                # execute the sql to update the qty
                order_Tuple = (newStock, orders[3])
                database.execute(stockControl_SQL, order_Tuple)
                mydb.commit()

    except socket.error as err:
        # print the error occured
        print(f"Error occurred: {err} ")
        # close the socket
        client_Socket.close()


def main():
    # Create a server socket
    # AF.INET refers to the address family IPV4
    # SOCK_STREAM means connection oriented TCP protocol
    try:
        # start the connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Socket successfully created")
            # Bind
            s.bind(('localhost', 69))

            # listen
            s.listen(10)
            print("Waiting for connection")

            # forever loop until client close the application
            while True:
                # Accept the connection
                client_Socket, address = s.accept()
                print('Connected to :', address[0], ':', address[1])

                # Start a new thread to keep the connection
                start_new_thread(connection_Thread, (client_Socket,))
    # print any error if occured
    except socket.error as err:
        print(f"{err} occurred during socket creation")
        s.close()


if __name__ == '__main__':
    main()
