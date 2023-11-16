from flask import Blueprint, render_template, request, Response
import requests
import ldap
import json

main = Blueprint('main', __name__)

endpoint = "https://api.corelogic.asia"
client_id = "jqhrXN8FIcA8LgMHvijARfAqzy0PD2Cp"
client_secret = "qWSAAO7n0XPjhMvT"
token = ""

@main.route("/")
def landing():
    return render_template("index.html")

@main.route("/addressSearch")
def addressSearch():
    address = request.args.get('addressSearch')
    address = address.replace(" Australia","")
    address = address.replace(',','')
    address = address.replace(' ','%20')
    login = checkauth()
    core_address = get_property_id(address)
    property_id = core_address['suggestions'][0]['propertyId']
    return_data = {
        "Document": get_property_report(property_id)['url'],
        "Guide": "100"
    }
    return_data = {
            "Document": get_property_report(property_id)['url'],
            "Guide": get_price_guide(property_id)
        }
    return render_template('data.html', form_data=return_data)

def get_price_guide(propertyID):
    data_uri = f"/property-details/au/properties/{propertyID}/otm/campaign/sales"
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(endpoint + data_uri, headers=headers)
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        return json_data['forSalePropertyCampaign']['campaigns'][0]['firstPublishedPrice']

    return None

def get_property_id(address):
    data_uri = f"/property/au/v2/suggest.json?q={address}"
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(endpoint + data_uri, headers=headers)
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        return json_data

def get_property_report(propertyID):
    data = {
        "customerName": "test",
        "reportRequester": {
            "email": "test@test.com",
            "name": "test",
            "phone": "phone"
        }
    }
    data = json.dumps(data)
    data_uri = f"/property-profile-report/au/property/{propertyID}/ppr"
    headers = {'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
                }
    resp = requests.post(endpoint + data_uri, headers=headers, data=data)
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        return json_data

    return None

def checkauth():
    global token
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(endpoint+"/property-details", headers=headers)
    print(resp.status_code)
    if resp.status_code == 401:
        print("Not logged in, logging in")
        token = login()
        return True
    print("Already logged in, proceeding")
    return True

def login(clientID=client_id, clientSecret=client_secret):
    login_uri = f"/access/oauth/token?grant_type=client_credentials&client_id={clientID}&client_secret={clientSecret}"
    resp = requests.get(endpoint + login_uri)
    if resp.status_code == 200:
        json_data = json.loads(resp.text)
        return json_data['access_token']
        
    return None