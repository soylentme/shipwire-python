shipwire-python
===============

[![Build Status](https://travis-ci.org/soylentme/shipwire-python.svg?branch=master)](https://travis-ci.org/soylentme/shipwire-python)
[![Coverage Status](https://coveralls.io/repos/soylentme/shipwire-python/badge.svg?branch=master&service=github)](https://coveralls.io/github/soylentme/shipwire-python?branch=master)

A Python abstraction layer around the Shipwire API.

#####Installing:

To install the shipwire package simply run:

```shell
> pip install shipwire
```

or include a line for 'shipwire' in your projects requirements.txt and run:
```shell
> pip install -r requirements.txt
```

#####Getting Started:

The first step in using the shipwire package is creating a new instance of the Shipwire class by passing it your username, password, and host. You can sign up for an account at https://shipwire.com for the production site or https://beta.shipwire.com for testing purposes. This package's default host is 'api.shipwire.com'. For testing api calls you may set the host to 'api.beta.shipwire.com'.

```python
from shipwire import *
s = Shipwire(username="neil@soylent.me",
             password="89ahdkjfnud@$@#%",
             host="api.beta.shipwire.com")
```

Once you have instantiated your Shipwire class you can start to make calls to the Shipwire API. You can get a list of orders placed to your account by running the following command:

```python
response = s.orders.list(updatedAfter="2014-10-19T21:09:26.030625")
```

For the full list of parameters that you can pass to each method, please visit https://www.shipwire.com/w/developers/ and look under 'API RESOURCES' for the given resource and method.

#####Methods:

This shipwire package currently provides the following methods for Shipwire API calls:

```python
s.order.get(id=41949255) # returns an order resource for the given id.
s.order.holds(id=41949255) # returns a list of holds on a given order.
s.order.items(id=41949255) # returns a list of items in a given order.
s.order.returns(id=41949255) # returns a list of returns for a given order.
s.order.trackings(id=41949255) # returns a list of tracking information for a given order.
s.orders.list(updatedAfter="2014-10-19T21:09:26.030625") # returns a list of orders filtered by the parameters based to the method.
s.stock.products() # returns a list of products that are listed in your shipwire account.
s.rate.quote(json={}) # returns rate quotes based on the json information you supply. See a sample of the json below.
s.order.create(json=your_json) # creates a new order in the shipwire system and returns a list of the orders created.
s.order.cancel(id=41949255) # cancels a specified order in the shipwire system.
s.order.modify(id=41949255,json=your_json) # modifies a specified order in the shipwire system and returns the order resource.
s.receiving.list() # Get an itemized list of receivings
s.receiving.create(json=your_json) # Create a new receiving
s.receiving.get(id=1234) # Get information about this receiving
s.receiving.modify(id=1234,json=your_json) # Modify information about this receiving
s.receiving.cancel(id=1234) # Cancel this receiving
s.receiving.cancel_labels(id=1234) # Cancel shipping_labels on this receiving
s.receiving.holds(id=1234) # Get the list of holds, if any, on this receiving
s.receiving.instructions_recipients(id=1234) # Get email recipients and instructions for this receiving.
s.receiving.items(id=1234) # Get the contents of this receiving
s.receiving.shipments(id=1234) # Get shipping dimension and container information
s.receiving.trackings(id=1234) # Get tracking information about this receiving.
s.webhooks.list() # Get an itemized list of webhook subscriptions
s.webhooks.create(json={'topic':'v1.order_updated', 'url':'https://requestbin.herokuapp.com/unique_id'}) # Create a new webhook subscription
s.webhooks.get(id=1234) # Get information about a specific webhook
s.webhooks.modify(id=1234, json=your_json) # Change an existing webhook
s.webhooks.delete(id=1234) # Delete an active webhook.
s.secrets.list() # List all webhook secure secrets (used in webhook validations)
s.secrets.create(json={'id': 123, 'secret':'fea02c613d1c3aab16...c3d74'}) # Create a new secret.
s.secrets.get(id=1234) # Get info about a single secret
s.secrets.delete(id=1234) # Delete a secret
```

#####Webhook Endpoints:
Shipwire requires webhook endpoints to be secured with SSL and return 200 ok for HEAD requests.

#####Responses:

Each call to the Shipwire API returns a response object with several standard attributes. The following attributes are available on each method call:

```python
response.status # returns the HTTP status code of the HTTP response, not to be confused with the Shipwire API status which can be found in the .errors and .warnings attributes.
response.message # returns a human readable equivalent of response.status for the HTTP response
response.resource # returns json object of the top level resource object
response.json # returns the full json response provided by the Shipwire API
response.response # returns the full requests package response object
response.resource_location # returns the URL of the top level resource
response.location # returns the URL of the top level resource
response.warnings # returns a list of warnings associated with the call
response.errors # returns a list of errors associated with the call
```

In addition to these standard attributes, the shipwire package also provides several list specific attributes for responses that have resources in list form. The orders.list, order.holds, order.items, order.returns, order.trackings, stock.products, and order.create methods all return resources in list form and have the following additional attributes:

```python
response.total # returns the total number of items in the list
response.previous # returns a URL to the previous group of items in the pagination
response.next # returns a URL to the next group of items in the pagination
response.offset # returns the nubmer of items offset by the current request
response.items # returns a list of items in the current group
response.limit # returns a count of the current group
response.all() # returns a list of all the items in the entire selection. Please note that this method can be time consuming and lead to timeout errors by the Shipwire API.
```

#####Methods that require information passed in json:
You must supply information in json form for the rate.quote, order.create, and order.modify methods. Examples of the json data to be supplied can be found on the shipwire developer website at https://www.shipwire.com/w/developers/ or also in the text below.

Please note that you must replace the null values in json with None in python.

Json sample for order.create
```javascript
{
    "orderNo": "foobar1",
    "externalId": "rFooBar1",
    "processAfterDate": "2014-06-10T16:30:00-07:00",
    "commerceName": "Foo Commerce",
    "items": [
        {
            "sku": "Laura-s_Pen",
            "quantity": 4,
            "commercialInvoiceValue": 4.5,
            "commercialInvoiceValueCurrency": "USD"
        },
        {
            "sku": "TwinPianos",
            "quantity": 4,
            "commercialInvoiceValue": 6.5,
            "commercialInvoiceValueCurrency": "USD"
        }
    ],
    "options": {
        "warehouseId": null,
        "warehouseExternalId": null,
        "warehouseRegion": "LAX",
        "warehouseArea": null,
        "serviceLevelCode": "1D",
        "carrierCode": null,
        "sameDay": "NOT REQUESTED",
        "forceDuplicate": 0,
        "forceAddress": 0,
        "testOrder": 0,
        "referrer": "Foo Referrer",
        "affiliate": null,
        "currency": "USD",
        "canSplit": 1,
        "hold": 1,
        "discountCode": "FREE STUFF",
        "server": "Production",
        "forceAsync": 0
    },
    "shipFrom": {"company": "We Sell'em Co."},
    "shipTo": {
        "email": "audrey.horne@greatnothern.com",
        "name": "Audrey Horne",
        "address1": "6501 Railroad Avenue SE",
        "address2": "Room 315",
        "address3": "",
        "city": "Snoqualmie",
        "state": "WA",
        "postalCode": "98065",
        "country": "US",
        "phone": "4258882556",
        "isCommercial": 0,
        "isPoBox": 0
    },
    "commercialInvoice": {
        "shippingValue": 4.85,
        "insuranceValue": 6.57,
        "additionalValue": 8.29,
        "shippingValueCurrency": "USD",
        "insuranceValueCurrency": "USD",
        "additionalValueCurrency": "USD"
    },
    "packingList": {
        "message1": {
            "body": "This must be where pies go when they die. Enjoy!",
            "header": "Enjoy this product!"
        }
    }
}
```

Please feel free to fork this repository at https://github.com/soylentme/shipwire-python and we'll be happy to incorporate modifications through pull requests.
