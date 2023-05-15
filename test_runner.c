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
    long output;
    long checkOutput;
    if (argc == 2) {
        if (isdigit(argv[1][0])) {
            output = ans(inputs[0]);
            checkOutput = ans(inputs[0]);
        } else {
            output = ans(argv[1]);
            checkOutput = ans(argv[1]);
        }
    } else if (argc == 3) {
        output = ans(inputs[0], inputs[1]);
        checkOutput = ans(inputs[0], inputs[1]);
    } else if (argc == 4 && argv[3][0] == 'S') {
        // heap allocate our 'buffer' to not disturb the prior stack manipulation
        // maybe also corrupt this?
        char* buf = malloc(1024);
        buf[1023] = '\0';
        ans(argv[1], inputs[1], buf);
        printf("%s", buf);
        return 0;
    }
    if (output != checkOutput) {
        printf("FAILED: got two different results: %lld, %lld", output, checkOutput);
        return 1;
    }
    printf("%ld", output);
    return 0;
}