#ifndef lox_debug_h
#define lox_debug_h

#include "chunk.h"

void dissassemble_chunk(Chunk *chunk, const char *name);
int dissassemble_instruction(Chunk *chunk, int offset);

#endif
