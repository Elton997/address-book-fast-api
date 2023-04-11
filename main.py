from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import sqlite3

# Initialize the FastAPI app
app = FastAPI()

# Define a Pydantic BaseModel to validate the address data
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    latitude: float = None
    longitude: float = None
    
    # Add a validator to automatically populate the latitude and longitude fields based on the street, city, state, and zip_code fields
    @validator('latitude', 'longitude', pre=True, always=True)
    def validate_location(cls, value, values):
        # Check if all required fields are present
        if 'street' in values and 'city' in values and 'state' in values and 'zip_code' in values:
            # Use the Nominatim geocoder to get the location coordinates from the address string
            geolocator = Nominatim(user_agent="addressbook")
            address_str = f"{values['street']}, {values['city']}, {values['state']} {values['zip_code']}"
            location = geolocator.geocode(address_str)
            # Raise an error if the location could not be found
            if location is None:
                raise ValueError('Unable to geocode address')
            # Set the latitude and longitude fields to the coordinates of the location
            values['latitude'] = location.latitude
            values['longitude'] = location.longitude
        # Return the longitude value (which is required by the BaseModel)
        return values['longitude']

# Define a class for interacting with the SQLite database
class AddressDB:
    def __init__(self, db_path):
        # Connect to the database and create the addresses table if it doesn't already exist
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        # Use SQL to create the addresses table with the necessary fields
        self.conn.execute('''CREATE TABLE IF NOT EXISTS addresses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                street TEXT,
                                city TEXT,
                                state TEXT,
                                zip_code TEXT,
                                latitude REAL,
                                longitude REAL)''')

    def add_address(self, address: Address):
        # Use SQL to insert the address data into the database
        self.conn.execute('''INSERT INTO addresses (street, city, state, zip_code, latitude, longitude)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                            (address.street, address.city, address.state, address.zip_code,
                            address.latitude, address.longitude))
        # Commit the transaction to the database
        self.conn.commit()

    def update_address(self, address_id: int, address: Address):
        # Use SQL to update an existing address in the database
        self.conn.execute('''UPDATE addresses SET street=?, city=?, state=?, zip_code=?, latitude=?, longitude=?
                            WHERE id=?''',
                            (address.street, address.city, address.state, address.zip_code,
                            address.latitude, address.longitude, address_id))
        # Commit the transaction to the database
        self.conn.commit()

    def delete_address(self, address_id: int):
        # Use SQL to delete an existing address from the database
        self.conn.execute('''DELETE FROM addresses WHERE id=?''', (address_id,))
        # Commit the transaction to the database
        self.conn.commit()

    def get_addresses_within_distance(self, latitude: float, longitude: float, distance: float) -> List[Address]:
        # Use SQL to get all existing addresses from the database and retrieve only the close distance addresses
        addresses = []
        for row in self.conn.execute('''SELECT street, city, state, zip_code, latitude, longitude FROM addresses'''):
            coords = (row[4], row[5])
            #geodesic()-Used to calculate the distance between coordinates from DB and API Request.
            if geodesic((latitude, longitude), coords).miles <= distance:
                address = Address(street=row[0], city=row[1], state=row[2], zip_code=row[3],
                                   latitude=row[4], longitude=row[5])
                addresses.append(address)
        print(addresses)
        return addresses

# Create DB session
db = AddressDB('addresses.db')

#Create an address in DB
@app.post('/addresses')
async def create_address(address: Address):
    db.add_address(address)
    return {'message': 'Address added successfully'}

#Update an address in DB
@app.put('/addresses/{address_id}')
async def update_address(address_id: int, address: Address):
    db.update_address(address_id, address)
    return {'message': 'Address updated successfully'}

#Delete an address in DB
@app.delete('/addresses/{address_id}')
async def delete_address(address_id: int):
    db.delete_address(address_id)
    return {'message': 'Address deleted successfully'}

#get existing within distance addresses from DB
@app.get('/get_addresses/')
async def get_addresses(latitude: float, longitude: float, distance: float):
    addresses = db.get_addresses_within_distance(latitude, longitude, distance)
    return {'addresses': addresses}
