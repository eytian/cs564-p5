DROP TABLE IF EXISTS Sellers;
DROP TABLE IF EXISTS Bidders;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Bids;


CREATE TABLE Sellers (user_id CHAR(256) NOT NULL UNIQUE,
	rating INT NOT NULL,
    location_id CHAR(256),
	PRIMARY KEY(user_id),
	FOREIGN KEY(location_id) REFERENCES Locations(location_id)
);

CREATE TABLE Bidders (user_id CHAR(256) NOT NULL UNIQUE,
    location_id CHAR(256),
    country CHAR(256),
    rating INT NOT NULL,
    PRIMARY KEY(user_id),
    FOREIGN KEY(location_id) REFERENCES Locations(location_id)
);

CREATE TABLE Locations (location_id CHAR(256) NOT NULL UNIQUE,
	location CHAR(256),
	country_id CHAR(256),
	PRIMARY KEY(location_id)
);

CREATE TABLE Items (item_id CHAR(256) NOT NULL UNIQUE,
	name CHAR(256),
	currently INT,
	buy_price DOUBLE,
	First_Bid DOUBLE,
	Number_of_Bids INT,
	started CHAR(256),
	ends CHAR(256),
	item_sale CHAR(256),
    item_bid CHAR(256),
    item_category CHAR(256),
	description CHAR(1000),
	PRIMARY KEY(item_id),
	FOREIGN KEY(item_bid) REFERENCES Bids(bids_id),
	FOREIGN KEY(item_sale) REFERENCES Sellers(user_id),
    FOREIGN KEY(item_category) REFERENCES Categories(category_id)
);

CREATE TABLE Categories (category_id CHAR(256) NOT NULL UNIQUE,
	category CHAR(256) NOT NULL,
	PRIMARY KEY(category_id)
);

CREATE TABLE Bids (bids_id CHAR(256) NOT NULL UNIQUE,
	amount CHAR(256),
	time CHAR(256),
	user_bid CHAR(256),
	item_id CHAR(256),
	PRIMARY KEY(bids_id),
	FOREIGN KEY(user_bid) REFERENCES Bidders(user_id),
	FOREIGN KEY(item_id) REFERENCES Items(item_id)
);

