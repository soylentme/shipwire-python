from unittest import TestCase

from shipwire import responses

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch


def fake_response(payload):
    json_fn = MagicMock(return_value=dict(payload))
    return MagicMock(json=json_fn)


def fake_list_response(items, next=None):
    return fake_response({
        'status': 200, 'resource': {'items': items, 'next': next}})


class ShipwireResponseTestCase(TestCase):
    def test_provides_resource(self):
        resource = dict(id=123456)
        response = fake_response({'resource': resource})
        obj = responses.ShipwireResponse(response, MagicMock())

        self.assertEqual(resource, obj.resource)


class ListResponseTestCase(TestCase):
    def test_provides_items(self):
        item = dict(resource=dict(id=123456))
        items = dict(items=[item])
        response = fake_response({'status': 200, 'resource': items})
        obj = responses.ListResponse(response, MagicMock())

        self.assertEqual([item], obj.items)

    def test_provides_next(self):
        item = dict(resource=dict(id=123456))
        items = dict(next=1234567, items=[item])
        response = fake_response({'status': 200, 'resource': items})
        obj = responses.ListResponse(response, MagicMock())

        self.assertEqual(items['next'], obj.next)

    @patch('shipwire.responses.requests.request')
    def test_all_calls_until_end(self, mock):
        initial_response = fake_list_response([], next=10)
        subsequent = [20, 30, 40, None]

        mock.side_effect = [fake_list_response([], next=p) for p in subsequent]

        sw_response = responses.ListResponse(initial_response, MagicMock())
        sw_response.all_serial()

        self.assertEqual(len(subsequent), mock.call_count)

    @patch('shipwire.responses.requests.request')
    def test_all_returns_all_items(self, mock):
        initial_response = fake_list_response([0], next=10)
        subsequent = [20, 30, 40, None]

        mock.side_effect = [fake_list_response([i + 1], next=p)
                            for i, p in enumerate(subsequent)]

        sw_response = responses.ListResponse(initial_response, MagicMock())
        self.assertEqual([0, 1, 2, 3, 4], sw_response.all_serial())
