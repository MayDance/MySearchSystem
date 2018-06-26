def merge_list(list1, list2):
    rlist = list(set(list1 + list2))
    return rlist


def and_list(list1, list2):
    rlist = list(set(list1) & set(list2))
    return rlist


def minus_list(list1, list2):
    rlist = list(set(list1) - set(list2))
    return rlist
