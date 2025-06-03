import unittest
import requests
from unittest.mock import patch, MagicMock

from app import (
    add_new_doc,
    get_doc_owner_name,
    get_all_doc_owners_names,
    append_doc_to_shelf,
    remove_doc_from_shelf,
    delete_doc,
    documents,
    directories,
    create_yandex_folder
)


class TestApp(unittest.TestCase):

    def setUp(self):
        self.original_documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]
        self.original_directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

        self.oauth_token = ''
        global documents, directories
        documents = self.original_documents.copy()
        directories = {k: v.copy() for k, v in self.original_directories.items()}

    def test_get_doc_owner_name(self):
        self.assertEqual(get_doc_owner_name("10006"), "Аристарх Павлов")
        self.assertEqual(get_doc_owner_name("11-2"), "Геннадий Покемонов")

    def test_get_all_doc_owners_names(self):
        self.assertEqual(get_all_doc_owners_names(), {'Василий Гупкин', 'Геннадий Покемонов', 'Аристарх Павлов'})

    @patch('__main__.check_document_existance')
    @patch('__main__.remove_doc_from_shelf')
    def test_delete_doc_success(self, mock_remove_doc, mock_check_exist):
        mock_check_exist.return_value = True

        user_document_number = '11-2'

        with patch('builtins.input', return_value=user_document_number):
            deleted_doc, success = delete_doc()

            self.assertEqual(deleted_doc, user_document_number)

            self.assertTrue(success)

            self.assertNotIn({"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"}, documents)

            mock_remove_doc.assert_called_once_with(user_document_number)

    @patch('builtins.input', side_effect=['123456789', 'passport', 'Мишин Кирилл', '3'])
    @patch('__main__.append_doc_to_shelf')
    def test_add_new_doc(self):
        result = add_new_doc()

        self.assertEqual(result, "3")
        self.assertIn("12345", directories["3"])
        self.assertIn(
            {"type": "passport", "number": "12345", "name": "Иван Иванов"},
            documents
        )

    def test_remove_doc_from_shelf(self):
        remove_doc_from_shelf("11-2")
        self.assertNotIn("11-2", directories["1"])
        self.assertEqual(len(directories["1"]), 2)



    @patch('requests.put')
    def test_create_yandex_folder_success(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_put.return_value = mock_response

        result = create_yandex_folder("test_folder", self.oauth_token)

        self.assertTrue(result)
        mock_put.assert_called_once_with(
            'https://cloud-api.yandex.net/v1/disk/resources',
            headers={'Authorization': self.oauth_token},
            params={'path': 'test_folder'}
        )

