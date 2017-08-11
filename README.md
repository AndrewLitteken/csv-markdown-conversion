# CSV to Markdown Converter #

A simple script to convert a `.csv` file into a nicely formatted Markdown table in plain text and when interpreted.

Written in Python and compatible with both Python 2.7 and Python 3.

Can support any delimeter, but a comma is supported by default

### Command Line Options ###
`-h --help` : Show usage statement<br>
`-v --verbose` : Show verbose information at runtime<br>
`-s --same_name` : Use input file name with file ending "md"<br>    
 
`-i --input input_file` : use given file for input<br>
`-o --output output_file` : use given file for output<br>
`-d --delimeter delimeter` : use the given delimeter<br>
`-f --format format_file` : use the given file for formatting<br>

### Formatting File ###
A formatting file can be provided to specify **bolding**, _italics_ and `code` in various cells.

The style is defined by the keywords `bold`, `italics` and `code`.  In a statement these can be placed at any time and multiple styles can be used.

The location is defined by keywords `row` and `col`.  These must be followed by a number in range to define the location.  This keyword and number pair can also be placed at any place in the statement.  `row` or `col` can not be used if the `all` keyword is used following the number.  This defines that an entire row or column will be styled as specified.

There are other special keywords: `title`, `bottom`, `start`, `end`.  These define a location similar to `all`.  `title` will style the top cell, `bottom` the bottom cell, `start` the leftmost cell in the row, and `end` the rightmost cell in the row.  All except for `end` can be used at any time.  The row must be specified previously in the statement for `end` to be used.

#### Examples ####
```
bold row 5 all
bold title col 6 italics
code row 10 col 3
row 10 bold end
```



