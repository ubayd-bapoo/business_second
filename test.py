import unittest

from main import app


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_no_main_page_correct_code(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_no_main_page_incorrect_code(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertNotEqual(response.status_code, 200)

    def test_api_url(self):
        response = self.app.get('/api/v1/bus_sec', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_endpoints_url(self):
        response = self.app.get('/api/v1/bus_sec?end_time=2020-03-29T10:30:45-06:00', follow_redirects=True)
        self.assertEqual(response.data.decode('ascii'), 'Request missing start time or end time')

    def test_api_endpoints_incorrect_date(self):
        response = self.app.get('/api/v1/bus_sec?start_time=2020-03-29T10:05:45-06:00&end_time=2020-03-52T10:30:45-06:00', follow_redirects=True)
        self.assertEqual(response.data.decode('ascii'), 'Invalid time data/format')

    def test_api_endpoints_incorrect_data(self):
        response = self.app.get('/api/v1/bus_sec?start_time=Hello&end_time=2020-03-52T10:30:45-06:00', follow_redirects=True)
        self.assertEqual(response.data.decode('ascii'), 'Invalid time data/format')

    def test_api_endpoints_weekday_output_incorrect(self):
        response = self.app.get('/api/v1/bus_sec?start_time=2020-03-16T12:04:45-06:00&end_time=2020-03-24T18:01:00-06:00', follow_redirects=True)
        self.assertNotEqual(int(response.data), 114915)

    def test_api_endpoints_weekday_output_correct(self):
        response = self.app.get('/api/v1/bus_sec?start_time=2020-03-16T12:04:45-06:00&end_time=2020-03-19T18:01:00-06:00', follow_redirects=True)
        self.assertEqual(int(response.data), 114915)


if __name__ == "__main__":
    unittest.main()
