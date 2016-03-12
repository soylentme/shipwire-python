import copy

import requests

from . import responses
from .exceptions import ResponseError, ShipwireError, TimeoutError

""" Add or remove methods and API calls here. """
METHODS = {
    'order': {
        'create': ['POST', 'orders'],
        'get': ['GET', 'orders', ''],
        'modify': ['PUT', 'orders', ''],
        'cancel': ['POST', 'orders', '/cancel'],
        'holds': ['GET', 'orders', '/holds'],
        'clear_holds': ['POST', 'orders', '/holds/clear'],
        'items': ['GET', 'orders', '/items'],
        'returns': ['GET', 'orders', '/returns'],
        'trackings': ['GET', 'orders', '/trackings'],
        'list': ['GET', 'orders'],
        'split_orders': ['GET', 'orders', '/splitOrders'],
    },
    'orders': {
        'list': ['GET', 'orders']
    },
    'stock': {
        'products': ['GET', 'stock']
    },
    'rate': {
        'quote': ['POST', 'rate']
    },
    'receiving': {
        'list': ['GET', 'receivings'],
        'create': ['POST', 'receivings'],
        'get': ['GET', 'receivings', ''],
        'modify': ['PUT', 'receivings', ''],
        'cancel': ['POST', 'receivings', '/cancel'],
        'cancel_labels': ['POST', 'receivings', '/labels/cancel'],
        'holds': ['GET', 'receivings', '/holds'],
        'instructions_recipients': ['GET', 'receivings',
                                    '/instructionsRecipients'],
        'items': ['GET', 'receivings', '/items'],
        'shipments': ['GET', 'receivings', '/shipments'],
        'trackings': ['GET', 'receivings', '/trackings'],
        'labels': ['GET', 'receivings', '/labels'],
    },
    'returns': {
        'list': ['GET', 'returns'],
        'create': ['POST', 'returns'],
        'get': ['GET', 'returns', ''],
        'cancel': ['POST', 'returns', '/cancel'],
        'holds': ['GET', 'returns', '/holds'],
        'items': ['GET', 'returns', '/items'],
        'trackings': ['GET', 'returns', '/trackings'],
        'labels': ['GET', 'returns', '/labels'],
    },
    'webhooks': {
        'list': ['GET', 'webhooks'],
        'create': ['POST', 'webhooks'],
        'get': ['GET', 'webhooks', ''],
        'modify': ['PUT', 'webhooks', ''],
        'delete': ['DELETE', 'webhooks', '']
    },
    'secrets': {
        'list': ['GET', 'secret'],
        'create': ['POST', 'secret'],
        'get': ['GET', 'secret', ''],
        'delete': ['DELETE', 'secret', '']
    }
}


class Shipwire():
    """ Shipwire API class."""
    def __init__(self, username='neil@example.com', password='your-password',
                 host='api.shipwire.com', api_version=3, secure=True,
                 raise_on_errors=False, timeout=None, **kwargs):
        self.host = host
        self.api_version = api_version
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.secure = secure
        self.resource  = False
        self.method = False
        self.call_params = False
        self.json = ''
        self.uri = ''
        self.raise_on_errors = raise_on_errors
        self.timeout = timeout

    def __getattr__(self, name):
        if name.startswith('__') or self.method:
            """ can't chain another attribute after the method and
            when __ the copying causes recurssion. """
            raise AttributeError(name)
        elif self.resource:
            if name in list(METHODS[self.resource].keys()):
                self.method = name
            else:
                raise ShipwireError('The \'%s\' attribute is not currently defined.'
                                    % name)
        else: # since self.resource and method_call_dict are empty this must be resource.
            if name in METHODS:
                self.resource = name
            else:
                raise ShipwireError('The \'%s\' resource is not currently defined.'
                                    % name)
        new_instance = copy.copy(self)
        self.resource = self.method = False
        return new_instance

    def __call__(self, *args, **kwargs):
        if self.method is False: # only run calls on methods, not resources.
            raise ShipwireError('Parameters can only be passed to specific methods.')
        if 'json' in kwargs:
            self.json = kwargs.pop('json')
        self.call_params = kwargs
        return self._call_api()

    def _call_api(self):
        self.uri = uri = self._make_uri()
        endpoint = METHODS[self.resource][self.method]
        http_method = endpoint[0]

        try:
            res = requests.request(http_method, uri, auth=self.auth,
                                   params=self.call_params,
                                   json=self.json, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise TimeoutError(exc)

        if res.status_code >= 400 and self.raise_on_errors:
            raise ResponseError(res)

        # wrap response is response classes.
        return getattr(responses, self._class_name())(res, self)

    def _class_name(self):
        return '%sResponse' % self.method.capitalize()

    def _make_uri(self):
        endpoint = METHODS[self.resource][self.method]
        number_words = len(endpoint)
        protocol = 'https' if self.secure else 'http'
        resource = endpoint[1]
        base = "%s://%s/api/v%s" % (protocol, self.host,
                                    self.api_version)
        if number_words == 2: #ex: ['GET', 'orders']
            uri = "%s/%s" % (base, resource)
        elif number_words == 3: #ex: ['GET', 'orders', 'returns']
            if 'id' not in self.call_params:
                raise ShipwireError('An \'id\' is required for this api call.')
            method = endpoint[2]
            uri = "%s/%s/%s%s" % (base, resource,
                                  self.call_params.get('id'),
                                  method)
        return uri
