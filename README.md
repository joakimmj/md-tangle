[![app-badge]][PyPI-md-tangle] ![Version] ![License] ![Format] ![PyVer] ![Downloads]

# [md-tangle][PyPI-md-tangle]
This project is a result of wanting config and setup files to be part of a document 
explaining my setup. I originally used [Org-mode][1] and [org-babel-tangle][2] in 
[Emacs][3] to achieve this. I really like Org-mode and Emacs, but I'm not fond of
being dependent on one editor. This is the reason I wanted a [CLI][4], and a more 
widely used document [markup language][5].

This way of programming is called [literate programming][6]. This programming paradigm 
was introduced by Donald Knuth. The idea is to write a program as an explanation of the
program logic in a natural language interspersed with snippets of traditional source code.
The source code can then be generated ("tangled") by using some tool.

As [Markdown][7] is used by most programmers, I saw that language fit for the task.
Markdown is a plaintext-ish format popular with programmers. It's simple, easy and 
already has support for embedding code blocks using ``` or ~~~~, mostly 
for the purposes of syntax highlighting in documentation.

## Installing
This CLI tool can be installed from PyPI using `pip`.

```bash
pip install md-tangle
```

For local development, you can install it in editable mode:

```bash
pip install -e .
```

## Command
By adding the keyword `tangle:<path/filename>`, this tool will tangle tagged code
blocks to given file. Supports `~` for home directory.

One can tangle the code block to multiple files by separating the files with chosen separator (default: `,`).

If the file already exists, the user will be prompted with the option to overwrite,
unless the `-f`/`--force` flag is added.

### Tags

By adding the keyword `tags:<tag>` to a tangled code block, it will NOT be included
in the resulting files if not included with the `-i`/`--include` flag.

### Flags

* `-h`/`--help`: Show help message and exit
* `--version`: Show installed version
* `-f`/`--force`: Force overwrite of files if the already exists
* `-v`/`--verbose`: Show output
* `-d`/`--destination`: Overwrite output destination
* `-i`/`--include`: Include tagged code blocks (separator=',')
* `-s`/`--separator`: Separator for tangle destinations (default=',')
* `-p`/`--block-padding`: Add N newlines between code blocks when writing to file (default=0)

## Usage

Take the following example:

`HelloWorld.md`
```markdown
# Some title
Describing the following code... bla bla.

~~~~javascript tangle:helloWorld.js
console.log("Hello, ");
console.log("world");
~~~~

## Styling
Adding header for my css files:

~~~~css tangle:styles/button.css,styles/input.css
/* Styling for mye awesome app */
~~~~

By adding some css ... 

~~~~css tangle:styles/button.css
#button1 {
    border: none;
}
~~~~

~~~~css tangle:styles/input.css
#button1 {
    border: none;
}
~~~~

~~~~css tangle:styles/theme.css tags:theme
#button1 {
    border-color: red;
}
~~~~
```

By installing `md-tangle` with `pip`, one could simply produce files from this file by executing:

```bash
$ md-tangle -v HelloWorld.md 
helloWorld.js                                      2 lines
styles/button.css                                  4 lines
styles/input.css                                   4 lines
$ ls 
helloWorld.js HelloWorld.md styles
```

If you also want to include tagged code blocks, you can run
```bash
$ md-tangle -v -i theme HelloWorld.md
helloWorld.js                                      2 lines
styles/button.css                                  4 lines
styles/input.css                                   4 lines
styles/theme.css                                   3 lines
$ ls
helloWorld.js HelloWorld.md styles
```

## Documentation

The [documentation][8] for `md-tangle` is of course written in Markdown, and tangles to the source
code.


[1]: https://en.wikipedia.org/wiki/Org-mode
[2]: https://orgmode.org/manual/Extracting-source-code.html
[3]: https://www.gnu.org/software/emacs/
[4]: https://en.wikipedia.org/wiki/Command-line_interface
[5]: https://en.wikipedia.org/wiki/Markup_language
[6]: https://en.wikipedia.org/wiki/Literate_programming
[7]: https://en.wikipedia.org/wiki/Markdown
[8]: https://github.com/joakimmj/md-tangle/blob/master/DOCS.md

[app-badge]: https://img.shields.io/badge/md--tangle-PyPI-orange.svg
[PyPI-md-tangle]: https://pypi.org/project/md-tangle
[Version]: https://img.shields.io/github/tag/joakimmj/md-tangle.svg?label=version
[License]: https://img.shields.io/github/license/joakimmj/md-tangle.svg
[Format]: https://img.shields.io/pypi/format/md_tangle.svg
[PyVer]: https://img.shields.io/pypi/pyversions/md-tangle.svg
[Downloads]: https://img.shields.io/pypi/dm/md-tangle.svg
