"""
The following class names are paired with the methods listed
at the top of the api module. If you add a method to the api
module you must also add a corresponding Response class below.
"""

import requests

HTTP_SUCCESS = 200
SHIPWIRE_GET_ALL_LIMIT = 200


class ShipwireResponse(object):
    def __init__(self, response, shipwire_instance):
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
        self.shipwire = shipwire_instance


class ListResponse(ShipwireResponse):
    def __init__(self, response, shipwire_instance):
        super(ListResponse, self).__init__(response, shipwire_instance)

        # check to make sure that you have a valid response
        if self.status is not HTTP_SUCCESS:
            return

        r = self.resource
        self.total = r.get('total')
        self.previous = r.get('previous')
        self.next = r.get('next')
        self.__next__ = r.get('next')
        self.offset = r.get('offset')
        self.items = r.get('items')
        self.limit = len(self.items)
        self.all_serial = self._get_all_serial
        self.all = self.all_serial

    def _get_all_serial(self):
        # loop over all items with previous and next
        next_uri = self.__next__
        req = self.response.request
        items = self.items

        while next_uri:
            resp = requests.request(req.method, next_uri, auth=self.shipwire.auth)
            list_resp = ListResponse(resp, self.shipwire)
            items.extend(list_resp.items)
            next_uri = list_resp.__next__

        return items


class CreateResponse(ListResponse):
    pass


class GetResponse(ShipwireResponse):
    pass


class ModifyResponse(ShipwireResponse):
    pass


class DeleteResponse(ShipwireResponse):
    pass


class CancelResponse(ShipwireResponse):
    pass


class ShipmentsResponse(ListResponse):
    pass


class Instructions_recipientsResponse(ListResponse):
    pass


class Cancel_labelsResponse(ListResponse):
    pass


class HoldsResponse(ListResponse):
    pass


class LabelsResponse(ListResponse):
    pass


class Clear_holdsResponse(ShipwireResponse):
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


class Split_ordersResponse(ListResponse):
    pass
