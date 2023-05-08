#include <stdlib.h>
#include <string.h>

extern long ans();

// This function has no "real" side effects, but it is a function with a pretty big stack
// that writes semi-random values in an attempt to make the stack messy in case the passed in
// code attempts to read unitialized memory from the stack
unsigned char playWithTheStack(char* seed) {
    volatile unsigned char buffer[2048];
    char val = seed[0];
    for (int i = 0; i < sizeof(buffer); ++i) {
        val = val * 10159 % 1069;
        buffer[i] = val % 256;
    }
    return buffer[511];
}

int main(int argc, char** argv) {
    int inputs[32];
    for (int index = 1; index < argc; ++index) {
        inputs[index - 1] = atoi(argv[index]);
    }
    playWithTheStack(argv[1]);
    int output;
    if (argc == 2) {
        output = ans(inputs[0]);
    } else if (argc == 3) {
        output = ans(inputs[0], inputs[1]);
    }
    printf("%lld\n", output);
    return 0;
}