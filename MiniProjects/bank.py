from datetime import datetime, date
from typing import Dict, Tuple, Set, List


# ========================================
# Task 1: Bank (4 points)
# ========================================

def load_file(file_name: str) -> str:
    with open(file_name, 'r') as my_file:
        return my_file.read()


commands_list = ["ADD", "CREATE", "SUB", "FILTER_OUT",
                 "AGGREGATE", "GOOD_DEED", "PRINT"]


def is_empty(accounts):
    return accounts == {}


def create(account_name, deposit, accounts):
    if account_name in accounts or deposit < 0:
        return False
    accounts[account_name] = deposit
    return True


def add(account_name, amount, accounts):
    if account_name not in accounts or amount < 0:
        return False
    accounts[account_name] += amount
    return True


def sub(account_name, amount, accounts):
    if account_name not in accounts or amount < 0:
        return False
    accounts[account_name] -= amount
    return True


def filter_out(count, method, accounts):
    if count < 0:
        return False
    if method != "MAX" and method != "MIN":
        return False
    if is_empty(accounts):
        return True
    if count > len(accounts):
        accounts.clear()
        return True
    if method == "MAX":
        sorted_accounts = sorted(accounts.items(), key=lambda x: (-x[1], x[0]))
    else:
        sorted_accounts = sorted(accounts.items(), key=lambda x: (x[1], x[0]))

    for i in range(count):
        del accounts[sorted_accounts[i][0]]
    return True


def aggregate(account_1, account_2, accounts):
    if account_1 not in accounts or account_2 not in accounts:
        return False
    accounts[account_1] += accounts[account_2]
    del accounts[account_2]
    return True


def find_the_richest(accounts):
    richest = sorted(accounts.items(), key=lambda x: (-x[1], x[0]))
    return richest[0][0]


def good_deed(amount, count, accounts):
    n = 0
    if amount < 0 or count < 0:
        return False
    if is_empty(accounts):
        return True
    sorted_accounts = sorted(accounts.items(), key=lambda x: (x[1], x[0]))
    richest = find_the_richest(accounts)
    if accounts[richest] < amount:
        return True
    while n != count and accounts[richest] - amount >= 0 \
            and n < len(accounts) - 1:
        accounts[richest] -= amount
        accounts[sorted_accounts[n][0]] += amount
        n += 1

    return True


def print_acc(accounts):
    acc = sorted(accounts.items(), key=lambda x: (-x[1], x[0]))
    for each_acc in acc:
        print("{}: {}".format(each_acc[0], each_acc[1]))


def wrong_parameters(instruction, line_number):
    print("Instruction \"{}\" called with an invalid argument on line {}."
          .format(instruction, line_number))


def instructions(line_parsed, line_number, accounts):
    command = line_parsed[0]
    if command not in commands_list:
        print("Invalid instruction \"{}\" on line {}."
              .format(command, line_number))
        return False
    if command != "PRINT" and len(line_parsed) != 3:
        print("Invalid number of arguments on line {}."
              .format(line_number))
        return False
    if command == "CREATE":
        if create(line_parsed[1], int(line_parsed[2]), accounts):
            return True
        wrong_parameters("CREATE", line_number)
        return False
    if command == "ADD":
        if add(line_parsed[1], int(line_parsed[2]), accounts):
            return True
        wrong_parameters("ADD", line_number)
        return False
    if command == "SUB":
        if sub(line_parsed[1], int(line_parsed[2]), accounts):
            return True
        wrong_parameters("SUB", line_number)
        return False
    if command == "FILTER_OUT":
        if filter_out(int(line_parsed[1]), line_parsed[2], accounts):
            return True
        wrong_parameters("FILTER_OUT", line_number)
        return False
    if command == "AGGREGATE":
        if aggregate(line_parsed[1], line_parsed[2], accounts):
            return True
        wrong_parameters("AGGREGATE", line_number)
        return False
    elif command == "GOOD_DEED":
        if good_deed(int(line_parsed[1]), int(line_parsed[2]), accounts):
            return True
        wrong_parameters("GOOD_DEED", line_number)
        return False
    elif command == "PRINT":
        print_acc(accounts)
        return True


def interpret_file(file_name: str, accounts: Dict[str, int]) -> None:
    file = load_file(file_name)
    parsed_file = file.split("\n")
    line_number = 1
    for line in parsed_file:
        line_parsed = line.split()
        if line_parsed != [] and \
                not instructions(line_parsed, line_number, accounts):
            return
        line_number += 1

# ========================================
# Task 2: Chat (4 points)
# ========================================


Message = Tuple[datetime, str, str]


def to_datetime(value: str) -> datetime:
    return datetime.utcfromtimestamp(int(value))


def parse_message(line: str) -> Message:
    message = line.split(",")
    return to_datetime(message[0]), message[1], message[2]


def longest_messages(chat: List[Message], count: int) -> List[Message]:
    sorted_messages = sorted(chat, key=lambda x: (-len(x[2])))
    if count > len(chat):
        return sorted_messages
    return sorted_messages[:count]


def messages_at(chat: List[Message], day: date) -> List[Message]:
    date_messages = []
    for message in chat:
        if day == message[0].date():
            date_messages.append(message)
    return date_messages


def senders(chat: List[Message]) -> Set[str]:
    senders_set = []
    for message in chat:
        senders_set.append(message[1])
    return set(senders_set)


def create_name_dictionary(chat):
    senders_dict = {}
    for message in chat:
        if message[1] not in senders_dict:
            senders_dict[message[1]] = 0
    return senders_dict


def message_counts(chat: List[Message]) -> Dict[str, int]:
    senders_data = create_name_dictionary(chat)
    for message in chat:
        senders_data[message[1]] += 1
    return senders_data


def mentions(chat: List[Message], user: str) -> List[str]:
    list_users = []
    nick = "@" + user
    for message in chat:
        if nick in message[2]:
            list_users.append(message[2])
    return list_users


# ========================================
# Task 3: Longest Word (2 points)
# ========================================


def replace_with_whitespace(text):
    non_alpha = "!\"#$%&'()*+,-./:;<=>?@[]{}^_`|~\\"
    for char in non_alpha:
        text = text.replace(char, " ")
    return text


def check_letters(word, provided_letters, case_insensitive):
    for char in word:
        if case_insensitive:
            if char.lower() not in provided_letters \
                    and char.upper() not in provided_letters:
                return False
        elif char not in provided_letters:
            return False
    return True


def longest_word(text: str, provided_letters: Set[str],
                 case_insensitive: bool = False) -> str:
    word = ""
    max_word = ""
    for char in text:
        if char.isalnum():
            word += char
        else:
            if check_letters(word, provided_letters, case_insensitive) \
                    and len(word) > len(max_word):
                max_word = word
            word = ""
    # checking last word in text
    if len(word) > len(max_word) \
            and check_letters(word, provided_letters, case_insensitive):
        max_word = word
    return max_word


# ========================================
# Task 4: Parentheses Check (2 points)
# ========================================


def top(stack):
    return stack[-1]


def parentheses_check(text: str, output: bool = False) -> bool:
    opening = ["(", "[", "{"]
    closing = [")", "]", "}"]
    stack = []
    for i in range(len(text)):
        if text[i] in opening:
            stack.append((text[i], i))
        elif text[i] in closing:
            if len(stack) == 0:
                if output:
                    print("\'{}\' at position {} does not have an opening"
                          " paired bracket".format(text[i], i))
                return False
            if (len(stack) > 0) and \
                    (opening[closing.index(text[i])] == top(stack)[0]):
                stack.pop()
            else:
                if output:
                    print("\'{}\' at position {} does not match "
                          "\'{}\' at position {}"
                          .format(top(stack)[0], top(stack)[1], text[i], i))
                return False
    if len(stack) > 0:
        if output:
            print("\'{}\' at position {} does not have a closing "
                  "paired bracket".format(stack[0][0], stack[0][1]))
        return False
    return True
