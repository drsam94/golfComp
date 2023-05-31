
// Defines function "ans" with an unspecified type that gets inspected in templates below
#include <string>
#include <vector>
using std::string;
using std::vector;
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

namespace std {
std::string to_string(const std::string& s) {
    return s;
}
}
template <typename F, typename ArgsArray, size_t... Indices>
std::string my_invoke_helper(F&&f, ArgsArray&& aa, std::index_sequence<Indices...>) {
    return std::to_string(std::invoke(f, std::get<Indices>(aa)...));
}

template <typename F, typename ArgsArray, typename TupleType = typename function_traits<F>::ArgTupleType>
std::string my_invoke(F&& f, ArgsArray&& aa) {
    return my_invoke_helper(f, aa, std::make_index_sequence<std::tuple_size_v<TupleType>>{});
}

template <typename ArgsArray>
std::string my_invoke(long (*f)(std::vector<int>), ArgsArray&& aa) {
    std::vector<int> in;
    for (auto elem : aa) {
        if (std::string(elem) == "I") {
            break;
        }
        in.push_back(elem);
    }
    return std::to_string(f(in));
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

/// A very hacky class for providing int or str inputs to the `ans` function
class IntOrStr {
    char* s;
  public:
    IntOrStr()=default;
    IntOrStr(const IntOrStr&) = default;
    IntOrStr(char* str) : s{str} {}

    operator int() const {
        return atoi(s);
    }
    operator std::string() const {
        return std::string{s};
    }
};

int main(int argc, char** argv) {
    std::array<IntOrStr, 32> inputs;
    playWithTheStack(argv[1]);
    for (int index = 1; index < argc; ++index) {
        inputs[index - 1] = argv[index];
    }
    std::string output = my_invoke(&ans, inputs);
    output = my_invoke(&ans, inputs);
    printf("%s", output.c_str());
    return 0;
}