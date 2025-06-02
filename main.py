from test_app import TestApp
import unittest

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApp)
    unittest.TextTestRunner().run(suite)
