CXX = g++
CXXSTD = c++17
CXXFLAGS = -std=$(CXXSTD) -Wall -Wextra -O2

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=.o)

TARGET = metadata.a

all: $(TARGET)

$(TARGET): $(OBJS)
	ar rcs $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Target to clean up compiled binaries and object files
clean:
	rm -f $(OBJS) $(TARGET)
