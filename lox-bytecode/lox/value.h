#ifndef lox_value_h
#define lox_value_h

#include "common.h"

typedef double Value;

typedef struct {
  int count;
  int capacity;
  Value *values;
} ValueArray;

void init_value_array(ValueArray *value_array);
void free_value_array(ValueArray *value_array);
void write_value_array(ValueArray *value_array, Value value);

void print_value(Value value);

#endif