#include <iostream>
#include <vector>
using namespace std;

unsigned char flag[] = "shadowctf{r3al1y_reallY_well__played_game}";
vector<unsigned char> values;

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
    int rounds = 10000000;
    values.resize(rounds);

    int t = 1337;
    for (int i = 0; i < rounds; ++i) {
        values[i] = t % 256;
        t = t * 1103515245 + 12345;
    }

    for (int i = 0; i < rounds; ++i) {
        for (int k = 0; k < 42; ++k) {
            flag[k] ^= values[rounds - 1 - i];
            flag[k] = __ROL__(flag[k], -(k % 7));
        }
    }

    for (int i = 0; i < 42; ++i) {
        cout << (int) flag[i] << ", ";
    }
    cout << endl;

    return 0;
}
