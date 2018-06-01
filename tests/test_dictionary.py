import unittest
from boggle.dictionary import Dictionary
from tests import ASSET_PATH

class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.dictionaryClass = Dictionary()
        self.test_word_dictionary = ["eight", "hug", "huge"]

    def test_load_file(self):
        fp = ASSET_PATH + "dictionary.txt"
        self.dictionaryClass.load_from_file(fp)
        self.assertListEqual(self.dictionaryClass.word_dictionary, self.test_word_dictionary)

    def test_generate_trie(self):
        self.dictionaryClass.word_dictionary = self.test_word_dictionary
        self.dictionaryClass.generate_trie()
        self.assertDictEqual(self.dictionaryClass.trie,
                             {'e': {'i': {'g': {'h': {'t': {'leave': True}}}}},
                              'h': {'u': {'g': {'e': {'leave': True},
                                                'leave': True}}}}
                             )

if __name__ == "__main__":
    unittest.main()