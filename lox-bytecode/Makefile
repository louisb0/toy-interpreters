CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g
DEPFLAGS = -MMD -MP

SRC_DIR = .
LOX_DIR = ./lox
OBJ_DIR = obj

MAIN_SRCS = $(wildcard $(SRC_DIR)/*.c)
LOX_SRCS = $(wildcard $(LOX_DIR)/*.c)

MAIN_OBJS = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(MAIN_SRCS))
LOX_OBJS = $(patsubst $(LOX_DIR)/%.c, $(OBJ_DIR)/%.o, $(LOX_SRCS))

OBJS = $(MAIN_OBJS) $(LOX_OBJS)

DEPS = $(OBJS:.o=.d)

TARGET = clox

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(DEPFLAGS) -c $< -o $@

$(OBJ_DIR)/%.o: $(LOX_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(DEPFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

clean:
	rm -rf $(OBJ_DIR) $(TARGET)

-include $(DEPS)

.PHONY: all clean
