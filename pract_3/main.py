import json
import sys
import re

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, text):
        text = self.remove_multiline_comments(text)
        self.parse_expressions(text)
        json_output = json.dumps(self.constants, indent=4)
        return json_output

    def remove_multiline_comments(self, text):
        return re.sub(r'\{\{!.*?\}\}', '', text, flags=re.DOTALL)
    
    def parse_value(self, value: str):
        if value.startswith("@"):
            return value.strip('@""')
        elif value.startswith(".[") and (value.endswith("].,") or value.endswith('].') or value.endswith('].;')):
            return self.evaluate_expression(value)
        elif value in self.constants:
            return self.constants[value]
        elif value.isdigit():
            return int(value)
        elif value.startswith('dict(') and (value.endswith("),") or value.endswith(')') or value.endswith(');')):
            return self.parse_dict(value)

        
    def parse_expressions(self, text):
        lines = text.split(';')
        result = {}
        for line in lines:
            line = line.strip()
            if 'is' not in line:
                continue
            name, value = line.split(' is ')
            name = name.strip()
            value = value.strip()
            self.constants[name] = self.parse_value(value)
        return result
    
    def _is_operator(self, c):
        return c in ['+', '-', '*', '/']

    def evaluate_expression(self, postfix_expr):
        stack = []
        tokens = postfix_expr.strip('.[].').split()
        for char in tokens:
            if not self._is_operator(char):
                stack.append(char)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                new_expr = f"({operand1}{char}{operand2})"
                stack.append(new_expr)
        infix = stack.pop()
        try:
            int_variables = {}
            for key, value in self.constants.items():
                if isinstance(value, int):
                    int_variables[key] = value
            allowed_globals = {"__builtins__": None, "max": max, "print": print}
            result = eval(infix, allowed_globals, int_variables)
            return result
        except Exception as e:

            raise ValueError(f"Error evaluating expression: {postfix_expr} ({e})")


    def find_dict_pos(self, text: str, start: int):
        count_of_open_brackets = 0
        count_of_close_brackets = 0
        end = start
        for sym in text:
            end += 1
            if sym == "(":
                count_of_open_brackets += 1
            elif sym == ")":
                count_of_close_brackets += 1
            if count_of_open_brackets == count_of_close_brackets and count_of_open_brackets != 0:
                return end
        raise ValueError("Incorect quotes!")

    def parse_dict(self, line):
        cleaned_line = line.strip('dict()')
        items = cleaned_line.split(',\n')
        result = {}
        shift = 0
        for item in items:
            name, value = item.split('=', 1)
            name = name.strip()
            value = value.strip()
            if value.startswith("dict"):
                start = cleaned_line.find('dict(')
                end = self.find_dict_pos(cleaned_line[cleaned_line.find('dict('):], start)
                result[name] = self.parse_value(cleaned_line[start:end])
                shift = end
            elif shift <= cleaned_line.find(item):
                result[name] = self.parse_value(value)
        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python config_parser.py output.json")
        sys.exit(1)

    output_file = sys.argv[1]

    config_text = sys.stdin.read()

    parser = ConfigParser()
    try:
        json_output = parser.parse(config_text)
        with open(output_file, 'w') as json_file:
            json_file.write(json_output)
        print(f"Output written to {output_file}")
    except ValueError as e:
        print(f"Syntax error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
