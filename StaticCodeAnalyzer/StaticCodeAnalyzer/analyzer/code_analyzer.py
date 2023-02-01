import re
import argparse
import os
import ast
from collections import defaultdict


class CodePEPAnalyzer:

    def __init__(self, dir_file):
        self.ast_analyzer = None
        self.dir_file = dir_file
        self.dir = ''
        self.too_long_nr = 0
        self.stats: dict[str, dict[int, list]] = {
            "function_names": defaultdict(list),
            "variables": defaultdict(list),
            "parameters": defaultdict(list),
            "is_constant_default": defaultdict(list),
        }

    def run_analyzer(self):
        if os.path.isfile(self.dir_file):
            return self.check_pep_compatibility(self.dir_file)

        if os.path.isdir(self.dir_file):
            scripts: list = os.listdir(self.dir_file)
            self.dir = self.dir_file
            for script in scripts:
                script_path: str = os.path.join(self.dir, script)
                self.check_pep_compatibility(script_path)

                self.stats: dict[str, dict[int, list]] = {
                    "function_names": defaultdict(list),
                    "variables": defaultdict(list),
                    "parameters": defaultdict(list),
                    "is_constant_default": defaultdict(list),
                }

    def visit_function_def(self, node):
        if isinstance(node, ast.FunctionDef):
            self.stats['function_names'][node.lineno].append(node.name)

            for a in node.args.args:
                self.stats["parameters"][node.lineno].append(a.arg)

            for a in node.args.defaults:
                self.stats["is_constant_default"][node.lineno].append(isinstance(a, (ast.List, ast.Dict, ast.Set)))

    def get_variable_names(self, node):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0].ctx, ast.Store):
                self.stats["variables"][node.lineno].append(node.targets[0].id)

    def get_class_variable_names(self, node):
        if isinstance(node, ast.Pass):
            return
        nodes = node.body
        for node in nodes:
            if isinstance(node, ast.Assign):
                if isinstance(node.targets[0].ctx, ast.Store):
                    try:
                        self.stats["variables"][node.lineno].append(node.targets[0].id)
                    except AttributeError:
                        self.stats["variables"][node.lineno].append(node.targets[0].attr)

    def get_func_name(self, lineno: int) -> list:
        return self.stats["function_names"][lineno]

    def get_parameters(self, lineno: int) -> list:
        return self.stats["parameters"][lineno]

    def get_variables(self, lineno: int) -> list:
        return self.stats["variables"][lineno]

    def get_mutable_defaults(self, lineno: int) -> str:
        for param_name, is_mutable in zip(self.stats["parameters"][lineno], self.stats["is_constant_default"][lineno]):
            if is_mutable:
                return param_name
        return ""

    def check_line_length_S001(self, i, line_content):
        if len(line_content) > 79:
            print(f"{self.dir_file}: Line {i}: S001 Too long")

    def indent_not_multi_of_four_S002(self, i, line_content):
        if re.match(r"(?!^( {4})*[^ ])", line_content):
            print(f"{self.dir_file}: Line {i}: S002 Indentation is not a multiple of four")

    def semicolon_after_statement_S003(self, i, line_content):
        if re.search(r"^([^#])*;(?!\S)", line_content):
            print(f"{self.dir_file}: Line {i}: S003 Unnecessary semicolon")

    def two_spaces_before_comm_S004(self, i, line_content):
        if re.match(r"[^#]*[^ ]( ?#)", line_content):
            print(f"{self.dir_file}: Line {i}: S004 At least two spaces required before inline comments")

    def found_todo_S005(self, i, line_content):
        if re.search(r"(?i)# *todo", line_content):
            print(f"{self.dir_file}: Line {i}: S005 TODO found")

    def two_blank_lines_S006(self, i, line_content, nr_of_blank_lines):
        if len(line_content) > 1 and nr_of_blank_lines > 2:
            print(f"{self.dir_file}: Line {i}: S006 More than two blank lines used before this line")

    @staticmethod
    def check_for_blank_lines(line_content, nr_of_blank_lines):

        if len(line_content) == 1:
            return 1
        elif len(line_content) > 1 and nr_of_blank_lines > 2:
            return 0
        else:
            return 0

    def too_many_spaces_S007(self, i, line_content):
        if "class" or "def" in line_content:
            if re.match("[ ]*def[ ]{2,}", line_content) is not None:
                print(f"S007 Too many spaces after 'def'")
            if re.match("[ ]*class[ ]{2,}", line_content) is not None:
                print(f"{self.dir_file}: Line {i}: S007 Too many spaces after 'class'")

    def class_name_camelcase_S008(self, i, line_content):
        if "class" in line_content:
            if re.match("[ ]*class[ ]*([A-Z][a-z]+)+[(]?(([A-Z][a-z]+)+)?[}]?:?", line_content) is None:
                name = re.search(r'[^\s]\w*[:]$', line_content).group()[:-1]
                print(f"{self.dir_file}: Line {i}: S008 Class name '{name}' should use CamelCase")

    def function_name_snakecase_S009(self, i, line_content):
        for func_name in self.get_func_name(i):
            if not re.match(r"[a-z_]+", func_name):
                print(f"{self.dir_file}: Line {i + 1}: S009 Function name '{func_name}' should use snake_case")

    def argument_name_snakecase_S010(self, i):
        for parameter in self.get_parameters(i):
            if not re.match(r"[a-z_]+", parameter):
                print(f"{self.dir_file}: Line {i}: S010 Argument name '{parameter}' should be snake_case")

    def variable_name_snakecase_S011(self, i):
        for variable in self.get_variables(i):
            if not re.match(r"[a-z_]+", variable):
                print(f"{self.dir_file}: Line {i}: S011 Argument name '{variable}' should be snake_case")

    def default_arg_val_mutable_S012(self, i):
        if self.get_mutable_defaults(i):
            print(f"{self.dir_file}: Line {i}: S012 Default argument value is mutable")

    def check_pep_compatibility(self, path):
        self.dir_file = path
        with open(path, 'r') as f:
            tree = ast.parse(f.read())
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for class_node in node.body:
                        self.visit_function_def(class_node)
                        self.get_class_variable_names(class_node)
                else:
                    self.visit_function_def(node)
                    self.get_variable_names(node)

            blank_lines = 0
            f.seek(0)
            for i, line in enumerate(f.readlines(), start=1):
                output = [self.check_line_length_S001(i, line),
                          self.indent_not_multi_of_four_S002(i, line),
                          self.semicolon_after_statement_S003(i, line),
                          self.two_spaces_before_comm_S004(i, line),
                          self.found_todo_S005(i, line),
                          self.two_blank_lines_S006(i, line, blank_lines),
                          self.too_many_spaces_S007(i, line),
                          self.class_name_camelcase_S008(i, line),
                          self.function_name_snakecase_S009(i, line),
                          self.argument_name_snakecase_S010(i),
                          self.variable_name_snakecase_S011(i),
                          self.default_arg_val_mutable_S012(i),
                          ]

                blanks = self.check_for_blank_lines(line, blank_lines)

                if blanks == 1:
                    blank_lines += 1
                elif blanks == 0:
                    blank_lines = 0


def get_input():
    parser = argparse.ArgumentParser(description="This program checks if python files follows PEP8")
    parser.add_argument('dir_file')
    args = parser.parse_args()
    return args.dir_file


def main():
    example = CodePEPAnalyzer(get_input())
    example.run_analyzer()


if __name__ == "__main__":
    main()
