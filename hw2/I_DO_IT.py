import sys
from os import walk
from os import path
from hashlib import sha1 as hasher

def getHash(direct):
    with open(direct, 'rb') as file:
        hasher = hasher()
        part = f.read(1024) #why not?
        while len(part):
            hasher.update(part)
            part = f.read(1024)
    return hasher.digest()

def getDic(root):
    tree = walk(root)
    dic = {}
    for branch, _, leaves in tree:
        for leave in leaves:
            if leave[0] != "." and leave[0] != "~":
                broom = branch + leave
                dic[getHash(broom)].append(leave) 
    return dic

if __name__ == "__main__":
    dic = getDic(sys.argv[1])
    for _, files in dic:
        for file in files:
            print(file, ":")
