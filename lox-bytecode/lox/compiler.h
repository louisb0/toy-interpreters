#ifndef lox_compiler_h
#define lox_compiler_h

#include "chunk.h"

bool compile(const char *source, Chunk *chunk);

#endif
