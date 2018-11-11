# md_tangle.py

## Usage

Take the following Markdown (`HelloWorld.md`):
```markdown
# Some title

Describing the following code... bla bla.

/```javascript tangle:helloWorld.js
console.log("Hello, world");
/```

By adding some css ... 

/~~~~css tangle:styles/button.css
#button1 {
    border: none;
}
/~~~~

```

By adding `md-tangle.py` to `$PATH`, one could simply produce files from this file by
executing:

```bash
$ md_tangle --verbose HelloWorld.md
helloWorld.js                                      1 lines
styles/button.css                                  3 lines
```
