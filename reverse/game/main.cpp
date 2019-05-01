#include <SFML/Graphics.hpp>
#include <algorithm>
#include <string>
#include <iostream>
#include <stdlib.h>
using namespace sf;

/* Constants section */
const int WIDTH = 32;
const int HEIGHT = 20;
const int BLOCK_SIZE = 30;
const int PLAT_SIZE = 3;
const int JMP_SPEED = 1500;
const int PX_WIDTH = WIDTH * BLOCK_SIZE;
const int PX_HEIGHT = HEIGHT * BLOCK_SIZE;

/* Need to global */
int cur_dblock = WIDTH / 2;
std::vector<bool> vis(WIDTH, false);
int jmp_counter = 0;
int already_done = 0;
int total = 10000000;
unsigned char flag[42];
int next = 0;

void regen_vis(int pos = -1) {
    for (int i = 0; i < WIDTH; ++i) {
        vis[i] = false;
    }
    if (pos == -1) {
        cur_dblock = (rand() % (WIDTH - PLAT_SIZE + 1));
    } else {
        cur_dblock = pos;
    }
    for (int i = 0; i < PLAT_SIZE; ++i) {
        vis[cur_dblock + i] = true;
    }
}


int color(int x) {
    return -std::abs(-x + 256) + 256;
}

std::string get_status_line_string(bool all = false) {
    char buffer[50];
    if (all) snprintf(buffer, 50, "%d of %d jumps done", already_done, total);
    else snprintf(buffer, 50, "%d of %d", already_done, total);
    return std::string(buffer);
}


void init_flag() {
    next = 1337;
    unsigned char init[42] = {
        243, 108, 65, 101, 103, 55, 97, 244, 98, 91, 115, 59, 33, 110,
        177, 125, 127, 115, 109, 33, 110, 236, 93, 127, 118, 109, 44,
        110, 223, 91, 80, 109, 105, 57, 103, 228, 91, 71, 96, 101, 37, 127
    };
    for (int i = 0; i < 42; ++i) {
        flag[i] = init[i];
    }
}

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

void flag_round() {
    for (int i = 0; i < 42; ++i) {
        flag[i] = __ROL__(flag[i], i % 7);
        flag[i] ^= (next % 256);
    }
    next = next * 1103515245 + 12345;
}

std::string get_flag() {
    char *data = reinterpret_cast<char*>(flag);
    return std::string(data, 42);
}

class Kolobok {
private:
    int sign(double value) {
        if (value > 0) return 1;
        else if (value == 0) return 0;
        return -1;
    }

    Rect<float> make_drect(float dx, float dy) {
        float left = this->sprite.getGlobalBounds().left;
        float top = this->sprite.getGlobalBounds().top;
        float width = this->sprite.getGlobalBounds().width;
        float height = this->sprite.getGlobalBounds().height;
        return Rect<float>(left + dx, top + dy, width, height);
    }

    float abs_min(float a, float b) {
        if (std::abs(a) < std::abs(b)) {
            return a;
        }
        return b;
    }

public:
    Texture texture;
    Sprite sprite;
    float down_speed;

    Kolobok(const std::string& filename) {
        this->texture.loadFromFile(filename);
        this->sprite.setTexture(this->texture);
        this->down_speed = 0;
    }

    void move(double dx, double dy, std::vector<Sprite>& objects) {
        float rdx = dx, rdy = dy;
        auto my_rect = this->sprite.getGlobalBounds();
        for (int i = 0; i < objects.size(); ++i) {
            auto &obj = objects[i];
            auto obj_rect = obj.getGlobalBounds();
            if (obj_rect.intersects(make_drect(dx, 0))) {
                if (dx > 0) {
                    rdx = abs_min(obj_rect.left - (my_rect.left + my_rect.width), rdx);
                } else {
                    rdx = abs_min(obj_rect.left + obj_rect.width - my_rect.left, rdx);
                }
            } else {
                rdx = abs_min(dx, rdx);
            }
            if (obj_rect.intersects(make_drect(0, dy)) && vis[i]) {
                if (dy > 0) {
                    rdy = abs_min(obj_rect.top - (my_rect.top + my_rect.height), rdy);
                } else {
                    rdy = abs_min(obj_rect.top + obj_rect.height - my_rect.top, rdy);
                }

                regen_vis();
                this->down_speed = -JMP_SPEED;
                ++already_done;
                flag_round();
                jmp_counter = 0;
            } else {
                rdy = abs_min(dy, rdy);
            }
        }
        this->sprite.move(rdx, rdy);
    }

    void gravity(float dt, std::vector<Sprite>& objects) {
        this->down_speed += 30;
        this->move(0, down_speed * dt, objects);
    }
};


int main() {
    srand(time(0));
    RenderWindow window(sf::VideoMode(BLOCK_SIZE * WIDTH, BLOCK_SIZE * HEIGHT), "Hellfire");

    Font font;
    font.loadFromFile("res/death.ttf");

    Font ubuntu;
    ubuntu.loadFromFile("res/ubuntu.ttf");

    Text text;
    text.setFont(font);
    text.setString("Hellfire");
    text.setCharacterSize(100);
    text.setFillColor(Color::White);
    auto start_x = (PX_WIDTH - text.getLocalBounds().width) / 2;
    text.setPosition(start_x + 20, 100);

    Text press_enter;
    press_enter.setString("Press enter to start");
    press_enter.setFont(ubuntu);
    press_enter.setCharacterSize(25);
    start_x = (PX_WIDTH - press_enter.getLocalBounds().width) / 2;
    press_enter.setPosition(start_x, 300);
    int cc = 0;

    Text shadow_ctf;
    shadow_ctf.setString("ShadowCTF 2019");
    shadow_ctf.setFont(ubuntu);
    shadow_ctf.setCharacterSize(15);
    shadow_ctf.setFillColor(Color::White);
    shadow_ctf.setPosition(10, (HEIGHT - 1) * BLOCK_SIZE);

    Texture fire_texture;
    fire_texture.loadFromFile("res/fire.png");
    int fire_counter = 0;

    Clock clock;
    auto kolobok = Kolobok("res/kolobok.png");

    Texture wall_texture;
    wall_texture.loadFromFile("res/ground.png");

    std::vector<Sprite> fires(WIDTH / 4);
    for (int i = 0; i < WIDTH / 4; ++i) {
        fires[i].setTexture(fire_texture);
        fires[i].setPosition(4 * BLOCK_SIZE * i, (HEIGHT - 4) * BLOCK_SIZE);
    }

    std::vector<Sprite> walls;
    for (int i = 0; i < WIDTH; ++i) {
        Sprite bottom;
        bottom.setTexture(wall_texture);
        bottom.setPosition(BLOCK_SIZE * i, (HEIGHT - 5) * BLOCK_SIZE);
        walls.push_back(bottom);
    }
    
    for (int i = 0; i < HEIGHT - 4; ++i) {
        Sprite left, right;
        left.setTexture(wall_texture);
        right.setTexture(wall_texture);
        left.setPosition(-BLOCK_SIZE, BLOCK_SIZE + BLOCK_SIZE * i);
        right.setPosition(WIDTH * BLOCK_SIZE, BLOCK_SIZE + BLOCK_SIZE * i);
        walls.push_back(left);
        walls.push_back(right);
    }

    Texture one_more;
    one_more.loadFromFile("res/rzumen.png");
    Sprite rzumen;
    rzumen.setTexture(one_more);
    auto rz_start = (PX_WIDTH - rzumen.getLocalBounds().width) / 2;
    rzumen.setPosition(rz_start, 150);

    Text status_line;
    status_line.setFont(ubuntu);
    status_line.setCharacterSize(20);
    status_line.setPosition(10, 5);
    status_line.setString("");

    float dt = 0;
    float rrr = 0;

menu:
    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }
        }

        if (Keyboard::isKeyPressed(Keyboard::Enter)) { break; }

        int cur_color = color(cc);
        cc = (cc + 1) % 512;
        press_enter.setFillColor(Color(cur_color, cur_color, cur_color));

        window.clear(Color::Black);

        for (int i = 0; i < WIDTH / 4; ++i) {
            fires[i].setTextureRect(Rect<int>(BLOCK_SIZE * 4 * (fire_counter / 4), 0, BLOCK_SIZE * 4, BLOCK_SIZE * 4));
            window.draw(fires[i]);
        }
        fire_counter = (fire_counter + 1) % (64 * 4);

        window.draw(text);
        window.draw(press_enter);
        window.draw(shadow_ctf);
        window.display();
        sleep(milliseconds(4));
    }

    kolobok.sprite.setPosition((WIDTH / 2) * BLOCK_SIZE, BLOCK_SIZE * 3);
    kolobok.down_speed = 0;
    jmp_counter = 0;
    already_done = 0;
    regen_vis(WIDTH / 2 - 1);
    init_flag();
 
    while (window.isOpen()) {
        Time elapsed = clock.getElapsedTime();
        clock.restart();

        if (already_done >= total) {
            goto win;
        }

        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }
        }

        // kolobok movement control block
        {
            auto pos = kolobok.sprite.getPosition();
            dt += elapsed.asSeconds();
            kolobok.gravity(elapsed.asSeconds(), walls);

            if (pos.y >= (HEIGHT - 1) * BLOCK_SIZE) {
                goto endgame;
            }

            if (Keyboard::isKeyPressed(Keyboard::Space)) {
                if (jmp_counter < 2 && dt > 0.5) {
                    kolobok.down_speed = -JMP_SPEED;
                    ++jmp_counter;
                    dt = 0;
                }
            }
            if (Keyboard::isKeyPressed(Keyboard::Left))  { kolobok.move(-4,  0, walls); } 
            if (Keyboard::isKeyPressed(Keyboard::Right)) { kolobok.move( 4,  0, walls); }
        }
        
        window.clear(Color::Black);

        for (int i = 0; i < WIDTH / 4; ++i) {
            fires[i].setTextureRect(Rect<int>(BLOCK_SIZE * 4 * (fire_counter / 4), 0, BLOCK_SIZE * 4, BLOCK_SIZE * 4));
            window.draw(fires[i]);
        }
        fire_counter = (fire_counter + 1) % (64 * 4);


        for (int i = 0; i < WIDTH; ++i) {
            if (vis[i]) {
                window.draw(walls[i]);
            }
        }
        for (int i = WIDTH; i < walls.size(); ++i) {
            window.draw(walls[i]);
        }

        status_line.setString(get_status_line_string());
        window.draw(status_line);
        window.draw(kolobok.sprite);
        
        window.display();
        sleep(milliseconds(4));
    }
    goto finish_label;

endgame:
    status_line.setString(get_status_line_string(true));
    rrr = (PX_WIDTH - status_line.getLocalBounds().width) / 2;
    status_line.setPosition(rrr - 10, 400);

    for (int t = 0; t < 400 && window.isOpen(); ++t) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }
        }

        window.clear(Color::Black);
        window.draw(rzumen);
        for (int i = 0; i < WIDTH / 4; ++i) {
            fires[i].setTextureRect(Rect<int>(BLOCK_SIZE * 4 * (fire_counter / 4), 0, BLOCK_SIZE * 4, BLOCK_SIZE * 4));
            window.draw(fires[i]);
        }
        fire_counter = (fire_counter + 1) % (64 * 4);

        
        window.draw(status_line);

        window.display();
        sleep(milliseconds(4));
    }
    status_line.setPosition(10, 5);

    goto menu;

win:
    status_line.setString(get_flag());
    rrr = (PX_WIDTH - status_line.getLocalBounds().width) / 2;
    status_line.setPosition(rrr - 10, 400);

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }
        }

        window.clear(Color::Black);
        window.draw(rzumen);

        for (int i = 0; i < WIDTH / 4; ++i) {
            fires[i].setTextureRect(Rect<int>(BLOCK_SIZE * 4 * (fire_counter / 4), 0, BLOCK_SIZE * 4, BLOCK_SIZE * 4));
            window.draw(fires[i]);
        }
        fire_counter = (fire_counter + 1) % (64 * 4);
        window.draw(status_line);

        window.display();
        sleep(milliseconds(4));
    }

finish_label:
    return 0;
}
