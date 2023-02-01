from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

PATH = "test/corpus.txt"

def preprocess():
    with open(PATH, "r", encoding="utf-8") as f:
        return f.read().split()


class TextGeneratorTests(StageTest):
    def generate(self):
        return [
            TestCase(stdin=PATH, time_limit=30000),
            TestCase(stdin=PATH, time_limit=30000),
            TestCase(stdin=PATH, time_limit=30000)
        ]

    def check(self, reply, attach):
        try:
            corpus = preprocess()
        except FileNotFoundError:
            return CheckResult.wrong("File not found at {}. Make sure the file "
                                     "has not been deleted or moved.".format(PATH))

        sentences = [sentence for sentence in reply.split('\n') if len(sentence)]

        if len(sentences) != 10:
            return CheckResult.wrong("You should output exactly 10 sentences! "
                                     "Every sentence should be in a new line.")

        for sent in sentences:
            if len(sent.split()) != 10:
                return CheckResult.wrong(
                    "Every sentence should contain exactly 10 tokens!")
            if len(set(sent.split())) == 1:
                return CheckResult.wrong(
                    "Invalid output. All words of a sentence are identical.")
            for token in sent.split():
                if token not in corpus:
                    return CheckResult.wrong("Sentences should contain "
                                             "only words from the corpus!")

        return CheckResult.correct()


if __name__ == '__main__':
    TextGeneratorTests().run_tests()
