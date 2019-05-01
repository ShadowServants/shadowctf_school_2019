#include <iostream>
#include <random>
#include <ctime>

int main() {

    srand(time(0));

    int pass = rand();

    std::cout << pass << "\n" << "1 2147483648\n";

    return 0;
}