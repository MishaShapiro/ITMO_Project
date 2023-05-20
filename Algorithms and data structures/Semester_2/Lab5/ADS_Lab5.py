import time

# Cross - Zero
def win_finder(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return "{0} - winner".format(board[i][0])
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return "{0} - winner".format(board[0][i])
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return "{0} - winner".format(board[0][0])
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != "":
        return "{0} - winner".format(board[1][1])
    return "No winner"

# sorted matrix element finder
def binar_matrix(matrix, num):
    for i in range(len(matrix)):
        border_left, border_right = 0, len(matrix[0]) - 1
        if matrix[i][0] <= num and matrix[i][-1] >= num:
            while border_left <= border_right:
                midle = (border_right + border_left) // 2
                if matrix[i][midle] == num:
                    return (i, midle)
                elif matrix[i][midle] > num:
                    border_right = midle - 1
                else:
                    border_left = midle + 1

    return None

def Ferz(n):
    def print_board(board, n):
        for i in range(n):
            for j in range(n):
                print(board[i][j], end=" ")
            print()

    def add_sol(board, ans, n):
        temp = []
        for i in range(n):
            string = ""
            for j in range(n):
                string += board[i][j]
            temp.append(string)
        ans.append(temp)

    def is_safe(row, col, board, n):
        x = row
        y = col

        while (x >= 0):
            if board[x][y] == "Q":
                return False
            else:
                x -= 1

        x = row
        y = col
        while (y < n and x >= 0):
            if board[x][y] == "Q":
                return False
            else:
                y += 1
                x -= 1

        x = row
        y = col
        while (y >= 0 and x >= 0):
            if board[x][y] == "Q":
                return False
            else:
                x -= 1
                y -= 1
        return True

    def solveNQueens(row, ans, board, n):
        if row == n:
            add_sol(board, ans, n)
            return

        for col in range(n):
            if is_safe(row, col, board, n):
                board[row][col] = "Q"
                solveNQueens(row + 1, ans, board, n)
                board[row][col] = "."

    if __name__ == "__main__":
        board = [["." for i in range(n)] for j in range(n)]
        ans = []
        solveNQueens(0, ans, board, n)

        if ans == []:
            print("Solution does not exist")
        else:
            print(len(ans))
            print(f"Out Of {len(ans)} solutions one is following")
            for i in range(len(ans)):
                print_board(ans[i], n)
                print("---------------")


# stairs step finder
def stairs_step_finder(x):
    if x < 1:
        return 0
    if x == 1:
        return 1
    else:
        return stairs_step_finder(x-1) + stairs_step_finder(x-2) + stairs_step_finder(x-3)

def stairs_step_finder_quick(x):
    mass = [0, 1]
    if x == 0:
        return 0
    for i in range(1, x):
        res = mass[-1]
        if len(mass) > 2:
            res += mass[-2]
        if len(mass) > 3:
            res += mass[-3]
        mass.append(res)
    return mass[-1]

# Three stack

class Three_stack():

    def __init__(self):
        self.multi_stack = ["|", "|"]
        self.first_start = 0
        self.second_start = 1
        self.third_start = 2

    def Add_Element(self, stack_number=1, value=0):
        if stack_number == 1:
            start = self.first_start
            self.first_start += 1
            self.second_start += 1
            self.third_start += 1
        elif stack_number == 2:
            start = self.second_start
            self.second_start += 1
            self.third_start += 1
        else:
            start = self.third_start
            self.third_start += 1
        self.multi_stack.insert(start, value)


    def Get_and_Remove_Element(self, stack_number=1):
        if stack_number == 1:
            start = self.first_start
            self.first_start -= 1
            self.second_start -= 1
            self.third_start -= 1
        elif stack_number == 2:
            start = self.second_start
            self.second_start -= 1
            self.third_start -= 1
        else:
            start = self.third_start
            self.third_start -= 1
        value = self.multi_stack[start-1]
        self.multi_stack.pop(start-1)
        return value

    def Get_All_Stack(self):
        return self.multi_stack

def example_stack():
    a = Three_stack()
    a.Add_Element(1, 1)
    a.Add_Element(1, 2)
    a.Add_Element(1, 3)
    a.Add_Element(2, "1")
    a.Add_Element(3, True)
    print(a.Get_All_Stack())
    print(a.Get_and_Remove_Element(1))
    print(a.Get_All_Stack())
    a.Add_Element(1, 2)
    print(a.Get_and_Remove_Element(2))
    print(a.Get_All_Stack())

# find miss number
def find_miss_number(mass):
    for i in range(min(mass), max(mass)):
        if i not in mass:
            return i

def expon_filter(mass):
    k = [i for i in range(1, len(mass))]
    summ = sum(k)
    for i in range(len(k)):
        k[i] = k[i]/summ
        mass[i] += (mass[i+1] - mass[i])*k[i]
    return mass

# board for first task
board = [["x", "x", "o"],
         ["", "x", "o"],
         ["", "", "o"]]

# matrix for second task
matrix = [[0, 1, 2, 3, 4],
          [1, 1, 2, 3, 4],
          [1, 2, 2, 3, 4],
          [2, 2, 3, 4, 5],
          [3, 3, 4, 5, 6],
          [3, 4, 5, 6, 7]]


# First_Task
print(win_finder(board))

# Second_Task
print(binar_matrix(matrix, 5))

# Third_Task
Ferz(8)

# Fourth_Task
Now_time = time.time()
print(stairs_step_finder(26))
print("Время выполнения используя рекурсивный метод", time.time() - Now_time)
Now_time = time.time()
print(stairs_step_finder_quick(26))
print("Время выполнения используя динамическое программирование, изменяя массив", time.time() - Now_time)

# Fith_Task
example_stack()

# Sixth_Task
print(expon_filter([3, 4, 5, 10, 4, 7, 8, 9, 1, 6, 7]))

# Seventh_Task
print(find_miss_number([3, 4, 5, 7, 8, 9]))
