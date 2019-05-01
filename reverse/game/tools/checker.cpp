#include <iostream>
#include <string>
using namespace std;


unsigned char flag[42] = {
    243, 108, 65, 101, 103, 55, 97, 244, 98, 91, 115, 59, 33, 110,
    177, 125, 127, 115, 109, 33, 110, 236, 93, 127, 118, 109, 44,
    110, 223, 91, 80, 109, 105, 57, 103, 228, 91, 71, 96, 101, 37, 127
};


template<class T>
inline T __ROL__(T value, int count) {
    const uint nbits = sizeof(T) * 8;
    if (count > 0) {
        count %= nbits;
        T high = value >> (nbits - count);
        if (T(-1) < 0) {
            high &= ~((T(-1) << count));
        }
        value <<= count;
        value |= high;
    } else {
        count = -count % nbits;
        T low = value << (nbits - count);
        value >>= count;
        value |= low;
    }
    return value;
}


int main() {
    int next = 1337;
    for (int i = 0; i < 10000000; ++i) {
        for (int i = 0; i < 42; ++i) {
            flag[i] = __ROL__(flag[i], i % 7);
            flag[i] ^= (next % 256);
        }
        next = next * 1103515245 + 12345;
    }

    cout << std::string(reinterpret_cast<char*>(flag), 42) << endl;

    return 0;
}
