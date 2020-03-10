def search_for_vowels(word:str) -> set:
    """Returns the vowels found in the entered word."""
    vowels = set('aeiou')
    return vowels.intersection(set(word))
