#include <stdio.h>
int pop(int* bp, int** sp) {
    if (bp == *sp) {
        return 0;
    } else {
        return *--(*sp);
    }
}
long ans(char* filename) {
    char program[25][100];
    bzero(program, 25*100);
    FILE *fp = fopen(filename, "r");
    for (int i = 0;fgets(program[i], 100, fp);++i);
    int stack[99];
    int *sp = stack;
    int pc[2] = {0, 0};
    int dir[2] = {1, 0};
    while (1) {
        char op = program[pc[1]][pc[0]];
        if (strchr("+-*/%`\\", op)) {
            int a = pop(stack,&sp);
            int b = pop(stack,&sp);
            if (op == '\\') {
                *sp++ = a;
                *sp++ = b;
            } else {
                int v;
                if (op == '+') v = b + a;
                if (op == '-') v = b - a;
                if (op == '*') v = b * a;
                if (op == '%') v = b % a;
                if (op == '/') v = b / a;
                if (op == '`') v = b > a;
                *sp++ = v;
            }
        } 
        if (op == '<') dir[0]=-1,dir[1]=0;
        if (op == '>') dir[0]=1,dir[1]=0;
        if (op == '^') dir[0]=0,dir[1]=-1;
        if (op == 'v') dir[0]=0,dir[1]=1;
        if (isdigit(op)) *sp++ = op - '0';
        if (op == '_') dir[1]=0,dir[0]=pop(stack,&sp) ? -1 : 1;
        if (op == '|') dir[0]=0,dir[1]=pop(stack,&sp) ? -1 : 1;
        if (op == ':') {
            int x = pop(stack,&sp);
            *sp++ = x;
            *sp++ = x;
        }
        if (op == '$') pop(stack,&sp);
        if (op == '!') {int val = pop(stack,&sp); *sp++ = val==0; }
        if (op == '@') return pop(stack,&sp);
        pc[0] = (pc[0] + dir[0]) % 100;
        pc[1] = (pc[1] + dir[1]) % 25;
    }
}