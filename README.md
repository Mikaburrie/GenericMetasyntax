# Generic Metasyntax for Context Free Language (CFL) Parsing
## Overview
The goal of this project is to create a metasyntax, represent the metasyntax using itself, and then create a parser for the metasyntax that can generate a parser for the metasyntax (that can generate a parser for the metasyntax... ad infinitum)

#### Files
`cfl.py` - Defines classes for parsing Context Free Languages (CFLs) based on generator functions. Rule names that start with an underscore (_) are excluded from the parse tree output

`gms.py` - Defines the Generic Metasyntax using parsers from clf.py

`generic_metasyntax.gms` - Defines the Generic Metasyntax using Generic Metasyntax

`test.py` - Parses generic_metasyntax.gms using the defintions in gms.py, generates a grammar for Generic Metasyntax from the resulting parse tree, and uses the generated grammar to parse generic_metasyntax.gms again. Equivalency of production rules is checked, proving the 'parse, generate grammar, parse, generate grammar...' cycle can be repeated infintely
