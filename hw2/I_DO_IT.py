import sys
from os import walk
from os import path
from hashlib import sha1 as hasher

def getHash(direct):
    with open(direct, 'rb') as f:
        hashe = hasher()
        part = f.read(2048) #optimal desigion for my comp.
        while len(part):
            hashe.update(part)
            part = f.read(2048)
    return hashe.digest()

def getDic(root):
    tree = walk(root)
    dic = {}
    hsh = " "
    for branch, _, leaves in tree:
        if os.path.islink(branch) == 0:
            for leave in leaves:
                if leave[0] != "." and leave[0] != "~":
                    broom = branch + '/' + leave
                    hsh = getHash(broom)
                    if hsh in dic:
                        dic[hsh].append(leave)
                    else:
                        dic[hsh] = []
                        dic[hsh].append(leave)
    return dic

if __name__ == "__main__":
    dic = getDic(sys.argv[1])
    for _, files in dic:
        if len(files) > 1:
            print(":".join(files))
