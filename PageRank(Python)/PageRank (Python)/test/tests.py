import numpy as np

from hstest.stage_test import *

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class Stage5Test(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(

                stdin="6\nA B C D E F\n0.000 0.000 0.000 0.167 0.167 1.000\n0.000 1.000 0.000 0.167 0.167 0.000\n0.000 0.000 0.500 0.167 0.167 0.000\n0.000 0.000 0.000 0.167 0.167 0.000\n0.000 0.000 0.000 0.167 0.167 0.000\n1.000 0.000 0.500 0.167 0.167 0.000\nE",
                attach=("Doesn't return correct result on a network of 6 nodes.", "E\n" + "F\n" + "A\n" + "B\n" + "C")
            ),
            TestCase(
                stdin="6\nA B C D E F\n0.167 0.167 0.000 0.000 0.000 0.000\n0.167 0.167 0.000 0.333 0.000 0.000\n0.167 0.167 0.000 0.000 0.000 0.000\n0.167 0.167 0.000 0.333 0.000 0.000\n0.167 0.167 1.000 0.000 1.000 0.500\n0.167 0.167 0.000 0.333 0.000 0.500\nC",
                attach=("Doesn't return correct result on a network of 6 nodes.", "C\n" + "E\n" + "F\n" + "D\n" + "B")
            ),
            TestCase(
                stdin="4\nA B C D\n0.250 0.250 0.000 0.000\n0.250 0.250 0.000 1.000\n0.250 0.250 1.000 0.000\n0.250 0.250 0.000 0.000\nA",
                attach=("Doesn't return correct result on a network of 4 nodes.", "A\n" + "C\n" + "B\n" + "D")
            ),
            TestCase(
                stdin="1\nA\n1\nA",
                attach=("Doesn't return correct result on a network of 1 node.", "A")
            )
        ]

    def check(self, reply, attach) -> CheckResult:
        feedback, ans = attach
        true_res = ans.split()
        n = len(true_res)
        res = reply.split()
        if len(res) != n:
            return CheckResult.wrong("Your program should print " + str(n) + " websites names line by line.")
        for i in range(n):
            if res[i] != true_res[i]:
                return CheckResult.wrong(feedback)
        return CheckResult.correct()


if __name__ == '__main__':
    Stage5Test('pagerank.pagerank').run_tests()
