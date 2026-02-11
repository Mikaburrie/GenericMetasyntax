
# Context Free Language (CFL) Parser

from collections.abc import Generator

class Group:

    def __init__(self, rule_name, index, length, groups):
        self.rule_name = rule_name
        self.index = index
        self.length = length
        self.slice = slice(index, index+length)
        self.groups: tuple[Group, ...] = groups

    def __repr__(self):
        if len(self.groups) == 0:
            return f"Group({self.rule_name}, {self.index}, {self.length})"
        else:
            groups_string = '\n'.join(str(group) for group in self.groups)
            groups_string = groups_string.replace('\n', '\n\t')
            return f"Group({self.rule_name}, {self.index}, {self.length}, \n\t{groups_string}\n)"

class Parser:
    
    def parse(self, string: str, index: int=0) -> Generator[tuple[int, tuple[Group, ...]]]:
        raise NotImplementedError()

class Terminal(Parser):

    def __init__(self, string: str):
        self.string = string

    def parse(self, string: str, index=0):
        if string.startswith(self.string, index):
            yield len(self.string), ()

    def __repr__(self):
        return f"Terminal({repr(self.string)})"

class Concat(Parser):

    def __init__(self, *parsers: Parser):
        self.parsers = parsers

    def parse(self, string: str, index=0):
        parser_stack = [self.parsers[0].parse(string, index)]
        parsed_stack = []
        parsed_length = 0

        while (parser_count := len(parser_stack)) > 0:
            try:
                # Get next parse option and append to stack
                parser = parser_stack[-1]
                parsed_stack.append(next(parser))
                parsed_length += parsed_stack[-1][0]

                # Add next parser to stack
                if parser_count != len(self.parsers):
                    parser = self.parsers[parser_count].parse(string, index + parsed_length)
                    parser_stack.append(parser)
                    continue

                # Stack is full, yield group option
                groups = sum((group for _, group in parsed_stack), start=())
                yield parsed_length, groups

            except StopIteration:
                # Remove parser when group options are exhausted
                parser_stack.pop()

            if len(parsed_stack) > 0:
                length, _ = parsed_stack.pop()
                parsed_length -= length

    def __repr__(self):
        if len(self.parsers) == 0:
            return f"Concat()"
        else:
            parsers_string = '\n'.join(str(parser) for parser in self.parsers)
            parsers_string = parsers_string.replace('\n', '\n\t')
            return f"Concat(\n\t{parsers_string}\n)"

class Union(Parser):

    def __init__(self, *parsers: Parser):
        self.parsers = parsers

    def parse(self, string: str, index=0):
        for parser in self.parsers:
            for parsed in parser.parse(string, index):
                yield parsed

    def __repr__(self):
        if len(self.parsers) == 0:
            return f"Union()"
        else:
            parsers_string = '\n'.join(str(parser) for parser in self.parsers)
            parsers_string = parsers_string.replace('\n', '\n\t')
            return f"Union(\n\t{parsers_string}\n)"

class Star(Parser):

    def __init__(self, parser: Parser):
        self.parser = parser
    
    def parse(self, string: str, index=0):
        parser_stack = [self.parser.parse(string, index)]
        parsed_stack = []
        parsed_length = 0

        while len(parser_stack) > 0:
            try:
                # Get next parse option and append to stack
                parser = parser_stack[-1]
                parsed_stack.append(next(parser))
                parsed_length += parsed_stack[-1][0]

                # Add next parser to stack
                parser = self.parser.parse(string, index + parsed_length)
                parser_stack.append(parser)

            except StopIteration:
                # Remove parser when group options are exhausted
                parser_stack.pop()

                # Yield group option
                groups = sum((group for _, group in parsed_stack), start=())
                yield parsed_length, groups
                if len(parsed_stack) > 0:
                    length, _ = parsed_stack.pop()
                    parsed_length -= length

    def __repr__(self):
        parser_string = str(self.parser).replace('\n', '\n\t')
        return f"Star(\n\t{parser_string}\n)"

class Rule(Parser):

    def __init__(self, name: str):
        self.name = name
        self.parser: Parser = None

    def parse(self, string: str, index=0):
        if self.parser == None:
            raise RuntimeError(f"rule '{self.name}' has no definition")
        for length, groups in self.parser.parse(string, index):
            yield length, (Group(self.name, index, length, groups),) if self.name[0] != '_' else groups

    def __repr__(self):
        return f"Rule('{self.name}')"

class Grammar:
    
    def __init__(self):
        self.rules: dict[str, Rule] = dict()
    
    def __getitem__(self, rule_name):
        rule = self.rules.get(rule_name)
        if rule != None:
            return rule

        rule = Rule(rule_name)
        self.rules[rule_name] = rule
        return rule

    def __setitem__(self, rule_name, parser: Parser):
        rule = self[rule_name]
        rule.parser = parser
