import tkinter as tk
import random
import copy
import search

from tkinter.ttk import Combobox
from time import sleep
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
from queue import PriorityQueue
from queue import Queue

def getInvCount(arr):
    arr1 = []
    for y in arr:
        for x in y:
            arr1.append(x)
    arr = arr1
    inv_count = 0
    for i in range(M * N - 1):
        for j in range(i + 1, M * N):
            # count pairs(arr[i], arr[j]) such that
            # i < j and arr[i] > arr[j]
            if (arr[j] and arr[i] and arr[i] > arr[j]):
                inv_count += 1

    return inv_count

# find Position of blank from bottom
def findXPosition(puzzle):
    # start from bottom-right corner of matrix
    for i in range(N - 1,-1,-1):
        for j in range(N - 1,-1,-1):
            if (puzzle[i][j] == 0):
                return N - i

def isSolvable(puzzle):
    # Count inversions in given puzzle
    invCount = getInvCount(puzzle)
    # If grid is odd, return true if inversion
    # count is even.
    if (N & 1):
        if invCount & 1 == 0:
            return True
    else:  # grid is even
        pos = findXPosition(puzzle)
        if (pos & 1):
            if invCount & 1 == 0:
                return True
        else:
            if invCount & 1:
                return True
    return False

def createBoard(N, M):
    board = list(range(1, M*N))
    board.append(0)
    random.shuffle(board)
    puzzle = [board[i:i+N] for i in range(0, M*N, N)]
    print(puzzle)
    if N==M:
        while isSolvable(puzzle) == False:
            i = random.randint(0, M-1)
            j = random.randint(0, N-1)
            print(i, j)
            if puzzle[i][j] != 0 and puzzle[j][i] != 0:
                puzzle[i][j], puzzle[j][i] = puzzle[j][i], puzzle[i][j]
            if isSolvable(puzzle) == False:
                puzzle[i][j], puzzle[j][i] = puzzle[j][i], puzzle[i][j]
        print(isSolvable(puzzle))
    return puzzle

def drawBoard():
    bgcolor = "#ffffff"
    for i in range(M):
        for j in range(N):
            value = str(board[i][j])
            if board[i][j] == 0:
                # Tạo một ô màu khác cho số 0
                value = ""
                bgcolor = "#00b894"
            else:
                bgcolor = "#ff7675"
            label = tk.Label(frame_left, text=value, width=8, height=4,
                         borderwidth=1, relief="solid", font=("Courier New", 23, "bold"), bg=bgcolor,fg="white")
            label.grid(row=i, column=j, sticky="nsew")
            tiles[i][j] = label

def clearTiles():
    count = 0
    for row in tiles:
        for label in row:
            label.destroy()

def newGame():
    global N, M, board, tiles, step_label, step, posX, posY, old_board, goal_state, state_count_label
    step = 0
    state_count = 0
    step_label.config(text=f"Số bước: 0")
    state_count_label.config(text=f"Số trạng thái: 0")
    if win_label:
        win_label.destroy()
    N = int(entry.get())
    M = int(entry_M.get())
    clearTiles()
    tiles = [[None for _ in range(N)] for _ in range(M)]
    board = createBoard(N, M)
    drawBoard()
    old_board = copy.deepcopy(board)
    posX, posY = findZeroPos(board)
    print("New Game: ", posX, posY)
    win_state = list(range(1, M * N))
    win_state.append(0)
    goal_state = tuple(win_state)

def check_win():
    # Trạng thái kết thúc là bảng đã sắp xếp theo thứ tự từ 1 đến N*N-1, kèm số 0 ở cuối
    win_state = list(range(1, M*N))
    win_state.append(0)
    return board == [win_state[i:i+N] for i in range(0, M*N, N)]

def swapLabel(row, col, new_row, new_col):
    board[new_row][new_col], board[row][col] = board[row][col], board[new_row][new_col]
    tiles[row][col]["text"] = str(board[row][col])
    tiles[row][col]["bg"] = "#ff7675"
    tiles[new_row][new_col]["text"] = ""
    tiles[new_row][new_col]["bg"] = "#00b894"

def move_tile(row, col, key):
    global step, step_label, posX, posY
    step = step + 1
    step_label.config(text=f"Số bước: {step}")
    new_row, new_col = None, None
    if row > 0 and key == 1:
        new_row, new_col = row - 1, col
        posX, posY = row - 1, col
    elif row < M - 1 and key == 2:
        new_row, new_col = row + 1, col
        posX, posY = row + 1, col
    elif col > 0 and key == 3:
        new_row, new_col = row, col - 1
        posX, posY = row, col-1
    elif col < N - 1 and key == 4:
        new_row, new_col = row, col + 1
        posX, posY = row, col + 1

    if new_row is not None and new_col is not None:
        swapLabel(row, col, new_row, new_col)
        root.update()
        if check_win():
            print("Win")
            global win_label
            win_label = tk.Label(frame_left, text="You win!", font=("Comic Sans MS", 20, "bold"))
            win_label.grid(row=M+4, columnspan=N)

def on_key_press(event):
    row, col = None, None
    row, col = posX, posY
    if event.keysym == "Up" and row > 0:
        move_tile(row, col, 1)
    elif event.keysym == "Down" and row < M - 1:
        move_tile(row, col, 2)
    elif event.keysym == "Left" and col > 0:
        move_tile(row, col, 3)
    elif event.keysym == "Right" and col < N - 1:
        move_tile(row, col, 4)

def findZeroPos(puzzles):
    for i in range(M):
        for j in range(N):
            if puzzles[i][j] == 0:
                row, col = i, j
                break
    return row, col

def createGUI():
    global N, M, tiles, board, entry, entry_M, frame_left, frame_right, step_label, posX, posY, \
        root, old_board, goal_state, state_count_label
    tiles = [[None for _ in range(N)] for _ in range(M)]
    # board = createBoard(N, M)
    #old_board = board
    board = [[1,4,0],[3,6,2],[5,8,7]]
    #board = [[0,7], [5,3], [4,6], [2,1]]
    # win_state = list(range(1, M * N))
    # win_state.append(0)
    # goal_state = tuple(win_state)
    goal_state = tuple([0,1,2,3,4,5,6,7,8])
    old_board = copy.deepcopy(board)
    root = tk.Tk()
    root.title("N-Puzzle Game")
    # Tạo một khung chứa bảng N-Puzzle và đặt nó bên trái
    frame_left = tk.Frame(root)
    frame_left.pack(side="left")

    # Tạo một khung chứa nút và chức năng và đặt nó bên phải
    frame_right = tk.Frame(root)
    frame_right.pack(side="right")
    drawBoard()
    posX, posY = findZeroPos(board)
    # Hiện số bước đi:
    step_label = tk.Label(frame_left, text=f"Số bước: {step}", font=("Comic Sans MS", 20))
    step_label.grid(row=M+1, columnspan=N+1)
    # Thêm các nút và chức năng vào khung bên phải
    entry_label = tk.Label(frame_right, text="Nhập N (M*N puzzles):", font=("Comic Sans MS", 20))
    entry_label.pack()
    entry = tk.Entry(frame_right, font=("Comic Sans MS", 20))
    entry.pack()
    entry_label = tk.Label(frame_right, text="Nhập M (M*N puzzles):", font=("Comic Sans MS", 20))
    entry_label.pack()
    entry_M = tk.Entry(frame_right, font=("Comic Sans MS", 20))
    entry_M.pack()
    # Nút upload ảnh
    # open_button = tk.Button(frame_right, text="Ảnh", command=open_file, font=("Comic Sans MS", 20),
    #                         bg="#badc58")
    # open_button.pack()
    # New Game
    new_game_button = tk.Button(frame_right, text="New Game", command=newGame, font=("Comic Sans MS", 20),
                                bg="#badc58")
    new_game_button.pack()

    refresh_button = tk.Button(frame_right, text="refresh", command=refresh, font=("Comic Sans MS", 20),
                                bg="#badc58")
    refresh_button.pack()

    algoSelect_label = tk.Label(frame_right, text="Chọn thuật toán:", font=("Comic Sans MS", 20))
    algoSelect_label.pack()
    combo = Combobox(frame_right, width=15)
    combo['font'] = ("Comic Sans MS", 20)
    combo['values'] = ('Solve BFS', 'Solve DFS', 'Solve ID', "Solve A*", "Solve UCS", "Solve Greedy",
                       "Solve Hill Climbing")
    combo.pack()
    def solve():
        algo = combo.get()
        match algo:
            case 'Solve BFS':
                BFS()
            case 'Solve DFS':
                DFS()
            case 'Solve ID':
                IterativeDeepening()
            case 'Solve A*':
                AStar()
            case 'Solve UCS':
                UCS()
            case 'Solve Greedy':
                Greedy()
            case 'Solve Hill Climbing':
                Hill_Climbing()

    solve_button = tk.Button(frame_right, text="Solve", command=solve, font=("Comic Sans MS", 20),
                               bg="#badc58")
    solve_button.pack()

    state_count_label = tk.Label(frame_right, text=f"Số trạng thái: 0", font=("Comic Sans MS", 20))
    state_count_label.pack()

    root.bind("<KeyPress>", on_key_press)
    root.focus_set()

    root.mainloop()

def convert_to_1D(array2D, row, col):
    arr1D = []
    for i in range (row):
        for j in range (col):
            arr1D.append(array2D[i][j])
    return arr1D

def BFS():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    way, state_count = search.BFS(tuple(start), goal_state, M, N)
    print(way)
    print(posX, posY)
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    automatically_move(way)

def DFS():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    max_depth = 1
    deep_str = simpledialog.askstring("Nhập độ sâu", "Nhập độ sâu:")
    if deep_str:
        max_depth = int(deep_str)
    way, found, deep_count, state_count = search.DFS(tuple(start), goal_state, M, N, max_depth)
    if found:
        print("Tìm thấy lời giải")
    else:
        print("Không tìm thấy lời giải")
    print("Độ sâu đã duyệt: ", deep_count)
    print("Số đỉnh đã duyệt: ", state_count)
    print(way)
    print(posX, posY)
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    if found:
        automatically_move(way)

def IterativeDeepening():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    max_depth = 1
    deep_str = simpledialog.askstring("Nhập độ sâu tối đa", "Nhập độ sâu tối đa:")
    if deep_str:
        max_depth = int(deep_str)
    way, found, state_count = search.IDFS(tuple(start), goal_state, M, N, max_depth)
    if found:
        print("Tìm thấy lời giải")
    else:
        print("Không tìm thấy lời giải")
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    print("Số đỉnh đã duyệt: ", state_count)
    print(way)
    print(posX, posY)
    automatically_move(way)

def AStar():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    way, state_count = search.AStar(tuple(start), goal_state, M, N)
    print(way)
    print(posX, posY)
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    automatically_move(way)

def UCS():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    way, state_count = search.UCS(tuple(start), goal_state, M, N)
    print(way)
    print(posX, posY)
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    automatically_move(way)

def Greedy():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    way, state_count = search.Greedy(tuple(start), goal_state, M, N)
    print(way)
    print(posX, posY)
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    automatically_move(way)

def Hill_Climbing():
    tmp_board = copy.deepcopy(board)
    start = convert_to_1D(tmp_board, M, N)
    way, state_count = search.Hill_Climbing(tuple(start), goal_state, M, N)
    print(way)
    print(posX, posY)
    state_count_label.config(text=f"Số trạng thái: {state_count}")
    automatically_move(way)

def automatically_move(way):
    for char in way:
        if char == "l":
            #print("left", end="-")
            move_tile(posX, posY, 3)
            #sleep(0.1)
        elif char == "r":
            #print("right", end="-")
            move_tile(posX, posY , 4)
            #sleep(0.1)
        elif char == "u":
            #print("up", end="-")
            move_tile(posX, posY, 1)
            #sleep(0.1)
        elif char == "d":
            #print("down", end="-")
            move_tile(posX, posY,2 )
            #sleep(0.1)

def refresh():
    global board, old_board, posX, posY, step, step_label, win_label
    if win_label:
        win_label.destroy()
    step=0
    step_label.config(text=f"Số bước: 0")
    state_count_label.config(text=f"Số trạng thái: 0")
    board = copy.deepcopy(old_board)
    print(board)
    posX, posY = findZeroPos(board)
    clearTiles()
    drawBoard()

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        # Điều chỉnh kích thước theo ý muốn
        image = image.resize((300, 300))
        width, height = image.size
        tile_width = width // N
        tile_height = height // M

        for i in range(M):
            for j in range(N):
                left = j * tile_width
                upper = i * tile_height
                right = left + tile_width
                lower = upper + tile_height
                tile = image.crop((left, upper, right, lower))

                photo = ImageTk.PhotoImage(tile)
                label = tk.Label(root, image=photo)
                label.photo = photo
                label.grid(row=i, column=j)

def init():
    global N, M, tiles, board, entry, frame_left, win_label, step, step_label, posX, posY, state_count_label
    step = 0
    state_count = 0
    win_label = None
    N = 3
    M = 3
    createGUI()

if __name__ == "__main__":
    init()