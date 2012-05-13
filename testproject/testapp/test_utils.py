def format_list(l, separator=' ', sort=True):
    """
    Make string of list. Also sort the list.
    E.g. [1, 2, 3] -> '1 2 3'
    """
    if sort:
        l = sorted(unicode(n) for n in l)
    else:
        l = [unicode(n) for n in l]
    return separator.join(l)