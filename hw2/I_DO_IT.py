import sys
import timeit
from os import walk
from os import path
from hashlib import sha1 as hasher

def getHash(direct):
    with open(direct, 'rb') as f:
        hashe = hasher()
        part = f.read(65536) #optimal desigion for my comp.
        while len(part):
            hashe.update(part)
            part = f.read(65536)
    return hashe.digest()

def getDic(root):
    tree = walk(root)
    dic = {}
    for branch, _, leaves in tree:
            for leave in leaves:
                if not leave.startwith('.') and not leave.startwith("~"):
                    broom = path.join(branch, leave)
                    hsh = getHash(broom)
                    if hsh not in dic:
                        dic[hsh] = []  
                    dic[hsh].append(leave)
    return dic

if __name__ == "__main__":
    dic = getDic(sys.argv[1])
    for files in dic.values():
        if len(files) > 1:
            print(":".join(files))
