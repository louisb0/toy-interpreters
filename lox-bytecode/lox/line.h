#ifndef lox_line_h
#define lox_line_h

typedef struct {
  int count;
  int capacity;
  int *lines;
  int *line_length;
} LineInfo;

void init_line_info(LineInfo *line_info);
void free_line_info(LineInfo *line_info);
void write_line_info(LineInfo *line_info, int line);

#endif
