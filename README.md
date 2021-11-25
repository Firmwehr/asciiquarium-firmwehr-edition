# Asciiquarium by Firmwehr

This repo contains a small handmade (not in Seattle though) implementation of
the popular [Asciiqarium](https://robobunny.com/projects/asciiquarium/html/)
program.

All code except the ASCII art in it is novel, as existing solutions typically
use completely unnecessary language features, such as:
- for loops
- postfix increment
- interfaces
- inheritance
- Strings *(who needs those???)*
- Lists

## How it works
This repo contains a [input.txt](input.txt) file with all the ASCII-art. It is
loosely based on
[Asciiqarium.java](https://github.com/cmatsuoka/asciiquarium-applet). A python
script is then used to convert the magical Strings in that file to more
reasonable data structures. The output of the script can then be pasted
verbatim in `Asciiquarium.java` to apply the changes.


## Why?
Oh boy, we are *way* past asking that question! Some non-trivial programs are
nice to find edge cases in your compiler though. This repo also just outright
crashes `libFirm` in many interesting ways if you do not split up the output
into small chunks, which is always fun :^)
