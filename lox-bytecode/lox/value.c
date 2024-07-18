#include <stdio.h>
#include <string.h>

#include "memory.h"
#include "object.h"
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

void print_value(Value value) {
  switch (value.type) {
  case VAL_NIL:
    printf("nil");
    break;
  case VAL_BOOL:
    printf(AS_BOOL(value) ? "true" : "false");
    break;
  case VAL_NUMBER:
    printf("%g", AS_NUMBER(value));
    break;
  case VAL_OBJ:
    print_object(value);
    break;
  }
}

bool values_equal(Value a, Value b) {
  if (a.type != b.type) {
    return false;
  }

  switch (a.type) {
  case VAL_NIL:
    return true;
  case VAL_BOOL:
    return AS_BOOL(a) == AS_BOOL(b);
  case VAL_NUMBER:
    return AS_NUMBER(a) == AS_NUMBER(b);
  case VAL_OBJ: {
    ObjString *a_string = AS_STRING(a);
    ObjString *b_string = AS_STRING(b);
    return a_string->length == b_string->length &&
           memcmp(a_string->chars, b_string->chars, a_string->length) == 0;
  }
  default:
    assert(!"Unreachable");
    return false;
  }
}
