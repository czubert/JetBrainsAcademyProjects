from pathlib import Path

import git
from git import InvalidGitRepositoryError, NoSuchPathError
from hstest import CheckResult, StageTest, dynamic_test, TestedProgram

ROOT = Path(__file__).resolve().parent.parent.parent.parent
repo_path = ROOT / 'Safety-net-study-repository'


class GitTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = None

    @dynamic_test
    def test1(self):
        """Tests if path is a valid git repository"""
        t = TestedProgram()
        try:
            self.r = git.Repo(repo_path)
        except NoSuchPathError as e:
            return CheckResult.wrong(f"The path '{repo_path}' does not exist!")
        except InvalidGitRepositoryError as e:
            return CheckResult.wrong(f"'{repo_path}' is not a valid git repository!")
        except Exception as err:
            return CheckResult.wrong(f"{err} error occurred while creating the Git instance!")

        return CheckResult.correct()

    @dynamic_test
    def test2(self):
        """Tests if all branches exist in the local repository"""
        branch_list = ['0.2.x-dev', 'main']
        branches = [str(branch) for branch in self.r.branches]
        for branch in branch_list:
            if branch not in branches:
                return CheckResult.wrong(f"{branch} is missing!")
        return CheckResult.correct()

    @dynamic_test
    def test3(self):
        """Tests active branch"""
        active_branch = '0.2.x-dev'
        try:
            is_valid_branch = self.r.active_branch.is_valid()
            current_branch_name = self.r.active_branch.name
        except TypeError:
            return CheckResult.wrong("Head might be detached!")
        except AssertionError:
            return CheckResult.wrong("Failed to read branch name!")
        except Exception as err:
            return CheckResult.wrong(f"{err} error occurred while reading branch name!")
        if not is_valid_branch:
            return CheckResult.wrong(f"Active branch is not valid!")
        if current_branch_name != active_branch:
            return CheckResult.wrong(f"Active branch is not '{active_branch}'!")

        return CheckResult.correct()


if __name__ == '__main__':
    GitTest().run_tests()
