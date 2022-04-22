from flask import Flask, request
import requests
from dicttoxml import dicttoxml
import env
import json

app = Flask(__name__)

GEOCODE_API_KEY = env.GEOCODE_API_KEY


# GET route: root route with a message, what api does. Doesn't require any input
@app.get("/")
def root_route():
    return "Fetches Latitude and Logitude of an address in 'json' or 'xml format using googlemapsAPI"


# POST route: accepts json as an input and calls googlemaps api
@app.post("/getAddressDetails")
def addr_details():
    address = request.json['address']
    output_type = request.json['output_format']

    try:
        # Available output_formats
        outputFormat = ['json', 'xml']

        # Address type is not string
        if type(address) != str:
            return "Please enter valid address"

        # Output format other than available formats
        elif output_type not in outputFormat:
            return "Please select output format 'json' or 'xml'"

        # All checks are passed
        else:
            location = requests.get(
                f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GEOCODE_API_KEY}'
            )

        results = location.json()['results']

        # Result is not empty or empty
        if results != []:
            location_coord = results[0]['geometry']['location']

            # Returns response according to type specified in output_value
            if output_type == 'json':
                address_coordinates = {
                    "coordinates": location_coord,
                    "address": address,
                }
                address_coordinates = json.dumps(address_coordinates)
                return address_coordinates

            elif output_type == 'xml':
                lat_lang = {"address": address, "coordinates": location_coord}
                location_xml = dicttoxml(lat_lang, attr_type=False)
                return location_xml

        # In case of no results or address has special character in it.
        else:
            return "No results found, please check if address is valid or check and remove any special characters in address"
    except Exception as e:
        print(e)
        return "Internal server error"


if __name__ == "__main__":
    app.run(debug=True)
