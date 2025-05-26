import unittest
from explorer import DirectoryExplorer, DirectoryActor

class TestDirectoryExplorer(unittest.TestCase):

    def setUp(self):
        self.dir_actor = DirectoryActor()
        self.dir_explorer = DirectoryExplorer()

        self.dir_actor.create_dir('', 'test_dir')
        self.dir_actor.create_file()