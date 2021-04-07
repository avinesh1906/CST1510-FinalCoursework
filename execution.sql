CREATE TABLE Categories (
categoriesID  int primary key auto_increment ,
Name varchar(50)
);

CREATE TABLE Products (
 productID	int  primary key auto_increment,
 Name varchar(50)
 );

 CREATE TABLE food (
FoodID int primary key auto_increment,
categoriesID int,
productID int,
price int,
qty int,
 CONSTRAINT Fk_Categories FOREIGN KEY (categoriesID) REFERENCES Categories(categoriesID),
 CONSTRAINT Fk_Products FOREIGN KEY (productID) REFERENCES Products(productID)
 );

 CREATE TABLE Platters (
 plattersID int primary key ,
 categoriesID int,
 platterName VARCHAR(50),
 price INT,
 qty int,
 CONSTRAINT Fk_Category FOREIGN KEY (categoriesID) REFERENCES Categories(categoriesID)
 );

INSERT INTO Categories (Name) VALUES ('Maki' );
INSERT INTO Categories (Name) VALUES ('Nigiri' );
INSERT INTO Categories (Name) VALUES ('Gunkans');
INSERT INTO Categories (Name) VALUES ('Flower Gunkans' );
INSERT INTO Categories (Name) VALUES ('California Rolls' );
INSERT INTO Categories (Name) VALUES ('Rainbow Rolls' );
INSERT INTO Categories (Name) VALUES ('Futomaki');
INSERT INTO Categories (Name) VALUES ('Sashimi');
INSERT INTO Categories (Name) VALUES ('Sushi Platters' );


INSERT INTO Products (Name) VALUES ('Cucumbeer');
INSERT INTO Products (Name) VALUES ('Avocado');
INSERT INTO Products (Name) VALUES ('Prawn');
INSERT INTO Products (Name) VALUES ('Salmon');
INSERT INTO Products (Name) VALUES ('Tuna');
INSERT INTO Products (Name) VALUES ('Tomato');
INSERT INTO Products (Name) VALUES ('Zucchini');
INSERT INTO Products (Name) VALUES ('Panko Prawn');
INSERT INTO Products (Name) VALUES ('Calamari');
INSERT INTO Products (Name) VALUES ('Wasabi Prawn');
INSERT INTO Products (Name) VALUES ('Tuna Tulips');
INSERT INTO Products (Name) VALUES ('Spicy Salmon Roses');
INSERT INTO Products (Name) VALUES ('Salmon Roses');
INSERT INTO Products (Name) VALUES ('Crunchy Athena');
INSERT INTO Products (Name) VALUES ('Coriander Bomb');
INSERT INTO Products (Name) VALUES ('Flamed Salom');
INSERT INTO Products (Name) VALUES ('Fried Prawn');
INSERT INTO Products (Name) VALUES ('Tempura Rock Shrimp');
INSERT INTO Products (Name) VALUES ('Lemon Salmon');
INSERT INTO Products (Name) VALUES ('Salom and Avo');
INSERT INTO Products (Name) VALUES ('Tuna and Avo');
INSERT INTO Products (Name) VALUES ('Sweet Prawn');
INSERT INTO Products (Name) VALUES ('Panko Salmon');
INSERT INTO Products (Name) VALUES ('Avocado');

INSERT INTO food (categoriesID, productID, price, qty) VALUES (1,1,135,43);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (1,2,145,46);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (1,3,235,35);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (1,4,255,47);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (1,5,235,23);

INSERT INTO food (categoriesID, productID, price, qty) VALUES (2,6,135,15);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (2,7,135,23);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (2,3,155,56);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (2,4,165,30);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (2,5,155,26);

INSERT INTO food (categoriesID, productID, price, qty) VALUES (3,8,205,31);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (3,9,215,49);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (3,10,205,50);

INSERT INTO food (categoriesID, productID, price, qty) VALUES (4,11,185,50);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (4,12,245,17);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (4,13,245,19);

INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,3,145,36);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,4,155,42);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,5,145,47);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,14,265,23);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,15,155,17);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,16,165,18);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,17,145,5);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,18,155,4);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (5,19,165,13);

INSERT INTO food (categoriesID, productID, price, qty) VALUES (6,20,250,17);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (6,21,225,11);

INSERT INTO food (categoriesID, productID, price, qty) VALUES (7,22,275,45);
INSERT INTO food (categoriesID, productID, price, qty) VALUES (7,23,295,47);

INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (30,8,'3 pieces', 285,50);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (31,8,'6 pieces', 525,30);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (32,8,'9 pieces', 695,23);

INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (33,9,'Fusion Crunch Platter', 745,10);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (34,9,'Flower Power Platter', 455,17);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (35,9,'Salmon Platter', 1175,19);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (36,9,'Zen Platter', 755,26);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (37,9,'Rising Sun Platter', 625,25);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (38,9,'Bonsai Platter (Veg)', 455,45);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (39,9,'Sushi for 1', 525,35);
INSERT INTO Platters (plattersID,categoriesID, platterName, price, qty) VALUES (40,9,'Sushi for 2', 945,46);




