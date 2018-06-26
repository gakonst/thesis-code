def normalize(d):
    if type(d) is str:
        return bytes(d, 'utf-8')
    elif type(d) is list:
        return [bytes(x, 'utf-8') for x in d]
    else:
        return d

def sort_by_depth(d, reverse=True):
    return sorted(
            d,
            key = lambda x: x.count('::'),
            reverse=reverse
    )
