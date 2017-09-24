import numpy as np

def upTo2Pow(n):
    i = 0
    while 2 ** i < int(n):
        i += 1
    return 2 ** i

def getLen():
    print("Write size of square matrix:")
    return input()

def printMatrix(M, lenM):
    for i in range (0, lenM):
        print(" ".join(str(M[i])))

def getMatrix(lenM):
    print("Write square matrix")
    M = np.ndarray(shape = (upTo2Pow(lenM), upTo2Pow(lenM)), dtype = int)
    for i in range (0, lenM):
        for j in range (0, lenM):
            M[i, j] = int(input())
    for i in range (lenM, upTo2Pow(lenM)):
        for j in range (0, upTo2Pow(lenM)):
            M[i, j] = 0
    for i in range (0, lenM):
        for j in range (lenM, upTo2Pow(lenM)):
            M[i, j] = 0
    return M

def multiplyMatrix(A, B, lenC):
    C = np.ndarray(shape = (lenC, lenC), dtype = int)
    C= nullMatrix(C, lenC)
    for i in range (0, lenC):
        for j in range (0, lenC):
            for k in range (0, lenC):
                C[i, k] += A[i, j] * B[j, k]
    return C

def nullMatrix(M, lenM):
    for i in range (0, lenM):
        for j in range (0, lenM):
            M[i, j] = 0
    return M

def partMatrix(M, lenM):
    lenm = int(lenM / 2)
    M11 = np.ndarray(shape = (lenm, lenm), dtype = int)
    for i in range (0, lenm):
        for j in range (0, lenm):
            M11[i, j] = M[i, j]
    M12 = np.ndarray(shape = (lenm, lenm), dtype = int)
    for i in range (0, lenm):
        for j in range (lenm, lenM):
            M12[i, j - lenm] = M[i, j]
    M21 = np.ndarray(shape = (lenm, lenm), dtype = int)
    for i in range (lenm, lenM):
        for j in range (0, lenm):
            M21[i - lenm, j] = M[i, j]
    M22 = np.ndarray(shape = (lenm, lenm), dtype = int)
    for i in range (lenm, lenM):
        for j in range (lenm, lenM):
            M22[i - lenm, j - lenm] = M[i, j]
    return M11, M12, M21, M22

def buildMatrix(M11, M12, M21, M22, lenM):
    lenm = int(lenM / 2)
    M = np.ndarray(shape = (lenM, lenM), dtype = int)
    for i in range (0, lenm):
        for j in range (0, lenm):
            M[i, j] = M11[i, j]
    for i in range (0, lenm):
        for j in range (lenm, lenM):
            M[i, j] = M12[i, j - lenm]
    for i in range (lenm, lenM):
        for j in range (0, lenm):
            M[i, j] = M21[i - lenm, j]
    for i in range (lenm, lenM):
        for j in range (lenm, lenM):
            M[i, j] = M22[i - lenm, j - lenm]
    return M

def multiplyStrassen(A, B, lenC):
    if lenC <= 32:
        return multiplyMatrix(A, B, lenC)
    else:
        lenc = int(lenC / 2)
        A11, A12, A21, A22 = partMatrix(A, lenC)
        B11, B12, B21, B22 = partMatrix(B, lenC)
        P1 = multiplyStrassen(A11 + A22, B11 + B12, lenc)
        P2 = multiplyStrassen(A21 + A22, B11, lenc)
        P3 = multiplyStrassen(A11, B12 - B22, lenc)
        P4 = multiplyStrassen(A22, B21 - B11, lenc)
        P5 = multiplyStrassen(A11 + A12, B22, lenc)
        P6 = multiplyStrassen(A21 - A11, B11 + B12, lenc)
        P7 = multiplyStrassen(A12 - A22, B21 + B22, lenc)
        C11 = P1 + P4 - P5 + P7
        C12 = P3 + P5
        C21 = P2 + P4
        C22 = P1 - P2 + P3 + P6
        return buildMatrix(C11, C12, C21, C22, lenC)

if __name__ == "__main__":
    print("Matrix A")
    lenA = int(getLen())
    A = getMatrix(lenA)
    lenA = upTo2Pow(lenA)
    print("Matrix B")
    B = getMatrix(lenA)
    print("Multiply result:")
    printMatrix(multiplyStrassen(A, B, lenA), lenA)

    
