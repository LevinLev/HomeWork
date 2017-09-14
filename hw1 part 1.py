# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    last = lst[0]
    i = 1
    while i < len(lst):
        if lst[i] == last:
            del lst[i]
        else:
            last = lst[i]
            i = i + 1
    return lst

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst = []
    for i in range (0, len(lst1) + len(lst2)):
        if len(lst1) == 0:
            while len(lst2) > 0:
                lst.append(lst2[0])
                del lst2[0]
                i = i + 1
            break
        elif len(lst2) == 0:
            while len(lst1) > 0:
                lst.append(lst1[0])
                del lst1[0]
                i = i + 1
            break
        elif lst1[0] < lst2[i]:
            lst.append(lst1[0])
            del lst1[0]
        else:
            lst.append(lst2[0])
            del lst2[0]
    return lst
