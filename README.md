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
* No implicit redeclarations, e.g. `fn func(a) { var a = 10; }`
* No implicit nil
* Constant folding
* Dead code elimination
* Control flow analysis
* Flat ASTs
* Tracebacks

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
* [https://blog.regehr.org/](https://blog.regehr.org/)
* [http://richardartoul.github.io/jekyll/update/2015/04/26/hidden-classes.html](http://richardartoul.github.io/jekyll/update/2015/04/26/hidden-classes.html)
* [https://pointersgonewild.com/](https://pointersgonewild.com/)
* [http://gameprogrammingpatterns.com/](http://gameprogrammingpatterns.com/)
* [https://journal.stuffwithstuff.com/](https://journal.stuffwithstuff.com/)
* [https://blog.subnetzero.io/](https://blog.subnetzero.io/)
* [https://en.m.wikibooks.org/wiki/Creating_a_Virtual_Machine/Register_VM_in_C](https://en.m.wikibooks.org/wiki/Creating_a_Virtual_Machine/Register_VM_in_C)
* [https://connascence.io/](https://connascence.io/)
* [https://www.pollylabs.org/education.html](https://www.pollylabs.org/education.html)
* [https://www.cs.colostate.edu/~pouchet/index.html#lectures](https://www.cs.colostate.edu/~pouchet/index.html#lectures)
* **[http://compileroptimizations.com/](http://compileroptimizations.com/)**
* [https://llvm.org/docs/Passes.html](https://llvm.org/docs/Passes.html)
* [https://www.cs.cornell.edu/courses/cs6120/2020fa/self-guided/](https://www.cs.cornell.edu/courses/cs6120/2020fa/self-guided/)
* [https://blog.trailofbits.com/category/compilers/page/2/](https://blog.trailofbits.com/category/compilers/page/2/)
* [https://blog.regehr.org/archives/2485](https://blog.regehr.org/archives/2485)
* [https://www.youtube.com/watch?v=V8dnIw3amLA](https://www.youtube.com/watch?v=V8dnIw3amLA)
* [https://compilers.cs.uni-saarland.de/papers/bbhlmz13cc.pdf](https://compilers.cs.uni-saarland.de/papers/bbhlmz13cc.pdf)
* [https://github.com/SeaOfNodes/Simple/tree/main](https://github.com/SeaOfNodes/Simple/tree/main)
* [https://www.youtube.com/watch?v=9epgZ-e6DUU](https://www.youtube.com/watch?v=9epgZ-e6DUU)
* [https://bernsteinbear.com/pl-resources/](https://bernsteinbear.com/pl-resources/)
* [https://old.reddit.com/r/Compilers/comments/rvnesz/resources_for_learning_compiler_design/hr88qo0/](https://old.reddit.com/r/Compilers/comments/rvnesz/resources_for_learning_compiler_design/hr88qo0/)
* [https://iliabylich.github.io/arena-based-parsers/tldr.html](https://iliabylich.github.io/arena-based-parsers/tldr.html)
