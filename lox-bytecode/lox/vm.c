#include <stdarg.h>
#include <stdio.h>

#include "chunk.h"
#include "common.h"
#include "compiler.h"
#include "debug.h"
#include "value.h"
#include "vm.h"

VM vm;

static void reset_stack() { vm.stack_top = vm.stack; }

static void runtime_error(const char *format, ...) {
  va_list args;
  va_start(args, format);
  vfprintf(stderr, format, args);
  va_end(args);
  fputs("\n", stderr);

  size_t instruction = vm.ip - vm.chunk->code - 1;
  int line = get_line(vm.chunk, (int)instruction);
  fprintf(stderr, "[line %d] in script\n", line);
  reset_stack();
}

void init_vm() { reset_stack(); }

void free_vm() {}

void push(Value value) {
  *vm.stack_top = value;
  vm.stack_top++;
}

Value pop() {
  vm.stack_top--;
  return *vm.stack_top;
}

static Value peek(int distance) { return vm.stack_top[-1 - distance]; }

static InterpretResult run() {
#define READ_BYTE() (*vm.ip++)
#define READ_CONSTANT() (vm.chunk->constants.values[READ_BYTE()])
#define BINARY_OP(value_type, op)                                              \
  do {                                                                         \
    if (!IS_NUMBER(peek(0)) || !IS_NUMBER(peek(1))) {                          \
      runtime_error("Operands must be numbers");                               \
      return INTERPRET_RUNTIME_ERROR;                                          \
    }                                                                          \
    double b = AS_NUMBER(pop());                                               \
    double a = AS_NUMBER(pop());                                               \
    push(value_type(a op b));                                                  \
  } while (false);

  for (;;) {
#ifdef DEBUG_TRACE_EXECUTION
    printf("          ");
    for (Value *slot = vm.stack; slot < vm.stack_top; slot++) {
      printf("[ ");
      print_value(*slot);
      printf(" ]");
    }
    printf("\n");
    dissassemble_instruction(vm.chunk, (int)(vm.ip - vm.chunk->code));
#endif

    uint8_t instruction;
    switch (instruction = READ_BYTE()) {
    case OP_CONSTANT:
      push(READ_CONSTANT());
      break;
    case OP_ADD:
      BINARY_OP(NUMBER_VAL, +);
      break;
    case OP_SUBTRACT:
      BINARY_OP(NUMBER_VAL, -);
      break;
    case OP_MULTIPLY:
      BINARY_OP(NUMBER_VAL, *);
      break;
    case OP_DIVIDE:
      BINARY_OP(NUMBER_VAL, /);
      break;
    case OP_NEGATE:
      if (!IS_NUMBER(peek(0))) {
        runtime_error("Operand must be a number.");
        return INTERPRET_RUNTIME_ERROR;
      }

      push(NUMBER_VAL(-AS_NUMBER(pop())));
      break;
    case OP_RETURN:
      print_value(pop());
      printf("\n");
      return INTERPRET_OK;
    }
  }

#undef READ_BYTE
#undef READ_CONSTANT
#undef BINARY_OP
}

InterpretResult interpret(const char *source) {
  Chunk chunk;
  init_chunk(&chunk);

  if (!compile(source, &chunk)) {
    free_chunk(&chunk);
    return INTERPRET_COMPILE_ERROR;
  }

  vm.chunk = &chunk;
  vm.ip = vm.chunk->code;

  InterpretResult result = run();

  free_chunk(&chunk);
  return result;
}
