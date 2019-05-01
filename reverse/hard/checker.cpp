#include <iostream>
#include <string.h>
#include <stdlib.h>
using namespace std;

//                              (
//                  .            )        )
//                           (  (|              .
//                       )   )\/ ( ( (
//               *  (   ((  /     ))\))  (  )    )
//             (     \   )\(          |  ))( )  (|
//             >)     ))/   |          )/  \((  ) \
//             (     (      .        -.     V )/   )(    (
//              \   /     .   \            .       \))   )) 
//                )(      (  | |   )            .    (  /
//               )(    ,'))     \ /          \( `.    )
//               (\>  ,'/__      ))            __`.  /
//              ( \   | /  ___   ( \/     ___   \ | ( (
//               \.)  |/  /   \__      __/   \   \|  ))
//              .  \. |>  \      | __ |      /   <|  /
//                   )/    \____/ :..: \____/     \ <
//            )   \ (|__  .      / ;: \          __| )  (
//           ((    )\)  ~--_     --  --      _--~    /  ))
//            \    (    |  ||               ||  |   (  /
//                  \.  |  ||_             _||  |  /
//                    > :  |  ~V+-I_I_I-+V~  |  : (.
//                   (  \:  T\   _     _   /T  : ./
//                    \  :    T^T T-+-T T^T    ;<
//                     \..`_       -+-       _'  )
//                        . `--=.._____..=--'. ./ 
//   ______     __                                           ______  
//  /      \   |  \                                         /      \ 
// |  $$$$$$\ _| $$_     ______    ______    ______        |  $$$$$$\
// | $$___\$$|   $$ \   |      \  /      \  /      \        \$$__| $$
//  \$$    \  \$$$$$$    \$$$$$$\|  $$$$$$\|  $$$$$$\       /      $$
//  _\$$$$$$\  | $$ __  /      $$| $$  | $$| $$    $$      |  $$$$$$ 
// |  \__| $$  | $$|  \|  $$$$$$$| $$__| $$| $$$$$$$$      | $$_____ 
//  \$$    $$   \$$  $$ \$$    $$ \$$    $$ \$$     \      | $$     \
//   \$$$$$$     \$$$$   \$$$$$$$ _\$$$$$$$  \$$$$$$$       \$$$$$$$$
//                               |  \__| $$                          
//                                \$$    $$                          
//                                 \$$$$$$                           

bool part1(char*flag){int*t=(int*)memfrob(flag,8);unsigned int b[]={3164519328,2997125270};
for(int i=0;i<2;b[i]=~b[i],++i){};return!(0<:t:>-0<:b:>+1<:t:>-1<:b:>);}int part2(char*flag){
int p[3][3]={ {93,96,87},{25,103,45},{96,102,59}};int pp[][3]={{flag[0],flag[1],flag[2]},{
flag[3],0x00000,flag[4]},{flag[5],flag[6],flag[7]}};int ppp[3][3]={{28611,16425,27948},{17896,
6555,17338},{27072,13905,26816}};int fff=0;for(int o0o=0;o0o<3;++o0o){for(int oo0=0;oo0<3;
++oo0){int OOO=0;for(int oO0=0;oO0<3;++oO0){OOO+=p[o0o][oO0]*pp[oO0][oo0];}ppp[o0o][oo0]-=OOO;
fff+=ppp[o0o][oo0];}}return !fff;}template<int q>struct st{enum{x=256*st<q-1>::x};};template<>
struct st<0>{enum{x=1};};bool part3(char*flag){unsigned long long h1=flag[7];h1=h1*st<1>::x+
flag[0];h1=h1*st<2>::x+flag[5];h1=h1*st<3>::x+flag[6];unsigned long long h2=flag[1];h2=h2*
st<1>::x+ flag[2];h2=h2*st<2>::x+flag[4];h2=h2*st<3>::x+flag[3];return h1==21498752183304270
&&h2==22873141751578743;}bool part4(char*flag){srand(0x1337);char k[]={'1','@','#','s','*',
'z','X','b'};for(int i=0;i<0x1337;++i){flag[rand()%8]^=k[rand()%8];}int t[]={120,3,95,54,16,
32,25,52};for(int i=0;i<8;++i){if(flag[i]!=t[i])return false;}return true;}bool check(char*
flag){return+part1(flag+0)+part2(flag+8)+part3(flag+16)+part4(flag+24)==4;}void run(){char
flag[256];operator>>(cin,flag);if((strlen(flag)==43||(cout<<"Wrong! Even size is not correct (•_• )"
<< endl,0))&&(strstr(flag,"shadowctf{")==flag||(cout<<"No No No"<<endl,0))&&(flag[42]=='}'||(cout<<
"Omg, no!\n",0))&&(check(flag+10)||(cout<<"Nope\n",0))){operator<<(clog, "YES\n");}}

int main() {
    run();
}
