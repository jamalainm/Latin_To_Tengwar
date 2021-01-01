#!/usr/bin/env python3
"""
This file converts the latin alphabet to the character encoding
used by the tengwar annatar font. It will not display tengwar
without the font being installed, too.
"""

class LatinText(latin_string):
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

