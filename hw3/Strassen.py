import numpy as np

def up_to_2pow(n):
    return 1 << (n - 1).bit_length()

def get_len():
    return input()

def print_matrix(M):
    lenM, _ = M.shape
    for i in range (0, lenM):
        print(" ".join(str(M[i])))

def get_matrix(lenM):
    lenBM = up_to_2pow(lenM)
    M = np.zeros((lenBM, lenBM), dtype = np.int)
    for i in range (0, lenM):
        S = input().split()
        M[i] = [int(s) for s in S]
    return M

def part_matrix(M):
    V1, V2 = np.vsplit(M, 2)
    M11, M21 = np.hsplit(V1, 2)
    M12, M22 = np.hsplit(V2, 2)
    return M11, M12, M21, M22

def build_matrix(M11, M12, M21, M22):
    lenm, _ = M11.shape
    lenM = lenm * 2
    M = np.zeros((lenM, lenM), dtype = np.int)
    M[:lenm, :lenm] = M11
    M[:lenm, lenm:lenM] = M12
    M[lenm:lenM, :lenm] = M21
    M[lenm:lenM, lenm:lenM] = M22
    return M

def multiply_matrix(A, B):
    lenC, _ = A.shape
    C = np.zeros((lenC, lenC), dtype = np.int)
    for i in range (0, lenC):
        for j in range (0, lenC):
            for k in range (0, lenC):
                C[i, k] += A[i, j] * B[j, k]
    return C

def multiply_strassen(A, B):
    lenC, _ = A.shape
    if lenC <= 32:
        return multiply_matrix(A, B)
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
    C = multiply_strassen(A, B)
    print_matrix(C[:size, :size])

    
