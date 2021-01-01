#!/usr/bin/env python3
"""
This file converts the latin alphabet to the character encoding
used by the tengwar annatar font. It will not display tengwar
without the font being installed, too.
"""

import re

vowels = ['a','e','i','o','u','á','é','í','ó','ú','ä','ë','ï','ö','ü']

combined_vowels = {
        'a' : 'C',
        'e' : 'F',
        'i' : 'G',
        'o' : 'H',
        'u' : 'J',
        'ä' : 'C',
        'ë' : 'F',
        'ï' : 'G',
        'ö' : 'H',
        'ü' : 'J',
        }

long_vowels = {
        'á' : '~C',
        'é' : '~F',
        'í' : '~G',
        'ó' : '~H',
        'ú' : '~J',
        }

independent_vowels = {
        'a' : '`C',
        'e' : '`F',
        'i' : '`G',
        'o' : '`H',
        'u' : '`J',
        'ä' : '`C',
        'ë' : '`F',
        'ï' : '`G',
        'ö' : '`H',
        'ü' : '`J',
        'á' : '~C',
        'é' : '~F',
        'í' : '~G',
        'ó' : '~H',
        'ú' : '~J',
        }

doubles = {
        'ñw' : 'b',
        'rd' : 'u',
        'ld' : 'm',
        'ss' : ',',
        'qu' : 'z',
        'nd' : '2',
        'mb' : 'w',
        'ng' : 's',
        'ch' : 'd',
        'hw' : 'c',
        'nt' : '4',
        'mp' : 'r',
        'nc' : 'f',
        'ai' : 'lC',
        'au' : '.C',
        'oi' : 'lH',
        'ui' : 'lJ',
        'eu' : '.F',
        'iu' : '.G',
        'ty' : '1Ì',
        'sy' : 'iÌ',
        'ny' : '5Ì',
        'ry' : '7Ì',
        'ly' : 'jÌ',
        'tt' : "1'",
        'nn' : "5'",
        'll' : "j'",
        'mm' : "t'",
        }

triples = {
        'ngw': 'x',
        'nqu': 'v',
        'ndy': '2Ì',
        'nty': '4Ì',
        }

consonants = {
        't' : '1',
        'p' : 'q',
        'c' : 'a',
        'k' : 'a',
        'f' : 'e',
        'n' : '5',
        'm' : 't',
        'ñ' : 'g',
        'r' : '7',
        'v' : 'y',
        'y' : 'h',
        'w' : 'n',
        'l' : 'j',
        'h' : 'd',
        's' : 'i',
        }

initial_consonant = {
        'h' : '9'
        }

class LatinText:
    """
    This object can be processed into words, The Latin characters
    of that word can then be translated to the encodings used by
    the Tengwar Annatar font to represent the same sounds.

    The object does assume that the string passed to the class
    is written using the conventions of representing Quenya
    with the Latin alphabet, as you might find in Tolkien's
    published works.

    ...
    Attributes
    words : list
        This is a list of words generated from the submitted string

    """
    def __init__(self,latin_string):
        self.latin_string = latin_string
        self.words = re.split("\W+",self.latin_string)

class LatinWord:
    """
    This object converts transliterated Quenya into the encoding
    used by the Tengwar Annatar font to represent the Elvish
    script.
    
    ...
    Attributes
    latin_word : str
        This is the original text of the word; it will be truncated
        as the annatar word is built
    latin_word_length : int
        This is the length of the Latin word; it will change as the
        annatar word is being built
    annatar_word : str
        This is a word that will be built piece by piece
    
    """
    def __init__(self,latin_word):
        self.latin_word = latin_word
        self.latin_word_length = len(self.latin_word)
        self.annatar_word = ""

    def transliterate(self):
        first = True
        word_length = len(self.latin_word)
        while word_length > 2:
            """ run through all substitutions """
            if self.triple_check():
                self.triple_substitute()
                word_length -= 3
            elif self.double_check():
                self.double_substitute()
                word_length -= 2
            elif self.initial_vowel_check():
                self.independent_vowel_substitute()
                word_length -= 1
            elif self.initial_h_check():
                self.initial_h_substitute()
                word_length -= 1
            elif self.long_vowel_check():
                self.long_vowel_substitute()
                word_length -= 1
            elif self.preceding_vowel_check():
                self.independent_vowel_substitute()
                word_length -= 1
            elif self.combined_vowel_check():
                self.combined_vowel_substitute()
                word_length -= 1
            elif self.consonant_check():
                self.consonant_substitute()
                word_length -= 1

        while word_length > 1:
            """ run double and signle substitutions, modified doubles """
            if self.double_check():
                self.double_substitute()
                word_length -= 2
            elif self.initial_vowel_check():
                self.independent_vowel_substitute()
                word_length -= 1
            elif self.initial_h_check():
                self.initial_h_substitute()
                word_length -= 1
            elif self.long_vowel_check():
                self.long_vowel_substitute()
                word_length -= 1
            elif self.preceding_vowel_check():
                self.independent_vowel_substitute()
                word_length -= 1
            elif self.combined_vowel_check():
                self.combined_vowel_substitute()
                word_length -= 1
            elif self.consonant_check():
                self.consonant_substitute()
                word_length -= 1

        while word_length > 0:
            """ run individual substitutions """
            if self.initial_vowel_check():
                self.independent_vowel_substitute()
                word_length -= 1
            elif self.initial_h_check():
                self.initial_h_substitute()
                word_length -= 1
            elif self.long_vowel_check():
                self.long_vowel_substitute()
                word_length -= 1
            elif self.preceding_vowel_check():
                self.independent_vowel_substitute()
                word_length -= 1
            elif self.combined_vowel_check():
                self.combined_vowel_substitute()
                word_length -= 1
            elif self.consonant_check():
                self.consonant_substitute()
                word_length -= 1


    def triple_check(self):
        if len(self.latin_word) == 3:
            if self.latin_word in triples.keys():
                return True
        elif self.latin_word[:3] in triples.keys():
            return True
        else:
            return False
            
    def double_check(self):
        if len(self.latin_word) == 2:
            if self.latin_word in doubles.keys():
                return True
        elif self.latin_word[:2] in doubles.keys():
            return True
        else:
            return False

    def triple_substitute(self):
        if len(self.latin_word) == 3:
            self.annatar_word += self.latin_word
            self.latin_word = ""
        else:
            self.annatar_word += triples[self.latin_word[:3]]
            self.latin_word = self.latin_word[3:]

    def double_substitute(self):
        if len(self.latin_word) == 2:
            self.annatar_word += self.latin_word
            self.latin_word = ""
        else:
            self.annatar_word += doubles[self.latin_word[:2]]
            self.latin_word = self.latin_word[2:]

    def initial_vowel_check(self):
        if self.latin_word[0] in vowels and len(self.annatar_word) == 0:
            return True

    def initial_h_check(self):
        if self.latin_word[0] == 'h' and len(self.annatar_word) == 0:
            return True

    def independent_vowel_substitute(self):
        self.annatar_word += independent_vowels[self.latin_word[0]]
        if len(self.latin_word) == 1:
            self.latin_word = ""
        else:
            self.latin_word = self.latin_word[1:]

    def initial_h_substitute(self):
        self.annatar_word += '9'
        if len(self.latin_word) == 1:
            self.latin_word = ""
        else:
            self.latin_word = self.latin_word[1:]

    def preceding_vowel_check(self):
        if len(self.annatar_word) > 0 and self.latin_word[0] in vowels:
            if self.annatar_word[-1] in combined_vowels.values():
                return True
            else:
                return False

    def combined_vowel_check(self):
        if len(self.annatar_word) > 0: 
            if self.latin_word[0] in vowels:
                return True

    def combined_vowel_substitute(self):
        self.annatar_word += combined_vowels[self.latin_word[0]]
        if len(self.latin_word) == 1:
            self.latin_word = ""
        else:
            self.latin_word = self.latin_word[1:]

    def consonant_check(self):
        if self.latin_word[0] in consonants.keys():
            return True

    def consonant_substitute(self):
        self.annatar_word += consonants[self.latin_word[0]]
        if len(self.latin_word) == 1:
            self.latin_word = ""
        else:
            self.latin_word = self.latin_word[1:]

    def long_vowel_check(self):
        if self.latin_word[0] in long_vowels.keys():
            return True

    def long_vowel_substitute(self):
        self.annatar_word += long_vowels[self.latin_word[0]]
        if len(self.latin_word) == 1:
            self.latin_word = ""
        else:
            self.latin_word = self.latin_word[1:]

def transcribe_sentence(sentence):
    latin_sentence = LatinText(sentence)

    words = [w for w in latin_sentence.words]

    quenya_words = []

    for word in words:
        tengwar_word = LatinWord(word)
        tengwar_word.transliterate()
        quenya_words.append(tengwar_word.annatar_word)

    new_sentence = ' '.join(quenya_words)

    return new_sentence


if __name__ == "__main__":
    my_sentence = transcribe_sentence("hísiel cápa nómerya foinallo")
    print(my_sentence)
