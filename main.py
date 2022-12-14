import requests
import configparser


# get the API key from the config file and return it to the caller.
#
def get_apikey():
    try:
        config = configparser.ConfigParser()
        config.read('app.config')
        apikey_from_file = config['secrets']['apikey']
    except KeyError:
        raise BadSecrets
    return apikey_from_file

class BadSecrets(Exception):
    pass

# A default exception handler
class NoSuchLocation(Exception):
    pass


# Call the API to get the location
def get_location(api_key):
    print("Set a location (current location: not set)")
    # get the zipcode from the user. For debugging, this has been
    # hardcoded

    zipcode = input("Put in zip code here:")

    location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                   'postalcodes/search?apikey={}&q={}'.format(api_key, zipcode)

    response = requests.get(location_url)

    try:
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    return key


def print_time_status(is_day):
    print("Day/Night: {} time".format("Day" if is_day else "Night"))

def get_conditions(key, api_key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/' \
        '{}?apikey={}'.format(key, api_key)
    response = requests.get(conditions_url)
    json_version = response.json()
    print("Current Conditions: {}".format(json_version[0].get('WeatherText')))
    print("Get forecast for tomorrow")

    is_day = json_version[0].get('IsDayTime')
    print_time_status(is_day)

    # gets current temperature in imperial units
    print("Current Temperature: {}\n".format(json_version[0]['Temperature']['Imperial']['Value']))


try:
    apikey = get_apikey()
    location_key = get_location(apikey)
    get_conditions(location_key, apikey)
except NoSuchLocation:
    print("Unable to get the location")
except BadSecrets:
    print("Unable to use secret file")
