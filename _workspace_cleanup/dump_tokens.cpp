#include <iostream>
#include "frontend/lexer/lexer.h"
#include <fstream>

using namespace npk::frontend;

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    std::ifstream file(argv[1]);
    std::string source((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    Lexer lexer(source);
    auto tokens = lexer.tokenize();
    for (auto& t : tokens) {
        if (t.line == 59) {
            std::cout << "L" << t.line << ":" << t.column << " [" << t.lexeme << "] type=" << (int)t.type << "\n";
        }
    }
    return 0;
}
