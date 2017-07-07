# Simple Macro Processor for Public Configurations
This program reads a text file, expands the macros variable founds in the text, and writes the updates lines to standard output.  Its purpose is to replace personal or confidential information, such a locations, user identifications, and passwords, in configuration files or C/C++ headers. 

## License
This program is released under a MIT [license](./LICENSE).

## Implementation
The program in written in Python 2.7 and was developed and tested on **Arch Linux** systems running on ARM processors, Mac OS El Capitan 10.11.6, and Centos 7.3.

## Installation
* Change the **Makefile** updating the`DEST_DIR` macro to specify the target directory.
* Issue `make install`

## Usage
### Command
`smp [-m json-file] [-Dmacro[=definition]...] file`

* `json-file` is a JSON file that contains macros followed by their definitions.
* `-Dmacro[=definition]` supplies a macro definition from the command line.  This optional and can be specified more than once.  If a macro is specified without a definition, it is assigned a zero-length string.
* `file` is the input text file; if not supplied standard input will be read.
* The updated text is written to standard output.

### Macro Expansion
After the input text is written, all lines are processed for macro variables in a format similar to **Bash* shell variables: `${name[-default]}`.  There `name` is a standard C Language variable name.   The `name` can be followed by a hypen/dash and a default string to be used if there is no macro definition.

### Error Processing
If a macro variable is found without a definition, the generated output is marked with an error indicator before and after the line.  The command will return a value of 1 to indicate the failure.

## Things To Do
* Provide update-in-place option.
* Proper **man** page.
* Allow macro expansions to contain macros.
* Convert to Python 3 when CentOS makes a RPM available is a current (3.6 or later) release.
