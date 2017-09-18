CC=cc

#common
CFLAGS=-O2 -g 

SRCS = xctopo.c \
		location.c

OBJS = 	$(SRCS:.c=.o)

TARGET = location.x

all:    $(TARGET)
		@echo Compilation done.

%.o:%.c
		$(CC) $(CFLAGS) -c $< -o $@ $(INC) $(LIBS) $(DEFINES)

$(TARGET): $(OBJS) 
		$(CC) $(CFLAGS) -o $(TARGET) $(OBJS) $(INC) $(LIBS) $(DEFINES)   

clean:
		$(RM) *.o *~

