
from cfl import *

gms = Grammar()

gms['_char_lower'] = Union(*(Terminal(c) for c in 'abcdefghijklmnopqrstuvwxyz'))
gms['_char_upper'] = Union(*(Terminal(c) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
gms['_char_alpha'] = Union(gms['_char_lower'], gms['_char_upper'])
gms['_char_numeric'] = Union(*(Terminal(c) for c in '0123456789'))
gms['_char_alnum'] = Union(gms['_char_alpha'], gms['_char_numeric'])
gms['_char_symbol'] = Union(*(Terminal(c) for c in '_=*,|()#'))
gms['_char_backslash'] = Concat(Terminal('\\'), Union(*(Terminal(c) for c in '\\\'"nrtbf')))
gms['_char_whitespace'] = Union(*(Terminal(c) for c in ' \t'))

gms['_terminal_char'] = Union(gms['_char_alnum'], gms['_char_symbol'], gms['_char_backslash'], gms['_char_whitespace'])
gms['double_string'] = Star(Union(gms['_terminal_char'], Terminal("'")))
gms['single_string'] = Star(Union(gms['_terminal_char'], Terminal('"')))
gms['terminal'] = Union(Concat(Terminal('"'), gms['double_string'], Terminal('"')), Concat(Terminal("'"), gms['single_string'], Terminal("'")))

gms['_rule_name_char'] = Union(gms['_char_lower'], Terminal('_'))
gms['rule_name'] = Concat(gms['_rule_name_char'], Star(gms['_rule_name_char']))

gms['_star_expressions'] = Union(gms['_parentheses'], gms['terminal'], gms['rule_name'])
gms['star'] = Concat(Terminal('*'), gms['_star_expressions'])

gms['_concat_expressions'] = Union(gms['_parentheses'], gms['terminal'], gms['star'], gms['rule_name'])
gms['concat'] = Concat(gms['_concat_expressions'], Terminal(', '), gms['_concat_expressions'], Star(Concat(Terminal(', '), gms['_concat_expressions'])))

gms['_union_expressions'] = Union(gms['_parentheses'], gms['terminal'], gms['star'], gms['rule_name'], gms['concat'])
gms['union'] = Concat(gms['_union_expressions'], Terminal(' | '), gms['_union_expressions'], Star(Concat(Terminal(' | '), gms['_union_expressions'])))

gms['_all_expressions'] = Union(gms['_parentheses'], gms['terminal'], gms['star'], gms['rule_name'], gms['union'], gms['concat'])
gms['_parentheses'] = Concat(Terminal('('), gms['_all_expressions'], Terminal(')'))

gms['_comment'] = Concat(Terminal('#'), Star(Union(gms['_terminal_char'], Terminal("'"), Terminal('"'))))
gms['rule'] = Concat(gms['rule_name'], Terminal(' = '), gms['_all_expressions'])
gms['grammar'] = Concat(Star(Terminal("\n")), Union(gms['_comment'], gms['rule']), Star(Concat(Terminal("\n"), Star(Terminal("\n")), Union(gms['_comment'], gms['rule']))), Star(Terminal("\n")))
