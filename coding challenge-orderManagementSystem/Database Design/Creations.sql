create database OrderManagement;
use OrderManagement;

CREATE TABLE Product (
    productId INT PRIMARY KEY,
    productName VARCHAR(100),
    description VARCHAR(MAX),
    price decimal(10,2),
    quantityInStock INT,
    type VARCHAR(50)
);

CREATE TABLE Users (
    userId INT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(50)
);

Create TABLE ELECTRONICS (
productId int foreign key (productId) references Product(productId),
brand VARCHAR(100), 
warrantyPeriod INT);

Create Table Clothing(
productId int foreign key(productId) references Product(productId),
size VARCHAR(50), 
color VARCHAR(50),
);

create table orders(
orderId int primary key,
userId int foreign key(userId) references Users(userId),
productId int foreign key(productId) references Product(productId),
quantity int,
orderdate date,
);
