from unittest import TestCase
from unittest.mock import patch, MagicMock
from utils import PathJoiner


class TestPathCreator(TestCase):
    def setUp(self):
        self.root = '/root/path'
        self.path_joiner = PathJoiner(self.root)

    def test_join_paths(self):
        first_part = 'directory/dir/'
        second_part = 'path/to/dir'
        result = self.path_joiner.join_paths(first_part, second_part)
        expected_result = f'{first_part}{second_part}'
        self.assertEqual(result, expected_result)

    def test_join_with_root_path(self):
        path = 'path/to/dir'
        expected = f'{self.root}/{path}'
        result = self.path_joiner.join_with_root_path(path)
        self.assertEqual(result, expected)

    def test_create_absolute_entity_path(self):
        storage_id = 'rerer'
        path_in_storage = 'path/to/dir'
        expected = f'{self.root}/{storage_id}/{path_in_storage}'
        result = self.path_joiner.create_absolute_entity_path(storage_id, path_in_storage)
        self.assertEqual(result, expected)
