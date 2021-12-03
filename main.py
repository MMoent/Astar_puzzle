import numpy as np
import time


# class that stores the puzzle array, generates the neighboring puzzle array and determines the solvability.
class Puzzle(object):
    def __init__(self, N, M, arr=None):
        if type(arr) == np.ndarray:
            self.N, self.M = arr.shape
            self.arr = arr
        else:
            self.N, self.M = N, M
            arr = np.arange(0, M * N)
            np.random.shuffle(arr)
            arr = np.reshape(arr, (N, M))
            self.arr = arr
        goal = np.arange(1, M * N)
        goal = np.append(goal, 0)
        self.goal = np.reshape(goal, (N, M))

    def __index(self):
        row_idx, col_idx = np.where(self.arr == 0)
        return row_idx[0], col_idx[0]

    def generate_neighbors(self):
        neighbors = []
        x, y = self.__index()
        if x != self.N - 1:
            arr = self.arr.copy()
            tmp = arr[x + 1, y]
            arr[x + 1, y] = 0
            arr[x, y] = tmp
            neighbors.append(arr)
        if x != 0:
            arr = self.arr.copy()
            tmp = arr[x - 1, y]
            arr[x - 1, y] = 0
            arr[x, y] = tmp
            neighbors.append(arr)
        if y != self.M - 1:
            arr = self.arr.copy()
            tmp = arr[x, y + 1]
            arr[x, y + 1] = 0
            arr[x, y] = tmp
            neighbors.append(arr)
        if y != 0:
            arr = self.arr.copy()
            tmp = arr[x, y - 1]
            arr[x, y - 1] = 0
            arr[x, y] = tmp
            neighbors.append(arr)
        return neighbors

    def show(self):
        print(f'The {self.N} * {self.M} puzzle is: \n', self.arr)
        print('The goal is: \n', self.goal)

    def manhattan(self):
        manhattan_i = []
        for i in range(self.N * self.M):
            manhattan_i.append(np.sum(np.abs(np.argwhere(self.arr == i) - np.argwhere(self.goal == i))))
        return sum(manhattan_i)

    def equal(self, puzzle):
        return (self.arr == puzzle.arr).all()

    def is_solvable(self):
        l = self.arr.flatten()
        l = np.delete(l, np.argwhere(l == 0))
        inverse_num = 0
        for i in range(len(l) - 1):
            for j in range(i + 1, len(l)):
                if l[j] < l[i]:
                    inverse_num += 1
        return inverse_num % 2 == 0


# class that store the puzzle and its parent, and the f score.
class Node(object):
    def __init__(self, cur, move, pre, f_score):
        self.cur = cur
        self.move = move
        self.pre = pre
        self.f_score = f_score


if __name__ == '__main__':
    N = int(input("Specify the number of rows: "))
    M = int(input("Specify the number of columns: "))
    test = np.array([[0, 1], [2, 3]])
    puzzle = Puzzle(N, M)
    puzzle.show()
    start = Node(puzzle, 0, None, puzzle.manhattan())

    # implemented with A* algorithm
    open_list = [start]
    close_list = []
    start_time = time.time()
    while True:
        if not open_list or not puzzle.is_solvable():
            print('unsolvable')
            break
        cur_node = open_list.pop()

        close_list.append(cur_node)

        if cur_node.cur.manhattan() == 0:
            end_time = time.time()
            steps = [cur_node.cur.arr]
            cnt = 0
            while cur_node.pre:
                cnt += 1
                steps.append(cur_node.pre.cur.arr)
                cur_node = cur_node.pre
            steps.reverse()
            print(f'Solved. {cnt} steps. {end_time-start_time:.4f}s')
            for n in steps:
                print(n)
                print('--------------------')
            break
        neighbor_arr_set = cur_node.cur.generate_neighbors()
        for neighbor_arr in neighbor_arr_set:
            # check if the node is in close list
            neighbor_puzzle = Puzzle(N, M, neighbor_arr)
            is_in_close, is_in_open = False, False
            for close_node in close_list:
                if close_node.cur.equal(neighbor_puzzle):
                    is_in_close = True
                    break
            if is_in_close:
                continue

            for open_node in open_list:
                if open_node.cur.equal(neighbor_puzzle):
                    is_in_open = True
                    break
            if not is_in_open:
                neighbor_node = Node(neighbor_puzzle, cur_node.move + 1, cur_node, neighbor_puzzle.manhattan() + cur_node.move + 1)
                open_list.append(neighbor_node)
        open_list = sorted(open_list, key=lambda y: y.f_score, reverse=True)

