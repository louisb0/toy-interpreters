#include "line.h"
#include "memory.h"

#include <stdio.h>

void init_line_info(LineInfo *line_info) {
  assert(line_info != NULL);

  line_info->count = 0;
  line_info->capacity = 0;
  line_info->lines = NULL;
}

void free_line_info(LineInfo *line_info) {
  assert(line_info != NULL);

  FREE_ARRAY(int, line_info->lines, line_info->capacity);
  init_line_info(line_info);
}

void write_line_info(LineInfo *line_info, int line) {
  assert(line_info != NULL);
  assert(line > 0);

  if (line_info->capacity < line_info->count + 2) {
    int old_capacity = line_info->capacity;
    line_info->capacity = GROW_CAPACITY(old_capacity);
    line_info->lines =
        GROW_ARRAY(int, line_info->lines, old_capacity, line_info->capacity);
  }

  if (line_info->count > 0 && line == line_info->lines[line_info->count - 2]) {
    line_info->lines[line_info->count - 1]++;
  } else {
    line_info->lines[line_info->count] = line;
    line_info->lines[line_info->count + 1] = 1;
    line_info->count += 2;
  }
}
