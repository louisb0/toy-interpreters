#include <stdio.h>

#include "chunk.h"
#include "debug.h"

static int constant_instruction(const char *name, Chunk *chunk, int offset);
static int simple_instruction(const char *name, int offset);

void dissassemble_chunk(Chunk *chunk, const char *name) {
  assert(chunk != NULL);
  assert(name != NULL);

  printf("=== %s ===\n", name);

  for (int offset = 0; offset < chunk->count;) {
    offset = dissassemble_instruction(chunk, offset);
  }
}

int dissassemble_instruction(Chunk *chunk, int offset) {
  assert(chunk != NULL);
  assert(offset >= 0);

  printf("%04d ", offset);
  if (offset > 0 && get_line(chunk, offset) == get_line(chunk, offset - 1)) {
    printf("   | ");
  } else {
    printf("%4d ", get_line(chunk, offset));
  }

  uint8_t instruction = chunk->code[offset];
  switch (instruction) {
  case OP_CONSTANT:
    return constant_instruction("OP_CONSTANT", chunk, offset);
  case OP_ADD:
    return simple_instruction("OP_ADD", offset);
  case OP_SUBTRACT:
    return simple_instruction("OP_SUBTRACT", offset);
  case OP_MULTIPLY:
    return simple_instruction("OP_MULTIPLY", offset);
  case OP_DIVIDE:
    return simple_instruction("OP_DIVIDE", offset);
  case OP_NEGATE:
    return simple_instruction("OP_NEGATE", offset);
  case OP_RETURN:
    return simple_instruction("OP_RETURN", offset);
  default:
    printf("Unknown opcode %d\n", instruction);
    return offset + 1;
  }
}

static int constant_instruction(const char *name, Chunk *chunk, int offset) {
  uint8_t constant = chunk->code[offset + 1];
  printf("%-16s %4d '", name, constant);
  print_value(chunk->constants.values[constant]);
  printf("'\n");
  return offset + 2;
}

static int simple_instruction(const char *name, int offset) {
  printf("%s\n", name);
  return offset + 1;
}
