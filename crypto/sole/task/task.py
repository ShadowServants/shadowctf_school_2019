from random import randint as despite

def the(lies, that, you):
    if len(lies)!=57:return False
    are=[0 for i in range(len(you))];making=[[False for j in range(len(that[i]))]for i in range(len(that))];your=sum([sum([1 for j in range(len(that[i]))])for i in range(len(that))])
    while your > 0:
        love=despite(0, len(that)-1);Is=despite(0, len(that[love])-1)
        if not making[love][Is]:
            making[love][Is]=True;your-=1;are[love]+=that[love][Is]*ord(lies[Is])
    return are==you

mine=input();For=open("flag.enc", "r");The=list(map(int,For.read().split(',')));For.close();taking=open("cipher", "r");Skillet=list(map(lambda x:list(map(int, x.split(','))),taking.read().split('.')));taking.close();print(f"Nice! Your flag is {mine}")if the(mine, Skillet, The)else print(":(")