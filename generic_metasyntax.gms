
_char_lower = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
_char_upper = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
_char_alpha = _char_lower | _char_upper
_char_numeric = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
_char_alnum = _char_alpha | _char_numeric
_char_symbol = "_" | "=" | "*" | "," | "|" | "(" | ")" | "#"
_char_backslash = "\\", ("\\" | "'" | '"' | "n" | "r" | "t" | "b" | "f")
_char_whitespace = " " | "\t"

_terminal_char = _char_alnum | _char_symbol | _char_backslash | _char_whitespace
double_string = *(_terminal_char | "'")
single_string = *(_terminal_char | '"')
terminal = '"', double_string, '"' | "'", single_string, "'"

_rule_name_char = _char_lower | "_"
rule_name = _rule_name_char, *_rule_name_char

_star_expressions = _parentheses | terminal | rule_name
star = "*", _star_expressions

_concat_expressions = _parentheses | terminal | star | rule_name
concat = _concat_expressions, ", ", _concat_expressions, *(", ", _concat_expressions)

_union_expressions = _parentheses | terminal | star | rule_name | concat
union = _union_expressions, " | ", _union_expressions, *(" | ", _union_expressions)

_all_expressions = _parentheses | terminal | star | rule_name | union | concat
_parentheses = "(", _all_expressions, ")"

_comment = "#", *(_terminal_char | "'" | '"')
rule = rule_name, " = ", _all_expressions
grammar = *"\n", (_comment | rule), *("\n", *"\n", (_comment | rule)), *"\n"
