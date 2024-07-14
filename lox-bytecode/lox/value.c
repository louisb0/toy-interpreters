#include <stdio.h>

#include "memory.h"
#include "value.h"

void init_value_array(ValueArray *value_array) {
  assert(value_array != NULL);

  value_array->count = 0;
  value_array->capacity = 0;
  value_array->values = NULL;
}

void free_value_array(ValueArray *value_array) {
  assert(value_array != NULL);

  FREE_ARRAY(Value, value_array->values, value_array->capacity);
  init_value_array(value_array);
}

void write_value_array(ValueArray *value_array, Value value) {
  assert(value_array != NULL);

  if (value_array->capacity < value_array->count + 1) {
    int old_capacity = value_array->capacity;
    value_array->capacity = GROW_CAPACITY(old_capacity);
    value_array->values = GROW_ARRAY(Value, value_array->values, old_capacity,
                                     value_array->capacity);
  }

  value_array->values[value_array->count] = value;
  value_array->count++;
}

void print_value(Value value) { printf("%g", AS_NUMBER(value)); }
