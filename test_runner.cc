
// Defines function "ans" with an unspecified type that gets inspected in templates below
#include <test_function.inc>

#include <stdio.h>
#include <functional>
#include <utility>
template <typename T> struct function_traits;

template <typename R, typename... Args>
struct function_traits<std::function<R(Args...)>> {
    static constexpr size_t arity = sizeof...(Args);
    using ReturnType = R;
    using ArgTupleType = std::tuple<Args...>;
};

template <typename R, typename... Args>
struct function_traits<R (*)(Args...)> {
    static constexpr size_t arity = sizeof...(Args);
    using ReturnType = R;
    using ArgTupleType = std::tuple<Args...>;
};

template <typename F, typename ArgsArray, size_t... Indices>
auto my_invoke_helper(F&&f, ArgsArray&& aa, std::index_sequence<Indices...>) {
    return std::invoke(f, std::get<Indices>(aa)...);
}

template <typename F, typename ArgsArray, typename TupleType = function_traits<F>::ArgTupleType>
auto my_invoke(F&& f, ArgsArray&& aa) {
    return my_invoke_helper(f, aa, std::make_index_sequence<std::tuple_size_v<TupleType>>{});
}

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
    std::array<int, 32> inputs;
    playWithTheStack(argv[1]);
    for (int index = 1; index < argc; ++index) {
        inputs[index - 1] = atoi(argv[index]);
    }
    long output = my_invoke(&ans, inputs), my_invoke(&ans, inputs);
    printf("%lld\n", output);
    return 0;
}