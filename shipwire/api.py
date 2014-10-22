import requests
import copy
import responses

SHIPWIRE_AVAILABLE_RESOURCES = ['order', 'orders', 'stock', 'rate']

""" Add or remove methods and API calls here. """
#TODO Add namespacing of keys for possible name collisions.
METHOD_CALL_DICT = {'create': ['POST', 'orders'],
                    'get': ['GET', 'orders', ''],
                    'modify': ['PUT', 'orders', ''],
                    'holds': ['GET', 'orders', '/holds'],
                    'items': ['GET', 'orders', '/items'],
                    'returns': ['GET', 'orders', '/returns'],
                    'trackings': ['GET', 'orders', '/trackings'],
                    'list': ['GET', 'orders'],
                    'products': ['GET', 'stock'],
                    'quote': ['POST', 'rate'], }

class Shipwire():
    """ Shipwire API class."""
    def __init__(self, username='neil@example.com', password='your-password',
                 host='api.shipwire.com', api_version=3, secure=True, **kwargs):
        self.host = host
        self.api_version = api_version
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.secure = secure
        self.resource  = False
        self.method = False
        self.call_params = False
        self.json = ''

    def __getattr__(self, name):
        if name.startswith('__') or self.method:
            """ can't chain another attribute after the method and
            when __ the copying causes recurssion. """
            raise AttributeError(name)
        elif self.resource:
            if name in METHOD_CALL_DICT.keys():
                self.method = name
            else:
                raise ShipwireError('The \'%s\' attribute is not currently defined.'
                                    % name)
        else: # since self.resource and method_call_dict are empty this must be resource.
            if name in SHIPWIRE_AVAILABLE_RESOURCES:
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
        uri = self._make_uri()
        print uri
        http_method = METHOD_CALL_DICT[self.method][0]
        res = requests.request(http_method, uri, auth=self.auth,
                               params=self.call_params,
                               json=self.json)
        # wrap response is response classes.
        return getattr(responses, self._class_name())(res)

    def _class_name(self):
        return '%sResponse' % self.method.capitalize()

    def _make_uri(self):
        number_words = len(METHOD_CALL_DICT[self.method])
        protocol = 'https' if self.secure else 'http'
        resource = METHOD_CALL_DICT[self.method][1]
        base = "%s://%s/api/v%s" % (protocol, self.host,
                                    self.api_version)
        if number_words == 2: #ex: ['GET', 'orders']
            uri = "%s/%s" % (base, resource)
        elif number_words == 3: #ex: ['GET', 'orders', 'returns']
            if 'id' not in self.call_params:
                raise ShipwireError('An \'id\' is required for this api call.')
            method = METHOD_CALL_DICT[self.method][2]
            uri = "%s/%s/%s%s" % (base, resource,
                                  self.call_params.get('id'),
                                  method)
        return uri

class ShipwireError(Exception):
    """
    Base Exception thrown by the Shipwire object when there is a
    general error interacting with the API.
    """
    pass
