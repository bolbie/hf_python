def search_for_vowels(word):
    """Returns a boolean value depending on
       the presence of any vowels."""
    vowels = set('aeiou')
    found = vowels.intersection(set(word))
    return bool(found)

