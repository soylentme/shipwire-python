class ShipwireResponse():
    def __init__(self, response):
        r = response
        self.response = r
        j = r.json()
        self.json = j
        self.status = j.get('status')
        self.message = j.get('message')
        self.location = j.get('resourceLocation')
        self.resource_location = self.location
        self.resource = j.get('resource')

"""
The following class names are paired with the methods listed
at the top of the api module. If you add a method to the api
module you must also add a corresponding Response class below.
"""

class ListResponse(ShipwireResponse):
    pass

class CreateResponse(ShipwireResponse):
    pass

class GetResponse(ShipwireResponse):
    pass

class ModifyResponse(ShipwireResponse):
    pass

class HoldsResponse(ShipwireResponse):
    pass

class ItemsResponse(ShipwireResponse):
    pass

class ReturnsResponse(ShipwireResponse):
    pass

class TrackingsResponse(ShipwireResponse):
    pass

class ProductsResponse(ShipwireResponse):
    pass

class QuoteResponse(ShipwireResponse):
    pass
