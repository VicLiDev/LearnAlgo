###############################################################################
# 通用 多目标 + 子目录 Makefile Demo
###############################################################################

# 工作目录
WK_DIR       := $(CURDIR)
CUR_MKF_FILE := $(lastword $(MAKEFILE_LIST))
CUR_MKF_DIR  := $(dir $(CUR_MKF_FILE))

# 打印信息
$(info [WorkDir]  $(WK_DIR))
$(info [Makefile] $(CUR_MKF_FILE))
$(info [Mkf Dir ] $(CUR_MKF_DIR))

###############################################################################
# 基本设置
###############################################################################

CC      := g++
CFLAGS  := -Wall -Wextra
MCRODEF := -DMCRO_DEMO -DMCRO_DEMO2=\"mcro2\"

# 通用 include / lib 目录（可被所有 target 使用）
INCLUDE_DIRS := $(CUR_MKF_DIR)/include \
				/usr/local/include \
				/usr/local/include/opencv4

LIB_DIRS := $(CUR_MKF_DIR)/lib \
			/usr/local/lib

LIBS := m \
		pthread \
		opencv_core \
		opencv_surface_matching \
		opencv_imgproc \
		opencv_highgui \
		opencv_flann

# 转换为命令行形式
CPPFLAGS += $(addprefix -I, $(INCLUDE_DIRS))
LDFLAGS  += $(addprefix -L, $(LIB_DIRS))
LDLIBS   += $(addprefix -l, $(LIBS))

###############################################################################
# 目录与目标定义
###############################################################################

# 源码目录（如果以后你想放到 src/ 可直接改这里）
SRC_DIR := $(CUR_MKF_DIR)

# 要生成的可执行文件
TARGETS := $(CUR_MKF_DIR)/ppf_demo_gpt \
		   $(CUR_MKF_DIR)/ppf_load_match \
		   $(CUR_MKF_DIR)/ppf_normal_computation

###############################################################################
# 每个可执行文件的源文件定义
###############################################################################

SRC_DEMO := $(CUR_MKF_DIR)/src/ppf_demo_gpt.cpp
OBJ_DEMO := $(SRC_DEMO:.cpp=.o)

SRC_DEMO2 := $(CUR_MKF_DIR)/src/ppf_load_match.cpp
OBJ_DEMO2 := $(SRC_DEMO2:.cpp=.o)

SRC_DEMO3 := $(CUR_MKF_DIR)/src/ppf_normal_computation.cpp
OBJ_DEMO3 := $(SRC_DEMO3:.cpp=.o)

###############################################################################
# 伪目标
###############################################################################

.PHONY: all clean

all: $(TARGETS)

###############################################################################
# 链接规则（每个可执行文件独立配置）
###############################################################################
$(CUR_MKF_DIR)/ppf_demo_gpt: $(OBJ_DEMO)
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

$(CUR_MKF_DIR)/ppf_load_match: $(OBJ_DEMO2)
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

$(CUR_MKF_DIR)/ppf_normal_computation: $(OBJ_DEMO3)
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

###############################################################################
# 通用编译规则（使用 pattern rule）
###############################################################################

# 将所有 .c 编译成 .o

%.o: %.c
	$(CC) $(CFLAGS) $(CPPFLAGS) $(MCRODEF) -c $< -o $@

###############################################################################
# 运行测试
###############################################################################
.PHONY: tests
tests: $(TARGETS)
	@echo "=== Running all tests ==="
	@for t in $(TARGETS); do \
		echo "-- Running $$t"; \
		$$t; \
		echo ""; \
	done

###############################################################################
# 清理
###############################################################################

clean:
	$(RM) $(OBJ_DEMO) $(OBJ_DEMO2) $(OBJ_DEMO3)
	$(RM) $(TARGETS)

