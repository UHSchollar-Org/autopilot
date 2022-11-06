def same_items(list1, list2):
    if len(list1) != len(list2):
        return False
    for item in list1:
        if item not in list2:
            return False
    return True


