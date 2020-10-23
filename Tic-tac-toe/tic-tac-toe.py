from typing import Optional, List, Tuple

type_playground = List[List[str]]
triple_bool = Tuple[bool, bool, bool]


def new_playground(height: int, width: int) -> type_playground:
    playground = []
    for _ in range(height):
        row = [" " for _ in range(width)]
        playground.append(row)
    return playground


def get(playground: type_playground, row: int, col: int) -> str:
    return playground[row][col]


def put(playground: type_playground, row: int, col: int, symbol: str) -> bool:
    if playground[row][col] == " ":
        playground[row][col] = symbol
        return True
    return False


def print_separation_line(width: int) -> None:
    length_row = width + 2 + width * 3
    for _ in range(3):
        print(" ", end="")
    for i in range(length_row - 1):
        if i % 4 == 0:
            print("+", end="")
        else:
            print("-", end="")


def print_playground_line(playground: type_playground,
                          width: int, playground_row: int) -> None:
    col = -1
    print(" {0:^{1}}".format(chr(ord('A') + playground_row), 2), end="")

    for i in range(width):
        print("|", end="")
        col += 1
        print("{0:^{1}}".format(playground[playground_row][col], 3), end="")
    print("|", end="")


def print_header(width: int) -> None:
    for _ in range(4):
        print(" ", end="")

    for i in range(width):
        if i < 10:
            print("{0:^{1}}".format(i, 3), end=" ")
        else:
            print("{0:>{1}}".format(i, 3), end=" ")


def draw(playground: type_playground) -> None:
    height = len(playground)
    width = len(playground[0])
    playground_row = -1
    print_header(width)
    print()

    for i in range(2 * height + 1):
        if i % 2 == 0:
            playground_row += 1
            print_separation_line(width)
            print()
        else:
            print_playground_line(playground, width, playground_row)
            print()


def solve_current(x_won: bool, o_won: bool) -> Optional[str]:
    if o_won and x_won:
        return "invalid"
    if o_won:
        return "O"
    if x_won:
        return "X"
    return None


def find_substring(string: str, symbol: str) -> bool:
    count = 0
    # if string is shorter than 5, no one can win
    if len(string) < 5:
        return False
    for char in string:
        if char == symbol:
            count += 1
        elif count == 5:
            break
        else:
            count = 0
    if count == 5:
        return True
    return False


def check_line(line: List[str]) -> Optional[str]:
    line_string = ""
    x_won = False
    o_won = False
    for element in line:
        line_string += element
    if find_substring(line_string, "O"):
        o_won = True
    if find_substring(line_string, "X"):
        x_won = True
    return solve_current(x_won, o_won)


def check_column(playground: type_playground, column: int) -> Optional[str]:
    column_string = ""
    x_won = False
    o_won = False
    for line in range(len(playground)):
        column_string += playground[line][column]
    if find_substring(column_string, "O"):
        o_won = True
    if find_substring(column_string, "X"):
        x_won = True
    return solve_current(x_won, o_won)


def check_diagonal(playground: type_playground, column: int, line: int,
                   diagonal_start_from: str) -> Optional[str]:
    diagonal_string = ""
    x_won = False
    o_won = False
    y = line
    x = column
    if diagonal_start_from == "left":
        condition = len(playground[0])
    else:
        condition = -1
    while y != -1 and x != condition:
        diagonal_string += playground[y][x]
        y -= 1
        if diagonal_start_from == "left":
            x += 1
        else:
            x -= 1
    if find_substring(diagonal_string, "O"):
        o_won = True
    if find_substring(diagonal_string, "X"):
        x_won = True
    return solve_current(x_won, o_won)


def check_tie(playground: type_playground) -> bool:
    tie = True
    for line in playground:
        if " " in line:
            tie = False
    return tie


def check_all_diagonals(playground: type_playground) \
        -> Tuple[bool, bool, bool]:
    y = len(playground) - 1
    x = len(playground[0]) - 5
    x_won, o_won, invalid = False, False, False

    while y >= 4:
        diagonal_result_left = check_diagonal(playground, x, y, "left")
        if x == 0:
            y -= 1
        if x != 0:
            x -= 1
        if diagonal_result_left == "invalid":
            invalid = True
        if diagonal_result_left == "X":
            x_won = True
        if diagonal_result_left == "O":
            o_won = True
    y = len(playground) - 1
    x = 4

    while y >= 4:
        diagonal_result_right = check_diagonal(playground, x, y, "right")
        if x == len(playground[0]) - 1:
            y -= 1
        if x != len(playground[0]) - 1:
            x += 1
        if diagonal_result_right == "invalid":
            invalid = True
        if diagonal_result_right == "X":
            x_won = True
        if diagonal_result_right == "O":
            o_won = True
    return x_won, o_won, invalid


def who_won(playground: type_playground) -> Optional[str]:
    x_won = False
    o_won = False
    for line in playground:
        line_result = check_line(line)
        if line_result == "invalid":
            return "invalid"
        elif line_result == "X":
            x_won = True
        elif line_result == "O":
            o_won = True

    for column in range(len(playground[0])):
        column_result = check_column(playground, column)
        if column_result == "invalid":
            return "invalid"
        elif column_result == "X":
            x_won = True
        elif column_result == "O":
            o_won = True
    if len(playground) > 4 and len(playground[0]) > 4:
        all_diagonals_result = check_all_diagonals(playground)
        if all_diagonals_result[2]:
            return "invalid"
        if all_diagonals_result[0]:
            x_won = True
        if all_diagonals_result[1]:
            o_won = True

    if check_tie(playground) and not x_won and not o_won:
        return "tie"
    if x_won and o_won:
        return "invalid"
    if x_won:
        return "X"
    if o_won:
        return "O"
    return None


def check_if_can_win(line_result: Optional[str], column_result: Optional[str],
                     diag_result: triple_bool, symbol: str) -> bool:
    if line_result == symbol:
        return True
    if column_result == symbol:
        return True
    if diag_result[0] and symbol == "X":
        return True
    if diag_result[1] and symbol == "O":
        return True
    return False


def hint(playground: type_playground, symbol: str) \
        -> Optional[Tuple[int, int]]:
    diag_result = (False, False, False)
    copied_playground = [x[:] for x in playground]
    for line in playground:
        for column in range(len(line)):
            if line[column] == " ":
                line_index = playground.index(line)
                put(copied_playground, line_index, column, symbol)
                line_result = check_line(copied_playground[line_index])
                column_result = \
                    check_column(copied_playground, column)
                if len(playground) > 4 and len(playground[0]) > 4:
                    diag_result = check_all_diagonals(copied_playground)
                copied_playground[line_index][column] = " "
                if check_if_can_win(line_result, column_result,
                                    diag_result, symbol):
                    return line_index, column
    return None


def player_input(symbol: str, height: int, width: int) -> Tuple[int, int]:
    line = ""
    column = ""
    valid_line = False
    valid_column = False
    while not valid_line or not valid_column:
        if not valid_line:
            line = input("Choose the line in interval A - {0} "
                         "where to put {1}: "
                         .format(chr(height + ord('A') - 1), symbol))
        if not valid_column:
            column = input("Choose the column in interval "
                           "0 - {0} where to put {1}: "
                           .format(width - 1, symbol))
        valid_line = True
        valid_column = True
        if not column.isdigit():
            print("Value of column must be natural number")
            valid_column = False
            continue
        if len(line) > 1:
            print("Line must be char in interval")
            valid_line = False
            continue
        if line > chr(height + ord('A') - 1) or 'A' > line:
            print(" Line  must be symbol in interval A - {}"
                  .format(chr(height + ord('A') - 1)))
            valid_line = False
            continue
        if int(column) > width - 1:
            print("Column must be in interval 0 - {}".format(width - 1))
            valid_column = False
            continue
    return ord(line) - ord('A'), int(column)


def player_turn(playground: type_playground, height: int,
                width: int, symbol: str) -> None:
    player_hint = hint(playground, symbol)
    valid = False
    while not valid:
        if player_hint is not None:
            print("Player ", symbol,
                  " can win in next turn. Line: {0} | Column: {1}"
                  .format(chr(player_hint[0] + ord('A')), player_hint[1]))
        co_ordinates = player_input(symbol, height, width)
        y, x = co_ordinates[0], co_ordinates[1]
        if put(playground, y, x, symbol):
            put(playground, y, x, symbol)
            valid = True
        else:
            print("This position is already filled")


def game(height: int, width: int) -> None:
    print("Five in a row rules: Players are putting symbols into playground. "
          "Player win when he has 5 same symbols in line, column or diagonal.")
    print("Each player is choosing where to put his symbol into playground "
          "by choosing symbol of line and then number of column")
    playground = new_playground(height, width)
    draw(playground)
    rounds = 0

    while who_won(playground) is None:
        if rounds % 2 == 0:
            player_turn(playground, height, width, "X")
            draw(playground)
            rounds += 1
            continue
        else:
            player_turn(playground, height, width, "O")
            draw(playground)
            rounds += 1
            continue
    win = who_won(playground)
    if win == "tie":
        print("The game ends with tie")
    elif win == "X":
        print("Player X wins")
    elif win == "O":
        print("Player O wins")
    else:
        print("Invalid end of the game")
