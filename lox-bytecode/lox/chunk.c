#include "chunk.h"
#include "memory.h"

void init_chunk(Chunk *chunk) {
  chunk->capacity = 0;
  chunk->count = 0;
  chunk->code = NULL;

  init_value_array(&chunk->constants);
  init_line_info(&chunk->line_info);
}

void free_chunk(Chunk *chunk) {
  FREE_ARRAY(uint8_t, chunk->code, chunk->capacity);
  free_value_array(&chunk->constants);
  free_line_info(&chunk->line_info);

  init_chunk(chunk);
}

void write_chunk(Chunk *chunk, uint8_t byte, int line) {
  if (chunk->capacity < chunk->count + 1) {
    int old_capacity = chunk->capacity;
    chunk->capacity = GROW_CAPACITY(old_capacity);
    chunk->code =
        GROW_ARRAY(uint8_t, chunk->code, old_capacity, chunk->capacity);
  }

  write_line_info(&chunk->line_info, line);
  chunk->code[chunk->count] = byte;
  chunk->count++;
}

int add_constant(Chunk *chunk, Value value) {
  write_value_array(&chunk->constants, value);
  return chunk->constants.count - 1;
}

int get_line(Chunk *chunk, int offset) {
  int index = 0;

  while (index < chunk->line_info.count && offset >= 0) {
    int line = chunk->line_info.lines[index];
    int line_length = chunk->line_info.lines[index + 1];

    if (offset < line_length) {
      return line;
    }

    offset -= line_length;
    index += 2;
  }

  assert(!"Unreachable");
}
