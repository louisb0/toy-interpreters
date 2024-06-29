# toy-interpreters

An implementation of both tree walking and bytecode interpreters from the books by Thorsten Ball and Robert Nystrom.

All the code is very messy and has never been refactored / cleaned up. The purpose of these projects is to get a basic understanding of interpreters and language design before creating my own hobby language.


## Notes

Stuff I thought about while working on this repo that I'd like to look back on when developing my own toy language.

### Interesting Features 

* Errors as values
* Error productions & Python-esque string formatting
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
* Tail call optimisation
* Anonymous functions
* Modules

### Resources

* [https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/](https://eli.thegreenplace.net/2019/go-compiler-internals-adding-a-new-statement-to-go-part-1/)
* [https://go.dev/ref/spec](https://go.dev/ref/spec)
* [lexer modes https://www.oilshell.org/blog/2017/12/17.html](https://www.oilshell.org/blog/2017/12/17.html)
* [https://docs.python.org/3/reference/grammar.html](https://docs.python.org/3/reference/grammar.html)
* [https://eli.thegreenplace.net/tag/python-internals](https://eli.thegreenplace.net/tag/python-internals)
* [https://tech.blog.aknin.name/category/my-projects/pythons-innards/](https://tech.blog.aknin.name/category/my-projects/pythons-innards/)
* [https://github.com/python/cpython/blob/main/InternalDocs/compiler.md](https://github.com/python/cpython/blob/main/InternalDocs/compiler.md)
* [https://realpython.com/cpython-source-code-guide/](https://realpython.com/cpython-source-code-guide/)
* [https://tenthousandmeters.com/blog/python-behind-the-scenes-3-stepping-through-the-cpython-source-code/](https://tenthousandmeters.com/blog/python-behind-the-scenes-3-stepping-through-the-cpython-source-code/)
* [https://futhark-lang.org/blog.html](https://futhark-lang.org/blog.html)
* [https://existentialtype.wordpress.com/2011/04/16/modules-matter-most/](https://existentialtype.wordpress.com/2011/04/16/modules-matter-most/)
