import requests

HTTP_SUCCESS = 200

class ShipwireResponse(object):
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
        self.warnings = j.get('warnings')
        self.errors = j.get('errors')

"""
The following class names are paired with the methods listed
at the top of the api module. If you add a method to the api
module you must also add a corresponding Response class below.
"""

class ListResponse(ShipwireResponse):
    def __init__(self, response):
        super(ListResponse, self).__init__(response)

        #check to make sure that you have a valid response
        if self.status is not HTTP_SUCCESS:
            return

        r = self.resource
        self.total =  r.get('total')
        self.previous = r.get('previous')
        self.next = r.get('next')
        self.offset = r.get('offset')
        self.items = r.get('items')
        self.limit = len(self.items)
        self.all = self._get_all

    def _get_all(self):
        # loop over all items with previous and next
        next = self.next
        req = self.response.request
        items = self.items

        while next:
            resp = requests.request(req.method, next, headers=req.headers)
            list_resp = ListResponse(resp)
            items.extend(list_resp.items)
            print next
            next = list_resp.next

        return items

class CreateResponse(ListResponse):
    pass

class GetResponse(ShipwireResponse):
    pass

class ModifyResponse(ShipwireResponse):
    pass

class HoldsResponse(ListResponse):
    pass

class ItemsResponse(ListResponse):
    pass

class ReturnsResponse(ListResponse):
    pass

class TrackingsResponse(ListResponse):
    pass

class ProductsResponse(ListResponse):
    pass

class QuoteResponse(ShipwireResponse):
    pass
