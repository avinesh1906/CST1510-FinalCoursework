# import libraries
from tkinter import *
from tkinter import messagebox
import socket
import pickle
import csv
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# global variable to store the amount payable, the change for cash payment, messagecode and timer
amount = 0
change = 0
messagecode = 0
timer = 6

# dict to store the file name of each image(VALUE) according to the categoryID(KEY)
sushiImageDict = {"1": "maki.png", "2": "nigiri.png", "3": "gunkan.png",
                  "4": "flowergunkans.png", "5": "californiaroll.png",
                  "6": "rainbowrolls.png", "7": "futomaki.png", "8": "sashimi.png",
                  "9": "platter.png"}
# Create a client socket
client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects the client to the server IP address
client_Socket.connect(('localhost', 69))


def background_operation():
    """
    background_operation takes no arguments.
    .
    .
    It will carry out the following operations:
    1) Make sure all the csv file is empty at the start to prevent dublicates data
    2) If csv is not empty, empty it.
    3) Receive the list that contains all records of the database
    4) Create respective csv file to store category, products, food and platters details
    """
    # list to store the name of files
    file_list = ["category.csv", "food.csv", "order.csv", "platter.csv", "product.csv"]
    # remove any data in the file before execution if have any.
    for fileName in file_list:
        if os.stat(f"files/{fileName}").st_size != 0:
            with open(f"files/{fileName}", "w") as category_file:
                category_file.truncate(0)

    # extract the categories details from the server
    database_list = pickle.loads(client_Socket.recv(2048))
    sushi_Categories = database_list[0]
    food_Details = database_list[1]
    platter_Details = database_list[2]
    product_Details = database_list[3]

    # create a text file to store the sushi_Categories
    for categories_item in sushi_Categories:
        categoryTemp_List = []
        with open("files/category.csv", 'a') as category_File:
            categoryTemp_List.append(f'{categories_item[0]},{categories_item[1]}\n')
            category_File.writelines(categoryTemp_List)

    # create a text file to store the sushi_Categories
    for food_content in food_Details:
        food_List = []
        with open("files/food.csv", 'a') as Food_File:
            food_List.append(
                f'{food_content[0]},{food_content[1]},{food_content[2]},{food_content[3]},{food_content[4]}\n')
            Food_File.writelines(food_List)

    # create a text file to store the sushi_Categories
    for platter_content in platter_Details:
        platter_List = []
        with open("files/platter.csv", 'a') as platter_File:
            platter_List.append(f'{platter_content[0]},{platter_content[1]},{platter_content[2]},{platter_content[3]},'
                                f'{platter_content[4]}\n')
            platter_File.writelines(platter_List)

    # create a text file to store the sushi_Categories
    for product_item in product_Details:
        product_List = []
        with open("files/product.csv", 'a') as product_File:
            product_List.append(f'{product_item[0]},{product_item[1]}\n')
            product_File.writelines(product_List)


# class to start the application
class App(Tk):
    """
        App Class
        Tk: Toplevel widget of Tk which represents mostly the main window of an application.
            It has an associated Tcl interpreter
        .
        .
        This class will:
        1) Create a frame
        2) Format the frame
        3) Allow to switch frame by destroying the previous used frame

    """

    # initialise constructor
    def __init__(self):
        # super() with Multiple Inheritance
        super(App, self).__init__()
        self._frame = None
        self.title("Vending Machine")
        self.switchFrame(Welcome)
        # prevent the user from closing the window directly
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(0, 0)
    # function to switch Frame
    def switchFrame(self, class_Frame):
        newFrame = class_Frame(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = newFrame
        self._frame.pack()

    # ask the window if he/she really wants to quit
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


class Welcome(Frame):
    """
    Welcome Class
    Frame: Frame widget which may contain other widgets and can have a 3D border.
    .
    .
    This function will display the welcome message and prompt the user:
    1) Proceed
    2) Exit the GUI
    """

    # initialise constructor
    def __init__(self, master):
        # calls constructor from the superclass
        Frame.__init__(self, master)
        global timer
        global messagecode
        # resize the window
        self.master.geometry("900x700+325+25")
        # function call
        background_operation()
        # set timer, messagecode to default
        timer = 6
        messagecode = 0

        '''Frame to store all the widgets'''
        window_Frame = Frame(self, width=900, height=700, bg="NavajoWhite4")
        window_Frame.pack(side=TOP)

        '''Frame to store the details'''
        details_Frame = Frame(window_Frame, width=700, height=650, highlightthickness="5", bg="PeachPuff2")
        details_Frame.place(x=100, y=25)

        # Welcome Message
        Label(details_Frame, text="WELCOME To", font=("Courier", 50), bg="PeachPuff2",).place(x=150, y=50)
        Label(details_Frame, text=" ケシャフ ", font=("Courier", 44), bg="PeachPuff2",).place(x=190, y=150)
        Label(details_Frame, text="Sushi", font=("Courier", 44), bg="PeachPuff2",).place(x=250, y=225)

        '''Display the logo'''
        logo = Image.open("pictures/logo(3).png")
        logoTk = ImageTk.PhotoImage(logo)
        picture_Label = Label(details_Frame, image=logoTk, )
        picture_Label.image = logoTk
        picture_Label.place(x=180, y=410)

        # Button to proceed to the main menu
        Button(details_Frame, text="Order Now!", font=("Courier", 20), bg="NavajoWhite4",
               command=lambda: master.switchFrame(Menu)).place(x=245, y=315)


class Menu(Frame):
    """
        Class for the main menu
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This  function will allow the client to:
        1) Choose a/many sushi(es)
        2) View the available sushi using matplotlib
        3) Allow new transactions
        4) Proceed to view order details

    """

    # initialise constructor
    def __init__(self, master):
        # calls constructor from the superclass
        Frame.__init__(self, master)

        # resize the window
        self.master.geometry("900x700+325+25")

        def extract(categoryID):
            """
                extract is a function which has categoryID as argument.
                :param categoryID : string
                .
                .
                This function will:
                1) Display the pie chart
                2) Display the product name of a specific category
            """

            '''Frame for details of each product of a specific categories'''
            products_Frame = Frame(details_Frame, width=210, height=630, highlightthickness="3", bg="PeachPuff2")
            products_Frame.place(x=210, y=0)

            '''Frame to display the Pie chart'''
            pieChart_Frame = Frame(details_Frame, width=400, height=350, bg="PeachPuff2", highlightthickness="3")
            pieChart_Frame.place(x=420, y=0)

            # global variable to store the categoryID to be used to display that category's specific picture
            global pictureID
            pictureID = categoryID
            # list to store the details of each product pressed
            button_list = []
            # extract the food/platter details from the food/platter.csv
            if int(categoryID) <= 7:  # only for single type sushi
                # open the following file in read mode
                with open('files/food.csv', 'r') as food_read:
                    # read the content of the file
                    foods = csv.reader(food_read)
                    food_list = list(foods)
                    # loop through the content of the food_list
                    for food_Details in food_list:
                        # check if categoryID of category.csv matches the one in food.csv
                        if categoryID == food_Details[1]:
                            # If yes, open product.csv in read mode
                            with open('files/product.csv', 'r') as product_read:
                                # read the content of the file
                                product = csv.reader(product_read)
                                product_list = list(product)
                                # loop through the list of product_list
                                for product_Details in product_list:
                                    # check if productID in food.csv matches the one in product.csv
                                    if food_Details[2] == product_Details[0]:
                                        # if yes, append the foodID, productName, price and quantity to button_list
                                        button_list.append([food_Details[0], product_Details[1], food_Details[3],
                                                            food_Details[4]])
            else:  # for platter sushi
                # open platter.csv in read mode
                with open('files/platter.csv', 'r') as platter_read:
                    # read content of platter file
                    platter = csv.reader(platter_read)
                    platter_List = list(platter)
                    # loop through platter_list
                    for platter_Details in platter_List:
                        # check if categoryID in category.csv matches the one in platter.csv
                        if categoryID == platter_Details[1]:
                            # If yes, append name, platterName, price and quantity to button_list
                            button_list.append([platter_Details[0], platter_Details[2], platter_Details[3],
                                                platter_Details[4]])

            yAxis = 28  # starting value for yAxis
            # delete old widgets
            for product_widget in products_Frame.winfo_children():
                product_widget.destroy()
            Label(products_Frame, text="Choose a Product:", font=("Courier", 13), bg="PeachPuff2").place(x=10, y=5)
            # replace with new widgets when category button clicked
            for Product_list in button_list:
                # display the products related to that specific category
                products_Button = Button(products_Frame, text=Product_list[1],
                                         command=lambda Product=Product_list: show_details(Product), width=20,
                                         height=2, font=("Courier", 11), bg="NavajoWhite4")
                products_Button.place(x=10, y=yAxis)  # position to place the button

                yAxis += 65  # increase the y-Axis according to number of item

            '''Display the pie chart of that specific category'''

            def realValue_format(values):
                """
                This function will display the real value instead of percentage
                :param values: int
                :return: my_format
                """

                def my_format(pct):
                    total = sum(values)
                    val = int(round(pct * total / 100.0))
                    return '{v:d}'.format(v=val)

                return my_format

            # list to store the product name and quantity
            product_Name = [name[1] for name in button_list]
            product_Qty = [int(quantity[3]) for quantity in button_list]

            fig = Figure()  # create a figure object
            fig.patch.set_facecolor('#f0cbab')

            ax = fig.add_subplot(111)  # add an Axes to the figure

            ax.pie(product_Qty, radius=0.9, labels=product_Name, autopct=realValue_format(product_Qty), startangle=270,
                   center=(1, 50))
            ax.set_title('Availability of Sushi', fontdict={'fontsize': 15}, x=0.5, y=0.95)
            chart1 = FigureCanvasTkAgg(fig, pieChart_Frame)
            chart1.get_tk_widget().place(x=-150, y=-40)

        def NEXT():
            """
            This function takes no argument.
            .
            .
            It will carry out the following operation:
            1) check if the order qty is greater than the stock qty
            2) Display any error if order > stock
            3) Append data to the order.csv
            4) Switch to ProductDetails Frame
            :return: nothing
            """
            # global variable to store the user's purchase qty and
            global purchase_qty
            # retrieve the user's qty
            purchase_qty = OrderProductQty
            # check if purchase_qty is more than available stock qty
            if int(purchase_qty) > int(stockQty):
                # display an error if purchase qty is more than stock qty
                messagebox.showerror("Error", "Cannot place order above the stock level")
                purchase_qty = OrderProductQty

            else:
                # list to store each order's details
                order_details = []
                # open order.csv in append mode
                with open('files/order.csv', 'a') as order:
                    order_details.append(f'{productName},{purchase_qty},{IndividualPrice},{IndividualID}\n')
                    order.writelines(order_details)
                # switch frame to Receipt
                master.switchFrame(ProductDetails)

        def show_details(details):
            """
            This function takes details as argument.
            :param details: list
            :return: nothing
            .
            .
            This function will carry out the following operations:
            1) Display the id, price, name and picture according to the categoryID
            2) Prompt the user for quantity
            3) Button to move to next window
            """
            ''' Frame to display sushi details'''
            Details_frame = Frame(details_Frame, width=400, height=290, bg="PeachPuff2", highlightthickness="3")
            Details_frame.place(x=420, y=350)

            # global variables for future reference
            global IndividualID
            global stockQty
            global IndividualPrice
            global productName
            global OrderProductQty

            OrderProductQty = 0
            IndividualPrice = details[2]
            IndividualID = details[0]

            def increase():
                global OrderProductQty
                if OrderProductQty < 10:
                    OrderProductQty += 1
                    TEXT = f"Quantity: {OrderProductQty}"
                    Qty.config(text=TEXT)
                    Next_Button['state'] = 'normal'

            def decrease():
                global OrderProductQty
                if OrderProductQty > 0:
                    OrderProductQty -= 1
                    TEXT = f"Quantity: {OrderProductQty}"
                    Qty.config(text=TEXT)
                if OrderProductQty <= 0:
                    Next_Button['state'] = 'disable'

            productID = "ID: " + str(details[0])
            productName = details[1]
            productPrice = "Price: Rs " + str(details[2])
            stockQty = details[3]
            # delete old widgets
            for details_widget in Details_frame.winfo_children():
                details_widget.destroy()
            # display the Name, productID and price
            if len(productName) >= 15:
                shorten_Text = productName[0:12] + "..."
                Label(Details_frame, text=shorten_Text, font=("courier", 22), bg="PeachPuff2", ).place(x=100, y=0)

            else:
                Label(Details_frame, text=productName, font=("courier", 22), bg="PeachPuff2", ).place(x=100, y=0)

            Label(Details_frame, text=productID, font=("courier", 17), bg="PeachPuff2", ).place(x=10, y=50)
            Label(Details_frame, text=productPrice, font=('courier', 15), bg="PeachPuff2", ).place(x=10, y=100)
            Qty = Label(Details_frame, text=f"Quantity: 0", font=("courier", 12),
                        bg="PeachPuff2", )
            Qty.place(x=10, y=150)
            Button(Details_frame, text="+", font="Courier", width=2, height=1, bg='PeachPuff2', command=increase) \
                .place(x=140, y=130)
            Button(Details_frame, text="-", font="Courier", width=2, height=1, bg="PeachPuff2", command=decrease) \
                .place(x=140, y=170)
            # find the picture ID in sushiImageDict
            if pictureID in sushiImageDict:
                # open the following image according to the pictureID
                sushiImage = Image.open(f"pictures/{sushiImageDict[pictureID]}")
                sushiTk = ImageTk.PhotoImage(sushiImage)
                # display the image
                picture_Label = Label(Details_frame, image=sushiTk)
                picture_Label.image = sushiTk
                picture_Label.place(x=200, y=45)

            Next_Button = Button(Details_frame, text="NEXT", font="Courier", width=10, height=2,
                                 bg="NavajoWhite4", command=NEXT)
            Next_Button.place(x=140, y=225)
            Next_Button['state'] = 'disable'

        '''Frame to store all the widgets'''
        window_Frame = Frame(self, width=900, height=700, bg="NavajoWhite4")
        window_Frame.pack(side=TOP)

        '''Frame to store the details'''
        details_Frame = Frame(window_Frame, width=830, height=650, highlightthickness="5", bg="PeachPuff2")
        details_Frame.place(x=35, y=25)

        Label(details_Frame, text="Choose a Category:", font=("Courier", 13), bg="PeachPuff2").place(x=10, y=5)
        yAxis = 30  # starting y-coordinate
        # open category.csv in read mode
        with open('files/category.csv', 'r') as category_read:
            # read the content of the file
            data = csv.reader(category_read)
            data_list = list(data)
            # for loop to display the content(Button) of sushi_Categories
            for categories_items in data_list:
                # display the category button
                Button(details_Frame, text=categories_items[1],
                       command=lambda category=categories_items[0]: extract(category), width=20,
                       height=2, font=("Courier", 11), bg="NavajoWhite4").place(x=10, y=yAxis)
                yAxis += round(620 / 9)


class ProductDetails(Frame):
    """
         Class Frame for each product details
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This function will display the details for each product and prompt the user:
        1) Add Another
        2) Proceed and Pay
        3) Cancel

    """

    # initialise constructor
    def __init__(self, master):
        # calls constructor from the superclass
        Frame.__init__(self, master)

        # function to exit
        def Cancel():
            """
            Cancel will carry out the following operations:
            1) Empty the order.csv file to delete past order
            2) switch frame to message
            :return: nothing
            """
            global messagecode
            messagecode = 1
            # empty the order.csv file
            with open(f"files/order.csv", "w") as category_file:
                category_file.truncate(0)
            # sent the empty file to server to make sure connection is not lost
            with open('files/order.csv', 'r') as order_file:
                order_Content = csv.reader(order_file)
                order_list = list(order_Content)
            client_message = pickle.dumps(order_list)
            client_Socket.send(client_message)
            self.master.switchFrame(Message)

        # resize the window
        self.master.geometry("900x700+325+25")

        '''Frame to store all the widgets'''
        window_Frame = Frame(self, width=900, height=700, bg="NavajoWhite4")
        window_Frame.pack(side=TOP)

        '''Frame to store the details'''
        details_Frame = Frame(window_Frame, width=700, height=500, highlightthickness="5", bg="PeachPuff2")
        details_Frame.place(x=100, y=100)

        '''Frame to display the product ID'''
        Label(details_Frame, text="Product", font=("Courier", 20), bg="PeachPuff2").place(x=30, y=10)
        Label(details_Frame, text=" ID ", font=("Courier", 18), bg="PeachPuff2").place(x=50, y=47)
        Label(details_Frame, text=IndividualID, font=("Courier", 27), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=250, y=10)

        '''Frame to display the product name'''
        Label(details_Frame, text="Product", font=("Courier", 20), bg="PeachPuff2").place(x=30, y=100)
        Label(details_Frame, text=" Name ", font=("Courier", 18), bg="PeachPuff2").place(x=50, y=137)
        if len(productName) >= 15:
            shorten_Text = productName[0:15] + "..."
            Label(details_Frame, text=shorten_Text, font=("Courier", 30), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=250, y=100)
        else:
            Label(details_Frame, text=productName, font=("Courier", 30), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=250, y=100)

        '''Frame to display the price per product'''
        Label(details_Frame, text="Individual", font=("Courier", 20), bg="PeachPuff2").place(x=12, y=200)
        Label(details_Frame, text=" Price ", font=("Courier", 18), bg="PeachPuff2").place(x=50, y=237)
        Label(details_Frame, text=f'Rs {IndividualPrice}', font=("Courier", 30), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=250, y=200)

        '''Frame to display the total price of that product'''
        Label(details_Frame, text="Total Price", font=("Courier", 20), bg="PeachPuff2").place(x=10, y=300)
        Label(details_Frame, text="Per Product", font=("Courier", 18), bg="PeachPuff2").place(x=30, y=337)
        TotalPricePerProduct = int(IndividualPrice) * int(purchase_qty)  # calculate the total cost per product
        Label(details_Frame, text=f'Rs {TotalPricePerProduct}', font=("Courier", 30), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=250, y=300)
        Label(details_Frame, text=f'({IndividualPrice}*{purchase_qty})', font=("Courier", 18),
              foreground="DarkGoldenrod4", bg="PeachPuff2").place(x=269, y=340)

        ''' Frame to proceed or cancel or to add new. '''
        Button(details_Frame, text="ADD ANOTHER", bg="RoyalBlue2", font=("Courier", 20), foreground="thistle2",
               command=lambda: master.switchFrame(Menu)).place(x=20, y=400)
        Button(details_Frame, text="PROCEED AND PAY", bg="dark green", font=("Courier", 20), foreground="thistle2",
               command=lambda: master.switchFrame(Receipt)).place(x=250, y=400)
        Button(details_Frame, text="CANCEL", font=("Courier", 20), bg="OrangeRed3", command=Cancel,
               foreground="thistle2").place(x=550, y=400)

        '''Display the logo'''
        logo = Image.open("pictures/logo.png")
        logoTk = ImageTk.PhotoImage(logo)
        picture_Label = Label(details_Frame, image=logoTk, )
        picture_Label.image = logoTk
        picture_Label.place(x=425, y=160)


class Receipt(Frame):
    """
         Class Frame for Receipt
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This function will display the receipt and prompt the user:
        1) Add Another
        2) Proceed and Pay
        3) Cancel

    """

    # initialise constructor
    def __init__(self, master):
        global TotalPrice
        # calls constructor from the superclass
        Frame.__init__(self, master)

        # resize the window
        self.master.geometry("900x700+325+25")

        '''Frame to store all the widgets'''
        window_Frame = Frame(self, width=900, height=700, bg="NavajoWhite4")
        window_Frame.pack(side=TOP)

        '''Frame to store the details'''
        details_Frame = Frame(window_Frame, width=700, height=650, highlightthickness="5", bg="PeachPuff2")
        details_Frame.place(x=100, y=25)

        '''Display title'''
        Label(details_Frame, text="RECEIPT", font=("Courier", 30), foreground="DarkGoldenrod4", bg="PeachPuff2").place(
            x=250, y=10)

        '''Display the logo'''
        logo = Image.open("pictures/logo2.png")
        logoTk = ImageTk.PhotoImage(logo)
        picture_Label = Label(details_Frame, image=logoTk)
        picture_Label.image = logoTk
        picture_Label.place(x=500, y=10)

        '''Display the Product Name'''
        Label(details_Frame, text="Product", font=("Courier", 20), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=30, y=85)
        Label(details_Frame, text=" Name ", font=("Courier", 18), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=40, y=120)

        '''Frame to display the price per product'''
        Label(details_Frame, text="Individual", font=("Courier", 20), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=220, y=85)
        Label(details_Frame, text=" Price ", font=("Courier", 18), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=260, y=120)

        '''Frame to display the quatity of that product'''
        Label(details_Frame, text="Qty", font=("Courier", 20), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=415, y=85)

        '''Frame to display the total price of that product'''
        Label(details_Frame, text="Total Price", font=("Courier", 20), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=490, y=85)
        Label(details_Frame, text="Per Product", font=("Courier", 18), foreground="DarkGoldenrod4",
              bg="PeachPuff2").place(x=505, y=120)

        ''' Display the order details'''
        # open the order.csv in read mode
        with open('files/order.csv', 'r') as order_readfile:
            # append the content of order_readfile to order_list
            order_content = csv.reader(order_readfile)
            order_list = list(order_content)

            yAxis = 153  # starting yAxis
            TotalPrice = 0  # total price of the whole order
            for row in order_list:
                # display the whole order details
                if len(row[0]) >= 15:
                    shorten_Text = row[0][0:12] + "..."
                    Label(details_Frame, text=shorten_Text, font=("Courier", 18), bg="PeachPuff2").place(x=35, y=yAxis)
                else:
                    Label(details_Frame, text=row[0], font=("Courier", 18), bg="PeachPuff2").place(x=35, y=yAxis)
                Label(details_Frame, text=row[2], font=("Courier", 18), bg="PeachPuff2").place(x=282, y=yAxis)
                Label(details_Frame, text=row[1], font=("Courier", 18), bg="PeachPuff2").place(x=435, y=yAxis)
                TotalPricePerProduct = int(row[2]) * int(row[1])
                TotalPrice += TotalPricePerProduct  # calculate the total price of the order
                Label(details_Frame, text=TotalPricePerProduct, font=("Courier", 18), bg="PeachPuff2").place(x=550,
                                                                                                             y=yAxis)
                yAxis += 40
            Label(self, text="-----------", font="Courier", foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=625, y=528)
            Label(self, text=f"Total Price: Rs {TotalPrice}", font=("Courier", 20), bg="PeachPuff2").place(x=420, y=550)
            Label(self, text="-----------", font="Courier", foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=625, y=578)

            '''Button for user to go back '''
            Button(details_Frame, text="Back", font=("Courier", 20), bg="RoyalBlue2", width=10,
                   command=lambda: master.switchFrame(ProductDetails), foreground="thistle2").place(x=130, y=580)
            ''' Button for user to proceed to payment method '''
            Button(details_Frame, text="Payment", font=("Courier", 20), bg="dark green", width=10,
                   command=lambda: master.switchFrame(Payment), foreground="thistle2").place(x=370, y=580)


class Payment(Frame):
    """
        Class Frame for Payment
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This function will display the payment methods (Cash or Card) and prompt the user:
        --> Credit Card details
        or
        --> Cash Payment details
    """

    # initialise constructor
    def __init__(self, master):
        # calls constructor from the superclass
        Frame.__init__(self, master)

        # resize the window
        self.master.geometry("900x700+325+25")

        '''function for cash payment'''

        def CASH():
            """
            This function will carry out the following operations:
            1) enable the user to enter the amount of money
            2) Validate the amount
            3) Proceed to next window
            :return: nothing
            """
            global amount
            amount = 0

            # Button to choose cash
            Button(Payment_Method, text="CASH", font=("Courier", 20), bg="AntiqueWhite4",
                   command=CASH, foreground="thistle2").place(x=150, y=20)
            # Button to choose card
            Button(Payment_Method, text="CARD", font=("Courier", 20), bg="AntiqueWhite4",
                   command=CARD, foreground="thistle2").place(x=450, y=20)

            # clear all widget in that specific frame
            for widgets in Payment_Details.winfo_children():
                widgets.destroy()

            Finish_Button["state"] = "disable"

            # a list to store the notes/coin the user will insert
            money_list = ["2000", "1000", "500", "200", "100",
                          "50", "25", "10", "5", "1",
                          "CE"]

            # function to clear everything on the display
            def ce():
                """
                This function will carry out the following operations:
                1) will clear whatever has been displayed on the display
                2) will set the total amount to zero
                :return: nothing
                """
                global amount
                amount = 0
                # display the change
                text = f"Rs 0"
                Change_Label.config(text=text)
                input_text.set(str(amount))
                Finish_Button["state"] = "disable"

            # function to calculate the total amount of notes/coin clicked
            def button_click(item):
                """
                This function will do the following operations:
                1) Calculate the total amount
                2) Display it on the display
                3) Calculate the change
                4) check if the change is negative
                5) If -ve, then display an error and also make the finish button disable
                6) else, display the change and set the finish button to normal
                :param item: string
                :return: nothing
                """
                global amount
                global change
                amount += int(item)
                input_text.set(str(amount))
                # calculate the change
                change = amount - TotalPrice
                # check if there is lack of money inserted
                if change < 0:
                    Finish_Button["state"] = "disable"
                else:
                    # display the change
                    text = f"Rs {change}"
                    Change_Label.config(text=text)
                    Finish_Button["state"] = "normal"

            # variable to store the amount entered by the user
            input_text = StringVar()
            input_text.set(str(amount))  # display the amount

            Label(Payment_Details, text="Cash due:", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=75, y=10, height=25)

            Label(Payment_Details, text=f'Rs {TotalPrice}', font=("Courier", 25),bg="PeachPuff2").place(x=347, y=10,
                                                                                                        height=25)

            Label(Payment_Details, text="Cash entered: ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=75, y=80, height=25)

            Label(Payment_Details, text=f"Your change:", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=75, y=150)

            Change_Label = Label(Payment_Details, text='Rs 0', font=("Courier", 25), bg="PeachPuff2")
            Change_Label.place(x=347, y=150)

            Label(Payment_Details, text="Enter your cash ", font=("Courier", 15), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=50, y=220, height=25)

            # generate the display bar
            screen = Entry(Payment_Details, font=("Courier", 23), textvariable=input_text, bg="light grey", bd=8,
                           width=5,
                           justify=CENTER)
            screen.place(x=355, y=70)

            i = 0  # starting index for money_list
            # loop to display the money button in Payment_Details frame
            for row in range(250, 330, 60):
                for column in range(75, 575, 100):
                    Button(Payment_Details, text=money_list[i], font=("Courier", 20), bg="AntiqueWhite4", width=5,
                           foreground="black", command=lambda name=money_list[i]: button_click(name)).place(
                        x=column, y=row)
                    i += 1  # increment the index

            # Button to clear everything on the display
            Button(Payment_Details, text="UNDO", font=("Courier", 20), bg="OrangeRed3", foreground="thistle2", width=12,
                   command=lambda: ce()).place(x=225, y=380)



        def CARD():
            Finish_Button["state"] = "disable"
            # Button to choose cash
            Button(Payment_Method, text="CASH", font=("Courier", 20), bg="AntiqueWhite4",
                   command=CASH, foreground="thistle2").place(x=150, y=20)
            # Button to choose card
            Button(Payment_Method, text="CARD", font=("Courier", 20), bg="AntiqueWhite4",
                   command=CARD, foreground="thistle2").place(x=450, y=20)
            """
            This function will prompt the user for the following details:
            1) Name
            2) Account Number
            3) CVV
            4) Valid Thru
            :return: nothing
            """
            def validate():
                if len(name.get()) == 0 or len(account_number.get()) == 0 or len(cvv.get()) == 0 or \
                        len(month.get()) == 0 or len(year.get()) == 0:
                    Finish_Button["state"] = 'disabled'
                else:
                    Finish_Button["state"] = 'normal'
            # clear all widget in that specific frame
            for widgets in Payment_Details.winfo_children():
                widgets.destroy()
            ''' Label and entry for user to enter bank details '''
            Label(Payment_Details, text="Name ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=70, y=50, height=25)
            name = Entry(Payment_Details, width=25, bg="AntiqueWhite3", font=("Courier", 15))
            name.place(x=220, y=50, height=25)

            Label(Payment_Details, text="Account ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=50, y=115, height=25)
            Label(Payment_Details, text=" Number ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=40, y=143, height=25)
            account_number = Entry(Payment_Details, width=20, bg="AntiqueWhite3", font=("Courier", 15))
            account_number.place(x=220, y=129, height=25)

            Label(Payment_Details, text="CVV ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=70, y=208, height=25)
            cvv = Entry(Payment_Details, width=3, bg="AntiqueWhite3", font=("Courier", 15))
            cvv.place(x=220, y=208, height=25)

            Label(Payment_Details, text="VALID  ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=53, y=273, height=25)
            Label(Payment_Details, text=" THRU ", font=("Courier", 25), foreground="DarkGoldenrod4",
                  bg="PeachPuff2").place(x=43, y=301, height=25)
            month = Entry(Payment_Details, width=2, bg="AntiqueWhite3", font=("Courier", 15))
            month.place(x=220, y=287, height=25)
            Label(Payment_Details, text='/', font=("Courier", 20, 'bold'), bg='PeachPuff2', fg='sienna4').place(
                x=252, y=280)
            year = Entry(Payment_Details, width=2, bg="AntiqueWhite3", font=("Courier", 15))
            year.place(x=275, y=287, height=25)

            # Button to validate correct entry
            Button(Payment_Details, text="VALIDATE", font=("Courier", 20), bg="AntiqueWhite4", foreground="black",
                   command=lambda: validate()).place(x=250, y=350)

        '''Frame to store all the widgets'''
        window_Frame = Frame(self, width=900, height=700, bg="NavajoWhite4")
        window_Frame.pack(side=TOP)

        '''Frame to display the payment method'''
        Payment_Method = Frame(window_Frame, width=900, height=100, bg="NavajoWhite4")
        Payment_Method.place(x=100, y=0)

        '''Frame to display cash change or bank details'''
        Payment_Details = Frame(window_Frame, width=650, height=525, highlightthickness="5", bg="PeachPuff2")
        Payment_Details.place(x=125, y=100)

        #  Label to indicate the user to choose cash or bank
        Label(Payment_Details, text="Please Choose ", font=("Courier", 50), bg="PeachPuff2").place(x=50, y=50)
        Label(Payment_Details, text=" A Button ", font=("Courier", 50), bg="PeachPuff2").place(x=120, y=120)
        Label(Payment_Details, text=" Below", font=("Courier", 50), bg="PeachPuff2").place(x=180, y=190)

        # Button to choose cash
        Button(Payment_Details, text="CASH", font=("Courier", 20), bg="AntiqueWhite4",
               command=CASH, foreground="thistle2").place(x=130, y=290)
        # Button to choose card
        Button(Payment_Details, text="CARD", font=("Courier", 20), bg="AntiqueWhite4",
               command=CARD, foreground="thistle2").place(x=430, y=290)

        # send order.csv as a list to server to update the database
        with open('files/order.csv', 'r') as order_file:
            order_Content = csv.reader(order_file)
            order_list = list(order_Content)
        client_message = pickle.dumps(order_list)
        client_Socket.send(client_message)

        # Finish Payment button
        Finish_Button = Button(window_Frame, text="Finish", font=("Courier", 20), bg="AntiqueWhite4",
                               command=lambda: master.switchFrame(Message), foreground="thistle2")
        Finish_Button.place(x=400, y=630)
        Finish_Button["state"] = "disable"


class Message(Frame):
    """
        Class Frame for Goodbye message
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This function will display the goodbye message and close the application.
    """

    # initialise constructor
    def __init__(self, master):
        # calls constructor from the superclass
        Frame.__init__(self, master)

        # resize the window
        self.master.geometry("900x700+325+25")

        MS_DELAY = 500  # Milliseconds between updates.
        timer_text = StringVar()

        def timer_function():
            """
            This function will switch the frame with a pre-determined time limit
            :return: nothing
            """
            global timer
            timer -= 1
            if timer <= 1:
                self.after(1000, lambda: master.switchFrame(Welcome))
            return timer

        def print_timer():
            """
            This function will display the remaining seconds to switch automatically to the welcome window
            :return: nothing
            """
            timer_text.set(f'Returning in {timer_function()} secs')
            details_Frame.after(MS_DELAY, print_timer)  # Schedule next check.

        '''Frame to store all the widgets'''
        window_Frame = Frame(self, width=900, height=700, bg="NavajoWhite4")
        window_Frame.pack(side=TOP)

        '''Frame to store the details'''
        details_Frame = Frame(window_Frame, width=700, height=500, highlightthickness="5", bg="PeachPuff2")
        details_Frame.place(x=100, y=100)

        if messagecode == 1:
            # Cancel Message
            Label(details_Frame, text="Sorry,", font=("Courier", 25), bg="PeachPuff2").place(x=300, y=50)
            Label(details_Frame, text="We could not provide you with ", font=("Courier", 20),
                  bg="PeachPuff2").place(x=120, y=100)
            Label(details_Frame, text=" your choice today.", font=("Courier", 22),
                  bg="PeachPuff2").place(x=180, y=140)
            Label(details_Frame, text="We hope to see you soon again. ", font=("Courier", 20),
                  bg="PeachPuff2").place(x=120, y=200)
            Label(details_Frame, text=" Have a good day!", font=("Courier", 22), bg="PeachPuff2").place(x=205, y=250)
            Redirecting_Label = Label(details_Frame, textvariable=timer_text, font=("Courier", 20), bg="PeachPuff2")
            Redirecting_Label.place(x=205, y=350)
            details_Frame.after(MS_DELAY, print_timer)

        else:
            # Good-Bye Message
            Label(details_Frame, text="Thank You", font=("Courier", 50), bg="PeachPuff2").place(x=140, y=50)
            Label(details_Frame, text=" Good-Bye ", font=("Courier", 44), bg="PeachPuff2").place(x=160, y=130)
            Label(details_Frame, text="Enjoy ケシャフ's ", font=("Courier", 44), bg="PeachPuff2").place(x=100, y=225)
            Label(details_Frame, text=" Sushi ", font=("Courier", 44), bg="PeachPuff2").place(x=210, y=300)
            Redirecting_Label = Label(details_Frame, textvariable=timer_text, font=("Courier", 20), bg="PeachPuff2")
            Redirecting_Label.place(x=195, y=380)
            details_Frame.after(MS_DELAY, print_timer)


def main():
    """
    It is the main function which will start the application.
    :return: nothing
    """
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
