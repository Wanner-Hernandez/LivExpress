import re

def filter_hashtags(iterable):
    # Filter strings from iterable and return only letters and numbers
    # ignore other Chars
    res = []

    for string in iterable:
        filter_string = "".join(re.split("[^a-zA-Z0-9]*", string))
        res.append(filter_string)
    return res

if __name__ == "__main__":
    x = ["#sgew", "@aerta", "i3#"]
    filtered = filter_hashtags(x)
    print(filtered)