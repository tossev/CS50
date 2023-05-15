def get_substring(string, length):
    output = set()
    for i, word in enumerate(string):
        word = string[i:i+length]
        if len(word) < length:
            break
        output.add(word)
    return(output)


def duplicates(a, b):
    return a & b


def lines(a, b):
    """Return lines in both a and b"""
    return duplicates(set(a.split('\n')), set(b.split('\n')))


def sentences(a, b):
    """Return sentences in both a and b"""
    from nltk.tokenize import sent_tokenize
    return duplicates(set(sent_tokenize(a)), set(sent_tokenize(b)))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    return duplicates(get_substring(string=a, length=n), get_substring(string=b, length=n))

