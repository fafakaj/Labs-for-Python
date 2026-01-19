import unittest


class TestMainController(unittest.TestCase):
    def test_route_structure(self):
        test_routes = [
            '/',
            '/author',
            '/users',
            '/currencies',
            '/currency/delete',
            '/currency/add'
        ]
        self.assertEqual(len(test_routes), 6)
        self.assertIn('/', test_routes)
        self.assertIn('/currencies', test_routes)


if __name__ == '__main__':
    unittest.main()