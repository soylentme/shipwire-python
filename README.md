shipwire-python
===============

A Python abstraction layer around the Shipwire API.


This package requires Requests package version 2.4.3 or higher.

#NOTE status code only respresents http status. Error codes are placed in 'error' parameter in json response.


from shipwire import *
s = Shipwire(username="neildurbin@gmail.com", password="numb3r",host="api.beta.shipwire.com")

order = s.order.get(id=41949255)
order_holds = s.order.holds(id=41949255)
order_items = s.order.items(id=41949255)
order_returns = s.order.returns(id=41949255)
order_trackings = s.order.trackings(id=41949255)
order_list = s.orders.list(updatedAfter="2014-10-19T21:09:26.030625")
products = s.stock.products()

j = {
    "options": {
        "currency": "USD",
        "groupBy": "all",
        "canSplit": 1,
        "warehouseArea": "US"
    },
    "order": {
        "shipTo": {
            "address1": "6501 Railroad Avenue SE",
            "address2": "Room 315",
            "address3": "",
            "city": "Snoqualmie",
            "postalCode": "85283",
            "region": "WA",
            "country": "US",
            "isCommercial": 0,
            "isPoBox": 0
        },
        "items": [
            {
                "sku": "1AP",
                "quantity": 3
            }
        ]
    }
}

quote = s.rate.quote(json=j)

j = {
    "orderNo": "foobar1",
    "externalId": "rFooBar2",
    "processAfterDate": "2014-06-10T16:30:00-07:00",
    "commerceName": "Foo Commerce",
    "items": [
        {
            "sku": "1AP",
            "quantity": 43,
            "commercialInvoiceValue": 4.5,
            "commercialInvoiceValueCurrency": "USD"
        }
    ],
    "options": {
        "warehouseId": None,
        "warehouseExternalId": None,
        "warehouseRegion": "LAX",
        "warehouseArea": None,
        "serviceLevelCode": "1D",
        "carrierCode": None,
        "sameDay": "NOT REQUESTED",
        "forceDuplicate": 0,
        "forceAddress": 0,
        "testOrder": 0,
        "referrer": "Foo Referrer",
        "affiliate": None,
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
        "address1": "501 S. Manhattan Place",
        "address2": "Apt 102",
        "address3": "",
        "city": "Los Angeles",
        "state": "CA",
        "postalCode": "90020",
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

order_create = s.order.create(json=j)

#NOTE status code only respresents http status. Error codes are placed in 'error' parameter in json response.

j = {
    "orderNo": "foobar1",
    "externalId": "rFooBar2",
    "processAfterDate": "2014-06-10T16:30:00-07:00",
    "commerceName": "Foo Commerce",
    "items": [
        {
            "sku": "1AP",
            "quantity": 4,
            "commercialInvoiceValue": 4.5,
            "commercialInvoiceValueCurrency": "USD"
        }
    ],
    "options": {
        "warehouseId": None,
        "warehouseExternalId": None,
        "warehouseRegion": "LAX",
        "warehouseArea": None,
        "serviceLevelCode": "1D",
        "carrierCode": None,
        "sameDay": "NOT REQUESTED",
        "forceDuplicate": 0,
        "forceAddress": 0,
        "testOrder": 0,
        "referrer": "Foo Referrer",
        "affiliate": None,
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
        "address1": "3615 Crooks Rd.",
        "address2": "Apt #1",
        "address3": "",
        "city": "Royal Oak",
        "state": "MI",
        "postalCode": "48073",
        "country": "US",
        "phone": "3135496820",
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

order_modify = s.order.modify(id=41949255,json=j)

j = {
    "shipTo": {
        "email": "audrey.horne@greatnothern.com",
        "name": "Audrey Horne",
        "address1": "3615 Crooks Rd.",
        "address2": "Apt #1",
        "address3": "",
        "city": "Royal Oak",
        "state": "MI",
        "postalCode": "48073",
        "country": "US",
        "phone": "3135496820",
        "isCommercial": 0,
        "isPoBox": 0
    }
}

order_modify = s.order.modify(id=41949255,json=j)

