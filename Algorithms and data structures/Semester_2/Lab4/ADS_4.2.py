matrix_list = {"A": [[2, -3, 1], [5, 4, -2]],
               "B": [[-7, 5], [2, -1], [4, 3]],
               "C": [[0, 1], [1, 0]],
               "D": [[1, 0], [0, 1]],
               "E": [[1, 0], [0, 1]],
               "F": [[1, 0], [0, 1]],
               "J": [[1, 0], [0, 1]]}

def matrix_show(mult_list):
    for i in mult_list.keys():
        print(i, "--->", mult_list[i])
    return ""

def multiplication(matrix1, matrix2):
    res = []
    height1, width1, height2, width2 = len(matrix1), len(matrix1[0]), len(matrix2), len(matrix2[0]),
    for height3 in range(height1):
        res.append([])
        for width3 in range(width2):
            sum = 0
            for elements in range(width1):
                sum += matrix1[height3][elements]*matrix2[elements][width3]
            res[height3].append(sum)
    return res

multiplication_list = {}

for i in range(len(matrix_list.keys())-1):
    matrix1, martix2 = list(matrix_list.keys())[i], list(matrix_list.keys())[i+1]
    if not(str((matrix_list[matrix1], matrix_list[martix2])) in multiplication_list.keys()):
        multiplication_list[str((matrix_list[matrix1], matrix_list[martix2]))] = multiplication(matrix_list[matrix1], matrix_list[martix2])
    matrix_list[martix2] = multiplication_list[str((matrix_list[matrix1], matrix_list[martix2]))]

print(matrix_show(multiplication_list))