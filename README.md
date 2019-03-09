# md-tangle

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

## Command
By adding the command `tangle:<path/filename>`, this tool will tangle tagged code
blocks to given file. Supports `~` for home directory.

If the file already exists, the user will be prompted with the option to overwrite,
unless the `-f`/`--force` flag is added.

### Flags

* `-h`/`--help`: Show help message and exit
* `-f`/`--force`: Force overwrite of files if the already exists
* `-v`/`--verbose`: Show output
  
## Usage

Take the following example:

`HelloWorld.md`
```markdown
# Some title

Describing the following code... bla bla.

~~~~javascript tangle:helloWorld.js
console.log("Hello, world");
~~~~

By adding some css ... 

~~~~css tangle:styles/button.css
#button1 {
    border: none;
}
~~~~

```

By adding installing `md-tangle` with `pip`, one could simply produce files from this file by
executing:

```bash
$ md-tangle -v HelloWorld.md 
helloWorld.js                                      2 lines
styles/button.css                                  4 lines
$ ls 
helloWorld.js HelloWorld.md styles
```

> If one wishes to use Python 2, one could easily install `md-tangle2` instead.

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
