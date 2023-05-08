CC=gcc
CXX=g++

REL_PATH = ../DRAMsim3

FMT_LIB_DIR= $(REL_PATH)/ext/fmt/include
INI_LIB_DIR= $(REL_PATH)/ext/headers
JSON_LIB_DIR=$(REL_PATH)/ext/headers
ARGS_LIB_DIR=$(REL_PATH)/ext/headers

INC=-I $(REL_PATH)/src/ -I$(FMT_LIB_DIR) -I$(INI_LIB_DIR) -I$(ARGS_LIB_DIR) -I$(JSON_LIB_DIR) -I /usr/include/python3.8
CXXFLAGS= -Wall -c -O3 -fPIC -std=c++11 $(INC) -DFMT_HEADER_ONLY=1


SRCS = $(REL_PATH)/src/bankstate.cc     $(REL_PATH)/src/channel_state.cc \
	   $(REL_PATH)/src/command_queue.cc $(REL_PATH)/src/common.cc \
	   $(REL_PATH)/src/configuration.cc $(REL_PATH)/src/controller.cc \
	   $(REL_PATH)/src/hmc.cc           $(REL_PATH)/src/dram_system.cc \
	   $(REL_PATH)/src/refresh.cc \
	   $(REL_PATH)/src/simple_stats.cc  $(REL_PATH)/src/timing.cc

RUNT = bankstate.o channel_state.o command_queue.o common.o \
		configuration.o controller.o hmc.o dram_system.o\
		refresh.o simple_stats.o timing.o


OBJECTS = $(addsuffix .o, $(basename $(SRCS)))
EXE_OBJS := $(OBJECTS)



all: _memory_system.so
	python moduletest.py

_memory_system.so: memory_system_wrap.o
	g++ -shared memory_system.o memory_system_wrap.o $(RUNT) -o _memory_system.so

memory_system_wrap.o: memory_system_wrap.cxx
	g++ $(CXXFLAGS) $(REL_PATH)/src/memory_system.cc memory_system_wrap.cxx $(SRCS)

memory_system_wrap.cxx:
	swig -python -c++ memory_system.i

clean:
	rm -f $(RUNT) memory_system_wrap.cxx memory_system_wrap.c memory_system.py memory_system.o _memory_system.so memory_system_wrap.o


