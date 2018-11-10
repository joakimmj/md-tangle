# Test tangling of code 

## Some info about files

This is some css.. 
~~~~css tangle:test.css
#button1 {
    border: none;
}
~~~~

Could also be written in javascript:
```javascript tangle:test.js
console.log("Hello world")
```

## More info about the css file

Add to css-file
```css tangle:test.css <random string>
#button2 {
    border: none;
}
```


This ```file``` can be `tangled` with `md-tangle`. 

```This``` lines starts with code block separator, but also closes it. This will
not be tangled.
