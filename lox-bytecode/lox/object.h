#ifndef lox_object_h
#define lox_object_h

#include "common.h"
#include "value.h"

#define OBJ_TYPE(value) (AS_OBJECT(value)->type)

#define IS_STRING(value) is_obj_type(value, OBJ_STRING)

#define AS_STRING(value) ((ObjString *)AS_OBJ(value))
#define AS_CSTRING(value) ((ObjString *)AS_OBJ(value)->chars)

typedef enum ObjType {
  OBJ_STRING,
} ObjType;

struct Obj {
  ObjType type;
};

struct ObjString {
  Obj obj;
  int length;
  char *chars;
};

static inline bool is_obj_type(Value value, ObjType type) {
  return IS_OBJ(value) && AS_OBJ(value)->type == type;
}

#endif
