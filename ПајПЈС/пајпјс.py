#ПајПЈС - Подударање језичких стилова у Пајтону

#Све је на ћирилици - осим кључних ријечи и неких ствари које се нису могле
#лако измијенити, као што је нпр. назив библиотеке functools или методе load у
#јасону. Док се неке кључне ријечи могу преименовати, нпр. штампај = print,
#друге се не могу, нпр. дефиниши = def неће радити, па су зато све кључне ријечи
#остављене у оригиналном облику.
import numpy as бројко
import spacy as свемирко
import json as јасон
from functools import reduce as смањи

with open("врсте.json") as датотека:
    све_врсте_ријечи = јасон.load(датотека)

опј = свемирко.load("en_core_web_sm")

def апсолутна_разлика(n1, n2):
    return 1 - (бројко.abs(n1 - n2) / (n1 + n2 + бројко.nextafter(0,1)))

def добиј_врсте_ријечи(текст):
    return [ријеч.tag_ for ријеч in опј(текст)]

def преброј(низ):
    бројач = {}
    for ставка in низ:
        бројач[ставка] = бројач.get(ставка, 0) + 1
    return бројач
    
def добиј_пропорције_в_р(текст):
    врсте_ријечи = добиј_врсте_ријечи(текст)
    број = преброј(врсте_ријечи)
    укупан_број = 0
    пропорције_в_р = {}
    
    for кључ,вриједност in број.items():
        укупан_број += вриједност
        пропорције_в_р[кључ] = број[кључ] / укупан_број

    return пропорције_в_р

def упореди_пропорције(п1, п2):
    сличност = [];
    for кључ in све_врсте_ријечи:
        if п1.get(кључ, None) is None or п2.get(кључ, None) is None:
            if п1.get(кључ, None) is None and п2.get(кључ, None) is None:
                continue
            else:
                сличност.append(0)
        elif п1[кључ] == п2[кључ]:
            сличност.append(1)
        else:
            тежина = бројко.abs(1 - ((п1[кључ] + п2[кључ])/2))
            разлика = апсолутна_разлика(п1[кључ], п2[кључ])
            сличност.append(разлика * тежина)
    if сличност:
        сума = смањи(lambda a, b: a + b, сличност)
        просјек = сума / len(сличност)
        return просјек
    else:
        return 0

def упореди_текстове (т1, т2):
    резултат = list(map(добиј_пропорције_в_р, [т1, т2]))
    return упореди_пропорције(резултат[0], резултат[1]);
