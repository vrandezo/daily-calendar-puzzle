board = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun", "x",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "x",
  "1",   "2", "3", "4", "5", "6", "7",
  "8", "9", "10", "11", "12", "13", "14",
  "15", "16", "17", "18", "19", "20", "21",
  "22", "23", "24", "25", "26", "27", "28",
  "29", "30", "31", "Sun", "Mon", "Tues", "Wed",
  "x", "x", "x", "x", "Thur", "Fri", "Sat"
]

weekdays = [ "Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun" ]

months = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

pieces = [
  "xxxx"
  "    "
  "    "
  "    ",
  "xxxx"
  "x   "
  "    "
  "    ",
  "x   "
  "xxx "
  "x   "
  "    ",
  "xxx "
  "  xx"
  "    "
  "    ",
  "x   "
  "xxx "
  "  x "
  "    ",
  "xxx "
  "xx  "
  "    "
  "    ",
  "xxx "
  "x   "
  "x   "
  "    ",
  "xxx "
  "x x "
  "    "
  "    ",
  "x   "
  "xx  "
  " x  "
  "    ",
  "xxx "
  "x   "
  "    "
  "    "
]

def show(candidate):
    for x in range(len(candidate)):
        content = candidate[x]
        if content.endswith('x'):
            content = content[:-1]
        if not content.endswith('*'):
            content += " "
        print(content.rjust(6), end="")
        if not (x+1)%7: print("")

def select(field, mask):
    copy = field.copy()
    for x in range(len(field)):
        if copy[x] == mask:
            copy[x] = copy[x] + "*"
            return copy
    return copy

def select_day(field, day):
    result = select(board, weekdays[day.weekday()])
    result = select(result, str(day.day))
    result = select(result, months[day.month-1])
    return result

def place(board, piece, tag):
    def is_blocked(board, index):
        if board[index].endswith("*"): return True
        if board[index].endswith("x"): return True
        if board[index].endswith("."): return True
        return False

    def first_free_field(board):
        for i in range(len(board)):
            if is_blocked(board, i): continue
            return i
        return 99

    fff = first_free_field(board)
    x = fff % 7
    y = fff // 7

    matrix = [
      0, 1, 2, 3,
      7, 8, 9, 10,
      14, 15, 16, 17,
      21, 22, 23, 24
    ]

    adjust = 0
    for i in range(4):
        if piece[i] == "x": break
        adjust += 1
    for m in range(len(matrix)):
        matrix[m] -= adjust

    copy = board.copy()

    for p in range(len(piece)):
        if piece[p] == "x":
            # print("p", p)
            xd = (matrix[p]+adjust) % 7 - adjust
            # print("xd", xd)
            yd = (matrix[p]+adjust) // 7
            # print("yd", yd)
            if x+xd > 6: return False
            if x+xd < 0: return False
            if y+yd > 7: return False
            if is_blocked(board, fff + matrix[p]): return False
            copy[fff + matrix[p]] = str(tag) + "."

    return copy

def print_piece(piece):
    for x in range(len(piece)):
        c = piece[x]
        if c == " ": c = "."
        print(c, end="")
        if not (x+1)%4: print("")

def mirror(piece):
    result = list(16 * " ")
    for i in range(16):
        if piece[i] == "x":
            x = i % 4
            y = i // 4
            pos = y*4 + (3-x)
            result[pos] = "x"
    return "".join(result)

def turn(piece):
    result = list(16 * " ")
    for i in range(16):
        if piece[i] == "x":
            x = i % 4
            y = i // 4
            pos = x*4 + (3-y)
            result[pos] = "x"
    return "".join(result)

def turn2(piece):
    return turn(turn(piece))

def turn3(piece):
    return turn(turn(turn(piece)))

def try_next(state, used):
    print("\r" + used.ljust(12), end="")
    if (len(used) == 10):
        print("SOLVED!")
        show(state)
        exit(0)
    for q in range(10):
        if str(q) in used:
            continue
        for j in range(8):
            if j == 0: turned_piece = pieces[q]
            if j == 1: turned_piece = turn(pieces[q])
            if j == 2: turned_piece = turn2(pieces[q])
            if j == 3: turned_piece = turn3(pieces[q])
            if j == 4: turned_piece = mirror(pieces[q])
            if j == 5: turned_piece = mirror(turn(pieces[q]))
            if j == 6: turned_piece = mirror(turn2(pieces[q]))
            if j == 7: turned_piece = mirror(turn3(pieces[q]))
            new_state = place(state, turned_piece, q)
            if new_state != False:
                try_next(new_state, used + str(q))

from datetime import date
riddle = select_day(board, date.today())
show(riddle)
print("")
try_next(riddle, "")
