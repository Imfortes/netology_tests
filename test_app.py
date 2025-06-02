import unittest
from app import get_doc_owner_name, get_all_doc_owners_names

class TestApp(unittest.TestCase):

    def test_get_doc_owner_name(self):
        self.assertEqual(get_doc_owner_name("10006"), "Аристарх Павлов")
        self.assertEqual(get_doc_owner_name("11-2"), "Геннадий Покемонов")

    def test_get_all_doc_owners_names(self):
        self.assertEqual(get_all_doc_owners_names(), {'Василий Гупкин', 'Геннадий Покемонов', 'Аристарх Павлов'})