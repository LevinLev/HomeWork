# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    newlist = []
    newlst.append(lst[0])
    last = lst[0]
    for i in range [1, len(lst)]:
        if lst[i] != last:
            last = lst[i]
            newlist.append(lst[i])
    return lst

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst = []
    it1 = 0
    it2 = 0
    for i in range (0, size1 + size2):
        if it1 == len(lst1) - 1:
            while it2 < len(lst2):
                lst.append(lst2[it2])
                it2 += 1
            break
        elif it2 == len(lst2) - 1:
            while it1 < len(lst1):
                lst.append(lst1[it1])
                it1 += 1
            break
        elif lst1[it1] < lst2[it2]:
            lst.append(lst1[it1])
            it1 += 1
        else:
            lst.append(lst2[it2])
            it2 += 2
    return lst
