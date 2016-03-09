from unittest import TestCase

from requests.exceptions import ConnectTimeout, ReadTimeout

from shipwire import api, responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class StubResponse(object):
    "A canned response with a similar API to requests.Response"

    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self):
        return self._json

    @property
    def content(self):
        return str(self.json())


class ShipwireTestCase(TestCase):
    def setUp(self):
        patcher = patch('shipwire.requests.request')
        self.addCleanup(patcher.stop)
        self.request = patcher.start()

        self.request.return_value = StubResponse(200, {})

        self.client = api.Shipwire()

    def assert_url(self, client, url):
        base = '{}://{}/api/v{}'.format(
            'https' if client.secure else 'http',
            client.host, client.api_version)

        actual = api.requests.request.call_args[0][1]
        self.assertEqual(base + url, actual)

    def assert_method(self, method):
        actual = api.requests.request.call_args[0][0]
        self.assertEqual(method.upper(), actual.upper())

    def assert_url_method(self, client, method, url):
        self.assert_method(method)
        self.assert_url(client, url)

    def test_get_resource(self):
        for resource in api.METHODS:
            resource_client = getattr(self.client, resource)
            self.assertEqual(resource, resource_client.resource)

    def test_get_resource_immutable(self):
        for resource in api.METHODS:
            self.assertIsNot(self.client, getattr(self.client, resource))
            self.assertNotEqual(resource, self.client.resource)

    def test_get_invalid_resource(self):
        with self.assertRaises(api.ShipwireError):
            self.client.not_a_real_resource

    def test_get_invalid_method(self):
        for resource in api.METHODS:
            with self.assertRaises(api.ShipwireError):
                getattr(self.client, resource).not_a_real_method

    def test_call_on_uninitialized_client(self):
        with self.assertRaises(api.ShipwireError):
            self.client()

    def test_call_on_client_without_method(self):
        with self.assertRaises(api.ShipwireError):
            self.client.orders()

    def test_call_generates_correct_order_url(self):
        self.client.orders.list()
        self.assert_url_method(self.client, 'GET', '/orders')

        # For backwards-compatibility reasons, list can be called on either
        # ``orders`` or ``order``.
        self.client.order.list()
        self.assert_url_method(self.client, 'GET', '/orders')

        self.client.order.create()
        self.assert_url_method(self.client, 'POST', '/orders')

        self.client.order.get(id=12345)
        self.assert_url_method(self.client, 'GET', '/orders/12345')

        self.client.order.modify(id=54321)
        self.assert_url_method(self.client, 'PUT', '/orders/54321')

        self.client.order.items(id=12345)
        self.assert_url_method(self.client, 'GET', '/orders/12345/items')

        self.client.order.holds(id=12345)
        self.assert_url_method(self.client, 'GET', '/orders/12345/holds')

        self.client.order.returns(id=12345)
        self.assert_url_method(self.client, 'GET', '/orders/12345/returns')

        self.client.order.trackings(id=12345)
        self.assert_url_method(self.client, 'GET', '/orders/12345/trackings')

    def test_call_generates_correct_stock_urls(self):
        self.client.stock.products()
        self.assert_url_method(self.client, 'GET', '/stock')

    def test_call_generates_correct_rate_urls(self):
        self.client.rate.quote()
        self.assert_url_method(self.client, 'POST', '/rate')

    def test_call_generates_correct_receiving_urls(self):
        self.client.receiving.list()
        self.assert_url_method(self.client, 'GET', '/receivings')

        self.client.receiving.create()
        self.assert_url_method(self.client, 'POST', '/receivings')

        self.client.receiving.get(id=12345)
        self.assert_url_method(self.client, 'GET', '/receivings/12345')

        self.client.receiving.modify(id=12345)
        self.assert_url_method(self.client, 'PUT', '/receivings/12345')

        self.client.receiving.cancel(id=12345)
        self.assert_url_method(self.client, 'POST', '/receivings/12345/cancel')

        self.client.receiving.cancel_labels(id=5)
        self.assert_url_method(self.client, 'POST',
                               '/receivings/5/labels/cancel')

        self.client.receiving.holds(id=54321)
        self.assert_url_method(self.client, 'GET', '/receivings/54321/holds')

        self.client.receiving.instructions_recipients(id=54321)
        self.assert_url_method(self.client, 'GET',
                               '/receivings/54321/instructionsRecipients')

        self.client.receiving.items(id=54321)
        self.assert_url_method(self.client, 'GET', '/receivings/54321/items')

        self.client.receiving.shipments(id=54321)
        self.assert_url_method(self.client, 'GET',
                               '/receivings/54321/shipments')

        self.client.receiving.trackings(id=54321)
        self.assert_url_method(self.client, 'GET',
                               '/receivings/54321/trackings')

    def test_call_generates_correct_webhooks_urls(self):
        self.client.webhooks.list()
        self.assert_url_method(self.client, 'GET', '/webhooks')

        self.client.webhooks.create()
        self.assert_url_method(self.client, 'POST', '/webhooks')

        self.client.webhooks.get(id=12345)
        self.assert_url_method(self.client, 'GET', '/webhooks/12345')

        self.client.webhooks.modify(id=12345)
        self.assert_url_method(self.client, 'PUT', '/webhooks/12345')

        self.client.webhooks.delete(id=12345)
        self.assert_url_method(self.client, 'DELETE', '/webhooks/12345')

    def test_call_requires_id_on_instance_operations(self):
        with self.assertRaises(api.ShipwireError):
            self.client.order.get(json={})

    def test_call_requests_with_auth(self):
        self.client.order.get(id=12345)
        auth = api.requests.request.call_args[1]['auth']
        self.assertEqual(self.client.auth, auth)

    def test_call_respects_secure(self):
        self.client.secure = True
        self.client.order.get(id=12345)
        uri = api.requests.request.call_args[0][1]
        self.assertTrue(uri.startswith('https://'))

    def test_call_respects_insecure(self):
        self.client.secure = False
        self.client.order.get(id=12345)
        uri = api.requests.request.call_args[0][1]
        self.assertTrue(uri.startswith('http://'))

    def test_call_raises_on_400_status_when_indicated(self):
        self.client.raise_on_errors = True
        self.request.return_value = StubResponse(403, {})

        with self.assertRaises(api.ResponseError):
            self.client.order.get(id=12345)

    def test_call_raises_on_500_status_when_indicated(self):
        self.client.raise_on_errors = True
        self.request.return_value = StubResponse(500, {})

        with self.assertRaises(api.ResponseError):
            self.client.order.get(id=12345)

    def test_call_doesnt_raise_when_indicated(self):
        self.client.raise_on_errors = False
        self.request.return_value = StubResponse(500, {})

        self.client.order.get(id=12345)

    def test_call_supports_timeouts(self):
        self.client.timeout = expected = (1.2, 3.4)
        self.client.order.get(id=12345)

        self.assertEqual(expected,
                         self.request.call_args[1]['timeout'])

    def test_call_wraps_connect_timeouts(self):
        self.client.timeout = 5.0
        self.request.side_effect = ConnectTimeout()

        with self.assertRaises(api.TimeoutError):
            self.client.order.get(id=12345)

    def test_call_wraps_read_timeouts(self):
        self.client.timeout = 5.0
        self.request.side_effect = ReadTimeout()

        with self.assertRaises(api.TimeoutError):
            self.client.order.get(id=12345)

    def test_call_returns_correct_order_class(self):
        self.assertIsInstance(self.client.order.list(),
                              responses.ListResponse)

        self.assertIsInstance(self.client.orders.list(),
                              responses.ListResponse)

        self.assertIsInstance(self.client.order.get(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.order.modify(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.order.cancel(id=1234),
                              responses.CancelResponse)

        self.assertIsInstance(self.client.order.holds(id=1234),
                              responses.ListResponse)

        self.assertIsInstance(self.client.order.items(id=1234),
                              responses.ListResponse)

        self.assertIsInstance(self.client.order.returns(id=1234),
                              responses.ListResponse)

        self.assertIsInstance(self.client.order.trackings(id=1234),
                              responses.ListResponse)

    def test_call_returns_correct_stock_response(self):
        self.assertIsInstance(self.client.stock.products(),
                              responses.ListResponse)

    def test_call_returns_correct_rate_response(self):
        self.assertIsInstance(self.client.rate.quote(),
                              responses.ShipwireResponse)

    def test_call_returns_correct_receiving_response(self):
        self.assertIsInstance(self.client.receiving.list(),
                              responses.ListResponse)

        self.assertIsInstance(self.client.receiving.create(),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.get(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.modify(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.cancel(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.cancel_labels(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.holds(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(
            self.client.receiving.instructions_recipients(id=1234),
            responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.items(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.shipments(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.receiving.trackings(id=1234),
                              responses.ShipwireResponse)

    def test_call_returns_correct_webhooks_response(self):
        self.assertIsInstance(self.client.webhooks.list(),
                              responses.ListResponse)

        self.assertIsInstance(self.client.webhooks.create(),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.webhooks.get(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.webhooks.modify(id=1234),
                              responses.ShipwireResponse)

        self.assertIsInstance(self.client.webhooks.delete(id=1234),
                              responses.ShipwireResponse)
