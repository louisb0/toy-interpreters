#include "lox/chunk.h"
#include "lox/debug.h"
#include "lox/vm.h"

int main(int argc, char *argv[]) {
  init_vm();

  Chunk chunk;
  init_chunk(&chunk);

  int constant = add_constant(&chunk, 3);
  write_chunk(&chunk, OP_CONSTANT, 12);
  write_chunk(&chunk, constant, 12);
  write_chunk(&chunk, OP_RETURN, 12);

  constant = add_constant(&chunk, 4);
  write_chunk(&chunk, OP_CONSTANT, 12);
  write_chunk(&chunk, constant, 12);
  write_chunk(&chunk, OP_RETURN, 12);

  constant = add_constant(&chunk, 5);
  write_chunk(&chunk, OP_CONSTANT, 13);
  write_chunk(&chunk, constant, 13);
  write_chunk(&chunk, OP_RETURN, 13);

  constant = add_constant(&chunk, 5);
  write_chunk(&chunk, OP_CONSTANT, 14);
  write_chunk(&chunk, constant, 14);
  write_chunk(&chunk, OP_RETURN, 14);

  // dissassemble_chunk(&chunk, "test");
  interpret(&chunk);
  free_vm();
  free_chunk(&chunk);
}
