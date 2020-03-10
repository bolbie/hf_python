def search_for_vowels(phrase:str) -> set:
    """Returns the vowels found in the entered phrase."""
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))
