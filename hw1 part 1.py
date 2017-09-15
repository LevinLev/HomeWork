# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    newlist = []
    newlist.append(lst[0])
    last = lst[0]
    for i in range [1, len(lst)]:
        if lst[i] != last:
            last = lst[i]
            newlist.append(lst[i])
    return newlist

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst = []
    it1 = 0
    it2 = 0
    size1 = len(lst1)
    size2 = len(lst2)
    while it1 < size1 && it2 < size2:
        if lst1[it1] < lst2[it2]:
            lst.append(lst1[it1])
            it1 += 1
        else:
            lst.append(lst2[it2])
            it2 += 1
    if it1 == size1 - 1:
        while it2 < size2:
            lst.append(lst2[it2])
            it2 += 1
    else it2 == size2 - 1:
        while it1 < size1:
            lst.append(lst1[it1])
            it1 += 1
    return lst
