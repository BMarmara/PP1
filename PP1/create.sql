DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Category;

CREATE TABLE Item(
    ItemID INTEGER not null, 
    Name VARCHAR(255) not null,
    Currently DECIMAL not null,
    Buy_Price DECIMAL,
    First_Bid DECIMAL not null,
    Number_of_Bids DECIMAL not null,
    Location VARCHAR(255) not null,
    Started VARCHAR(255) not null,
    Ends TIME not null,
    UserID VARCHAR(255) not null,
    SellerRating Integer not null,
    Description TEXT not null,
    PRIMARY KEY(ItemID),
    FOREIGN KEY(UserID) REFERENCES Person(UserID)
);

CREATE TABLE Person(
    UserID VARCHAR(255) not null,
    Rating DECIMAL not null,
    Location VARCHAR(255),
    Country VARCHAR(255)
    -- PRIMARY KEY(UserID)
);

CREATE TABLE Bid(
    ItemID INTEGER not null,
    UserID VARCHAR(255) not null,     
    Time DATETIME not null,
    Amount DECIMAL,
    -- PRIMARY KEY(UserID),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Category(
    ItemID INTEGER not null,
    Category VARCHAR(255) not null,
    PRIMARY KEY(ItemId, Category),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)
);
