#include <stdlib.h>
#include <string.h>

extern long ans();

int main(int argc, char** argv) {
    int inputs[32];
    for (int i = 1; i < argc; ++i) {
        inputs[i - 1] = atoi(argv[i]);
    }
    int output;
    if (argc == 2) {
        output = ans(inputs[0]);
    } else if (argc == 3) {
        output = ans(inputs[0], inputs[1]);
    }
    printf("%lld\n", output);
    return 0;
}