import sys, os
from boggle import ASSET_PATH

class Dictionary:
    def __init__(self, fp=None, redisConn=None):
        self.trie = None
        self.word_dictionary = None

        if fp:
            self.load_from_file(fp)
            self.generate_trie()

    def load_from_file(self, fp):
        with open(fp, 'r',encoding="utf-8") as dictionaryFile:
            self.word_dictionary =  sorted([i.strip().lower() for i in dictionaryFile.readlines()])

    def generate_trie(self):
        # use Dict for now
        self.trie = {}
        for word in self.word_dictionary:
            trieNode = self.trie
            for char in word:
                if char not in trieNode:
                    trieNode[char] = {}
                trieNode = trieNode[char]
            trieNode["leave"] = True

    def get_trie(self):
        if not self.trie:
            self.trie = self.generate_trie()
        return self.trie

    def get_word_dictionary(self):
        return self.word_dictionary

    def dictionary_from_database(self):
        pass