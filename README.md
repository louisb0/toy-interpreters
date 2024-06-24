# toy-interpreters

An implementation of both tree walking and bytecode interpreters from the books by Thorsten Ball and Robert Nystrom.

All the code is very messy and has never been refactored / cleaned up. The purpose of these projects is to get a basic understanding of interpreters and language design before creating my own hobby language.


## Notes

Stuff I thought about while working on this repo that I'd like to look back on when developing my own toy language.

### Interesting Features 

* Errors as values
* Error productions & Python-esque formatting
* Ternary
* Linux/Mac/Windows keywords, e.g. `fn linux function() {}`
* Statically typed
* Some concept of a standard library
* `defer` and `comptime` keywords from Zig
* Generics
* Async
* LSP/Formatter
* Destructuring
* Optional chaining
* Switch 
* Lazy evaluation
* Format strings
* List comprehension
* For-in loops

### Resources

* [https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/](https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/)
* [https://docs.python.org/3/reference/grammar.html](https://docs.python.org/3/reference/grammar.html)
* [https://go.dev/ref/spec](https://go.dev/ref/spec)
