def search_for_vowels(word):
    """Returns the vowels found in the entered word."""
    vowels = set('aeiou')
    found = vowels.intersection(set(word))
    return found

