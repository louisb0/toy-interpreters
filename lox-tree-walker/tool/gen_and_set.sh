#!/bin/zsh

python ast_gen.py ast_spec.yml
mv ast_out.py ../lox/ast.py   
mv visitors_out.py ../lox/visitors/visitor.py
