
def search_for_vowels(phrase: str) -> set:
    """Returns the vowels found in the entered phrase."""
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))


def search_for_letters(phrase: str, letters: str='aeuio') -> set:
    """Return a set() of the 'letters' found in the entered 'phrase'."""
    return set(letters).intersection(set(phrase))
