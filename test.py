#!/usr/bin/env python3

import ast
import sys

from gms import *

# Get leftmost generic metasyntax parse of generic_metasyntax.gms
with open("generic_metasyntax.gms") as text_file:
    text = text_file.read()

for length, groups in gms['grammar'].parse(text):
    if length == len(text):
        parsed_grammar = groups[0]
        break
else:
    print("No parse trees")
    sys.exit(1)

def build_expression(expression_group: Group, grammar: Grammar, text: str):
    rule_name = expression_group.rule_name
    expressions = (build_expression(group, grammar, text) for group in expression_group.groups)
    match rule_name:
        case 'union':
            return Union(*expressions)
        case 'concat':
            return Concat(*expressions)
        case 'star':
            return Star(*expressions)
        case 'terminal':
            terminal_string = ast.literal_eval(text[expression_group.slice])
            return Terminal(terminal_string)
        case 'rule_name':
            rule_name = text[expression_group.slice]
            rule = grammar[rule_name]
            return rule

# Generate generic metasyntax grammar from parsed generic_metasyntax.gms
generated_grammar = Grammar()
for rule in parsed_grammar.groups:
    rule_name_group, expression_group = rule.groups
    rule_name = text[rule_name_group.slice]
    expression = build_expression(expression_group, generated_grammar, text)
    generated_grammar[rule_name] = expression
    # print(repr(grammar[rule_name].parser))
    # print(repr(gms[rule_name].parser))
    print(rule_name, "matches gms.py:", repr(generated_grammar[rule_name].parser) == repr(gms[rule_name].parser))

# Parse generic_metasyntax.gms with generic metasyntax grammar generated from generic_metasyntax.gms
for length, groups in generated_grammar['grammar'].parse(text):
    if length == len(text):
        parsed_grammar = groups[0]
        print(parsed_grammar)
        break
