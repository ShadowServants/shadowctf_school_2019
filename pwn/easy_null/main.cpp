#include <iostream>
#include <string>
#include <cstring>

int main() {
    const char *secret = getenv("SECRET");
    const char *flag = getenv("FLAG");

    if (secret == nullptr) {
        std::cout << "Secret not found";
        return 1;
    }

    if (flag == nullptr) {
        std::cout << "Flag not found";
        return 1;
    }

    std::string login;
    std::string password;

    std::cout << "Login: ";
    std::cin >> login;
    std::cout << "Password: ";
    std::cin >> password;

    if ((strcmp(login.c_str(), "admin") != 0) ||
        (strcmp((login + password).c_str(), (login + std::string(secret)).c_str()) != 0)) {
        std::cout << "Access denied" << std::endl;
    } else {
        std::cout << std::string(flag) << std::endl;
    }

    return 0;
}
