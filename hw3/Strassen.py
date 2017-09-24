import numpy as np
import sys

def up_to_2pow(n):
    return 1 << (n - 1).bit_length()

def get_len():
    return input()

def print_matrix(M, lenM):
    
    for i in range (0, lenM):
        for j in range (0, lenM - 1):
            sys.stdout.write(str(M[i, j]) + " ")
        print(str(M[i, lenM - 1]))

def get_matrix(lenM):
    M = np.zeros((up_to_2pow(lenM), up_to_2pow(lenM)))
    for i in range (0, lenM):
        S = input().split()
        for j in range (0, len(S)):
            M[i, j] = int(S[j])
    for i in range (lenM, up_to_2pow(lenM)):
        for j in range (0, up_to_2pow(lenM)):
            M[i, j] = 0
    for i in range (0, lenM):
        for j in range (lenM, up_to_2pow(lenM)):
            M[i, j] = 0
    return M

def part_matrix(M):
    V1, V2 = np.vsplit(M, 2)
    M11, M21 = np.hsplit(V1, 2)
    M12, M22 = np.hsplit(V2, 2)
    return M11, M12, M21, M22

def build_matrix(M11, M12, M21, M22):
    lenm, _ = M11.shape
    lenM = lenm * 2
    M = np.zeros((lenM, lenM))
    M[:lenm, :lenm] = M11
    M[:lenm, lenm:lenM] = M12
    M[lenm:lenM, :lenm] = M21
    M[lenm:lenM, lenm:lenM] = M22
    return M

def multiply_strassen(A, B):
    lenC, _ = A.shape
    if lenC <= 32:
        return A * B
    else:
        lenc = lenC // 2
        A11, A12, A21, A22 = part_matrix(A)
        B11, B12, B21, B22 = part_matrix(B)
        P1 = multiply_strassen(A11 + A22, B11 + B12)
        P2 = multiply_strassen(A21 + A22, B11)
        P3 = multiply_strassen(A11, B12 - B22)
        P4 = multiply_strassen(A22, B21 - B11)
        P5 = multiply_strassen(A11 + A12, B22)
        P6 = multiply_strassen(A21 - A11, B11 + B12)
        P7 = multiply_strassen(A12 - A22, B21 + B22)
        C11 = P1 + P4 - P5 + P7
        C12 = P3 + P5
        C21 = P2 + P4
        C22 = P1 - P2 + P3 + P6
        return build_matrix(C11, C12, C21, C22)

if __name__ == "__main__":
    size = int(get_len())
    A = get_matrix(size)
    lenA = up_to_2pow(size)
    B = get_matrix(size)
    print_matrix(multiply_strassen(A, B), size)

    
