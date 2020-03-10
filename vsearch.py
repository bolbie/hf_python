def search_for_vowels(word):
    """Output vowels found in the entered word."""
    vowels = set('aeiou')
    found = vowels.intersection(set(word))
    for vowel in found:
        print(vowel)
