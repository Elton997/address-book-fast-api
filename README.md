# FastAPI Address Book
This is a simple API built using FastAPI to create, update, delete, and retrieve addresses from a SQLite database. The API uses geopy to geocode the addresses and geodesic to calculate the distance between coordinates.

## Dependencies
The following dependencies are required to run the application:

- FastAPI
- Pydantic
- geopy
- geodesic
- SQLite

## Installation
```
git clone https://github.com/Elton997/address-book-fast-api.git
```

To install the dependencies, run the following command:
```
pip install fastapi pydantic geopy
```

## Usage
Create Virtual Environment in Python to run the FastAPI:

(For Windows Users)
```
python -m venv .venv
.venv\Scripts\activate.bat 
pip install uvicorn
```

(For MAC or Linux Users)
```
python -m venv .venv
source venv/bin/activate
pip install uvicorn
```

To start the API, run the following command:
```
uvicorn main:app --reload
```

This will start the API server at **http://localhost:8000**.

## Creating an Address
To create an address, send a POST request to the **/addresses** endpoint with the address data in the request body. The API will automatically geocode the address and add it to the database.

**Request Body:**
```
{
"street": "Naigaon",
"city": "Mumbai",
"state": "Maharashtra",
"zip_code": "401211"
}
```

## Updating an Address
To update an existing address, send a PUT request to the **/addresses/{address_id}** endpoint with the updated address data in the request body.

## Deleting an Address
To delete an existing address, send a DELETE request to the **/addresses/{address_id}** endpoint with the address ID in the URL.

## Getting Addresses within a Distance
To get all addresses within a certain distance from a given latitude and longitude, send a GET request to the **/get_addresses** endpoint with the latitude, longitude, and distance in the query parameters.

## Postman Colletion:
I've already added the Postman collection for testing purpose, you can use the same.

## License
This project is licensed under the terms of the MIT license.
