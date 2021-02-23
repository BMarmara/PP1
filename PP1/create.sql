DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Bidder;
DROP TABLE IF EXISTS Category;

CREATE TABLE Item(
    itemId INTEGER not null, 
    userId VARCHAR(255) not null,
    itemName VARCHAR(255) not null,
    currently VARCHAR(255) not null,
    buy_price VARCHAR(255),
    first_bid VARCHAR(255) not null,
    number_of_bids DECIMAL not null,
    itemLocation VARCHAR(255),
    country VARCHAR(255),
    itemStarted VARCHAR(255) not null,
    itemEnded TIME not null,
    itemDescription TEXT not null,
    PRIMARY KEY(itemId),
    FOREIGN KEY(userId) REFERENCES Bids(userId)
);

CREATE TABLE Person(
    userId VARCHAR(255) not null,
    rating DECIMAL not null,
    PRIMARY KEY(userId)
);

CREATE TABLE Bid(
    bidder VARCHAR(255) not null, 
    itemId INTEGER not null,
    bidTime TIME not null,
    amount VARCHAR(255),
    PRIMARY KEY(bidder),
    FOREIGN KEY(itemId) REFERENCES Item(itemId)
);

CREATE TABLE Bidder(
    userId VARCHAR(255),
    rating DECIMAL not null,
    bidderLocation VARCHAR(255),
    country VARCHAR(255),
    PRIMARY KEY(userId)
);

CREATE TABLE Category(
    itemId INTEGER not null,
    category VARCHAR(255) not null,
    PRIMARY KEY(itemId),
    FOREIGN KEY(itemId) REFERENCES Item(itemId)
);