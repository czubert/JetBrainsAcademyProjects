import random

from hstest import *
import re


class LastPencilTest(StageTest):
    @dynamic_test()
    def CheckOutput(self):
        main = TestedProgram()
        output = main.start().lower()
        lines = output.strip().split('\n')
        if len(lines) != 1 or "how many pencils" not in output:
            raise WrongAnswer("When the game starts, it should output only one line asking the user about the amount "
                              "of pencils they would like to use with the \"How many pencils\" string")

        output2 = main.execute("1")
        output2 = output2.replace(" ", "")
        pattern = re.compile(".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)")
        if len(output2.split()) != 1:
            raise WrongAnswer("When the user replies with the amount of pencils, the game should print 1 non-empty "
                              "line asking who will be the first player.\n"
                              f"{len(output2.split())} lines were found in the output.")
        if not re.match(pattern, output2):
            raise WrongAnswer("When the user replies with the amount of pencils, the game should ask who will"
                              " be the first player ending with the \"(\"Name1\", \"Name2\")\" string.")
        return CheckResult.correct()

    data = ["a", "_", "test", "|", "|||||", " ", "-", "two", "10g", "k5", "-0.2", "0.3"]

    @dynamic_test(data=data)
    def CheckNumericAmount(self, inp):
        main = TestedProgram()
        main.start()

        output = main.execute(inp).lower()

        if ("number of pencils" not in output) or ("numeric" not in output):
            raise WrongAnswer("When the user provides the number of pencils as a non-numeric sequence, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again"
                              " with the \"The number of pencils should be numeric\" string.")
        for i in range(1, 5):
            output = main.execute(inp).lower()
            if ("number of pencils" not in output) or ("numeric" not in output):
                raise WrongAnswer("When the user provides the number of pencils as a non-numeric sequence "
                                  "after another wrong input, the game should "
                                  "inform the user that their input is incorrect and prompt the user for input again"
                                  " with the \"The number of pencils should be numeric\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckNotZeroAmount(self):
        main = TestedProgram()
        main.start()
        output = main.execute("0").lower()

        if ("number of pencils" not in output) or ("positive" not in output):
            raise WrongAnswer("When the user provides \"0\" as a number of pencils, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again"
                              " with the \"The number of pencils should be positive\" string.")
        for i in range(1, 5):
            output = main.execute("0").lower()
            if ("number of pencils" not in output) or ("positive" not in output):
                raise WrongAnswer("When the user provides \"0\" as a number of pencils "
                                  "after another wrong input, the game should "
                                  "inform the user that their input is incorrect and prompt the user for input again"
                                  " with the \"The number of pencils should be positive\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckBothAmount(self):
        main = TestedProgram()
        main.start()

        output = main.execute("0").lower()
        if ("number of pencils" not in output) or ("positive" not in output):
            raise WrongAnswer("When the user provides \"0\" as a number of pencils, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again"
                              " with the \"The number of pencils should be positive\" string.")
        output = main.execute("a").lower()
        if ("number of pencils" not in output) or ("numeric" not in output):
            raise WrongAnswer("When the user provides the number of pencils as a non-numeric sequence "
                              "after another wrong input, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again"
                              " with the \"The number of pencils should be numeric\" string.")
        output = main.execute("0").lower()
        if ("number of pencils" not in output) or ("positive" not in output):
            raise WrongAnswer("When the user provides \"0\" as a number of pencils "
                              "after another wrong input, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again"
                              " with the \"The number of pencils should be positive\" string.")
        output2 = main.execute("1")
        output2 = output2.replace(" ", "")
        pattern = re.compile(".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)")
        if not re.match(pattern, output2):
            raise WrongAnswer("When the user correctly replies with number of pencils after wrong input, the "
                              "game should ask who will"
                              " be the first player ending with the \"(\"Name\", \"Name2\")\" string")
        return CheckResult.correct()

    test_data = [
        [2, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [3, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [4, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [5, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [9, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [13, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [17, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [21, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [101, 1, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [2, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [3, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [4, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [5, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [9, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [13, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [17, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [21, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
        [101, 2, ["4", "a", "0", "-1", "_", "|", "|||||"]],
    ]

    @dynamic_test(data=test_data, repeat=10)
    def CheckGame(self, amount, first, incorrect):
        main = TestedProgram()
        main.start()

        output = main.execute(str(amount))
        output = output.replace(" ", "")

        leftName = output[output.rfind('(') + 1:output.rfind(',')]
        rightName = output[output.rfind(',') + 1:output.rfind(')')]

        prevPlayer = ""
        nextPlayer = ""
        if first == 1:
            prevPlayer = leftName
            nextPlayer = rightName
        else:
            prevPlayer = rightName
            nextPlayer = leftName

        output2 = main.execute(leftName + rightName).lower()

        if ("choose between" not in output2) or (leftName.lower() not in output2) or (rightName.lower() not in output2):
            raise WrongAnswer("When the user provides the string that is not equal to"
                              f"'{leftName}' or '{rightName}', the game should "
                              "inform the user that their input is incorrect and prompt the user for input again"
                              f" with the \"Choose between '{leftName}' and '{rightName}'\" string.")
        for i in range(1, 5):
            output2 = main.execute(leftName + rightName).lower()
            if ("choose between" not in output2) or (leftName.lower() not in output2) or (
                    rightName.lower() not in output2):
                raise WrongAnswer("When the user provides the string that is not equal to"
                                  f"'{leftName}' or '{rightName}' after another wrong input, the game should "
                                  "inform the user that their input is incorrect and prompt the user for input again"
                                  f" with the \"Choose between '{leftName}' and '{rightName}'\" string.")

        output3 = main.execute(prevPlayer).lower()
        lines = output3.strip().split('\n')
        linesNonEmpty = [s for s in lines if len(s) != 0]

        if first == 1:
            if len(linesNonEmpty) != 2:
                raise WrongAnswer("When the player provides the game correct initial conditions"
                                  f", the program should print 2 non-empty lines if {prevPlayer} was first.")
            checkPencils = [s for s in lines if '|' in s]
            if len(checkPencils) != 1:
                raise WrongAnswer("When the player provides the game correct initial conditions"
                                  ", the program should print one line that contains vertical bar symbols "
                                  f"if {prevPlayer} was first.")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The line with pencils should not contain any other symbols except for "
                                  "the '|' symbol.")
            if len(checkPencils[0]) != int(amount):
                raise WrongAnswer("The line with pencils should contain as many '|' symbols as the player provided.")
            checkTurn = any((prevPlayer.lower() in s) and ("turn" in s) for s in lines)

            if not checkTurn:
                raise WrongAnswer(f"When the player provides the game initial conditions"
                                  f" there should be a line in output that contains the \"{prevPlayer}\'s turn\""
                                  f" string if {prevPlayer} was chosen as the first player.")
        else:
            if len(linesNonEmpty) != 5:
                raise WrongAnswer("When the player provides the correct game initial conditions"
                                  f", if {prevPlayer} goes first there should be printed 5 non-empty lines "
                                  f"in such order:\n"
                                  f"2 for {prevPlayer}\n"
                                  f"1 for {prevPlayer}'s move\n"
                                  f"2 for {nextPlayer}")

            linesPrev = linesNonEmpty[:2]
            turn = linesNonEmpty[2]
            linesNext = linesNonEmpty[2:]

            checkPencils = [s for s in linesPrev if '|' in s]

            if len(checkPencils) != 1:
                raise WrongAnswer("When the player provides the correct initial game conditions"
                                  ", the program should print one line for each player, that contains '|' "
                                  f"symbols if {prevPlayer} was first")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The line with pencils should not contain any other symbols except for "
                                  "the '|' symbol.")
            if len(checkPencils[0]) != amount:
                raise WrongAnswer("When the player provides the correct initial game conditions,"
                                  f"the {prevPlayer}'s line with pencils should contain as many '|' symbols "
                                  f"as the player provided.")

            checkTurn = any((prevPlayer.lower() in s) and ("turn" in s) for s in linesPrev)

            if not checkTurn:
                raise WrongAnswer(f"When the player provides the correct initial game conditions"
                                  f" there should be a line in the output for the {prevPlayer}'s turn that contains "
                                  f"\"{prevPlayer}\" and \"turn\" strings if '{prevPlayer}' was chosen as the "
                                  f"first player")

            if turn != '1' and turn != '2' and turn != '3':
                raise WrongAnswer(f"When the player provides the correct initial game conditions"
                                  f" and the first player is {prevPlayer}, there should be printed 5 non-empty lines, "
                                  f"third of them is {prevPlayer}'s turn, so it should be either '1', '2' or '3'")

            bottake = (amount - 1) % 4

            if bottake != 0 and int(turn) != bottake:
                raise WrongAnswer(f"{prevPlayer}'s move doesn't follow a winning strategy. Example:\n"
                                  f"If there are {amount} pencils left and it's {prevPlayer}'s turn, he takes {turn} "
                                  f"pencils instead of {bottake}")

            checkPencils = [s for s in linesNext if '|' in s]

            if len(checkPencils) != 1:
                raise WrongAnswer("When the player provided the game correct initial conditions"
                                  ", there should be exactly one line in output for each player, that contains '|' "
                                  f"symbols if {prevPlayer} was first")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The pencils-lines should not contain any other symbols except the '|'")
            if len(checkPencils[0]) != amount-int(turn):
                raise WrongAnswer("When the player provided the game correct initial conditions,"
                                  f"the {nextPlayer}'s pencils-line should contain as much '|' symbols, as much as "
                                  f"there is left after {prevPlayer}'s turn")

            checkTurn = any((nextPlayer.lower() in s) and ("turn" in s) for s in linesNext)

            if not checkTurn:
                raise WrongAnswer(f"When the player provided the game correct initial conditions"
                                  f" there should be a line in output for {nextPlayer}'s turn containing "
                                  f"\"{nextPlayer}\" and \"turn\" substrings if '{prevPlayer}' was chosen as the "
                                  f"first player")

        onTable = amount
        if first == 2:
            onTable -= int(linesNonEmpty[2])
            prevPlayer, nextPlayer = nextPlayer, prevPlayer

        while onTable > 0:
            for j in incorrect:
                output = main.execute(j).lower()
                if ("possible values" not in output) or ('1' not in output) or ('2' not in output) or (
                        '3' not in output):
                    raise WrongAnswer(f"If the player enters a string of how many pencils he took, that is not"
                                      f" '1', '2' or '3' - the game should "
                                      "inform user that his input is incorrect and re-query the input"
                                      f" with \"Possible values: '1', '2', '3'\" substring")
            i = random.randint(1, 3)
            output = main.execute(str(i)).lower()
            if i >= onTable:
                if onTable != i:
                    if ("too many" not in output) or ('pencils' not in output):
                        raise WrongAnswer(
                            "If the player enters number of pencils that is greater than there are on the table"
                            " - the game should inform user that his input is incorrect and re-query the input"
                            " with \"too many pencils\" substring")

                    output = main.execute(str(onTable)).lower()
                lines = output.strip().split('\n')
                linesNonEmpty = [s for s in lines if len(s) != 0]

                if len(linesNonEmpty) != 1 or (nextPlayer.lower() not in linesNonEmpty[0]) or (
                        'win' not in linesNonEmpty[0] and 'won' not in linesNonEmpty[0]):
                    raise WrongAnswer(
                        "When the last pencil was taken - there should be exactly one line in output, informing "
                        "who was the winner in this game with \"*Name*\" and \"win\"/\"won\" substrings")

                if not main.is_finished():
                    raise WrongAnswer("Your program should not request anything, when there are no pencils left")

                return CheckResult.correct()

            onTable -= i
            lines = output.strip().split('\n')
            linesNonEmpty = [s for s in lines if len(s) != 0]

            if onTable == 1:
                if len(linesNonEmpty) != 4:
                    raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                      f"if {nextPlayer} left with 1 pencil, there should be printed exactly 4 "
                                      f"non-empty lines in such order:\n"
                                      f"2 for {nextPlayer}\n"
                                      f"1 for {nextPlayer}'s move\n"
                                      f"1 for game-results")
                linesPrev = linesNonEmpty[:2]
                turn = linesNonEmpty[2]
                result = linesNonEmpty[3]

                checkPencils = [s for s in linesPrev if '|' in s]

                if len(checkPencils) != 1:
                    raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                      ", there should be exactly one line in output for each player, that contains '|'")
                if len(list(set(checkPencils[0]))) != 1:
                    raise WrongAnswer("The pencils-lines should not contain any other symbols except the '|'")
                if len(checkPencils[0]) != onTable:
                    raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                      f"the pencils-line for {nextPlayer} should contain as much '|' symbols, as there "
                                      f"are pencils left")

                checkTurn = any((nextPlayer.lower() in s) and ("turn" in s) for s in linesPrev)

                if not checkTurn:
                    raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                      f" there should be a line in output for {nextPlayer}'s turn containing "
                                      f"\"{nextPlayer}\" and \"turn\" substrings")
                if turn != "1":
                    raise WrongAnswer(f"If {nextPlayer} left with 1 pencil, he can't take any other amount, except 1")
                if (prevPlayer.lower() not in result) or ('win' not in result and 'won' not in result):
                    raise WrongAnswer(
                        "When the last pencil was taken - there should be exactly one line in output, informing "
                        "who was the winner in this game with \"*Name*\" and \"win\" substrings")

                if not main.is_finished():
                    raise WrongAnswer("Your program should not request anything, when there are no pencils left")

                return CheckResult.correct()


            if len(linesNonEmpty) != 5:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  ", there should be printed exactly 5 non-empty lines "
                                  f"in such order:\n"
                                  f"2 for {nextPlayer}\n"
                                  f"1 for {nextPlayer}'s move\n"
                                  f"2 for {prevPlayer}")
            linesPrev = linesNonEmpty[:2]
            turn = linesNonEmpty[2]
            linesNext = linesNonEmpty[2:]

            checkPencils = [s for s in linesPrev if '|' in s]

            if len(checkPencils) != 1:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  ", there should be exactly one line in output for each player, that contains '|'")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The pencils-lines should not contain any other symbols except the '|'")
            if len(checkPencils[0]) != onTable:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  f"the pencils-line for {nextPlayer} should contain as much '|' symbols, as there "
                                  f"are pencils left")

            checkTurn = any((nextPlayer.lower() in s) and ("turn" in s) for s in linesPrev)

            if not checkTurn:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  f" there should be a line in output for {nextPlayer}'s turn containing "
                                  f"\"{nextPlayer}\" and \"turn\" substrings")

            if turn != '1' and turn != '2' and turn != '3':
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  f"- there should be printed 5 non-empty lines, third of them is {prevPlayer}'s turn, "
                                  "so it should be either '1', '2' or '3'")

            bottake = (onTable - 1) % 4
            if bottake != 0 and int(turn) != bottake:
                raise WrongAnswer(f"{nextPlayer}'s move doesn't follow a winning strategy. Example:\n"
                                  f"If there are {onTable} pencils left and it's {nextPlayer}'s turn, he takes {turn} "
                                  f"pencils instead of {bottake}")
            onTable -= int(turn)

            checkPencils = [s for s in linesNext if '|' in s]

            if len(checkPencils) != 1:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  ", there should be exactly one line in output for each player, that contains '|'")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The pencils-lines should not contain any other symbols except the '|'")
            if len(checkPencils[0]) != onTable:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  f"the pencils-line for {prevPlayer} should contain as much '|' symbols, as there "
                                  f"are pencils left")

            checkTurn = any((prevPlayer.lower() in s) and ("turn" in s) for s in linesNext)

            if not checkTurn:
                raise WrongAnswer(f"After inputting number of pencils, that {prevPlayer} has taken"
                                  f" there should be a line in output for {prevPlayer}'s turn containing "
                                  f"\"{prevPlayer}\" and \"turn\" substrings")


if __name__ == '__main__':
    LastPencilTest().run_tests()
