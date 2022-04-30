dict = {}
baseString = ""


def dictInit():
    global dict
    text_file = open("data/Dictionary/oxford_dictionary_words.txt", "r")
    # lines = text_file.readlines()
    lines = text_file.read().split('\n')
    print(lines)
    print(len(lines))
    text_file.close()
    # dict.add(lines)
    dict = set(lines)
    print(dict)


def sSpellAlg(word):
    global baseString
    # [ [ ( float, char ), ( float, char ) ] [ ( float, char ), ( float, char ) ] ]
    # [ [ ( float, char ) ] ]
    # List of positions where each position has a list of ordered pairs where each order pair contains a
    # float percentage and a char value
    # eg = [[(1, 'a'), (.87, 'b'), (.32, 'c')], [(1, 'e'), (.62, 'f')], [(1, 'g'), (.33, 'h')]]
    string = ""
    arr = []
    print(word)
    for i in range(len(word)):
        pos = word[i]
        string = string + pos.pop(0)[1]
        for j in range(len(pos)):
            arr.append((pos[j][0], pos[j][1], i))


    print(string)
    baseString = string
    arr.sort(key=lambda x: x[0], reverse=True)
    print(arr)
    result = spellCheck(string, arr)
    print("result: ", result)
    return result


def spellCheck(string, todo):
    if string in dict or not todo:
        return string
    else:
        return spellCheck(replaceNext(baseString, todo), todo)


def replaceNext(string, todo):
    if todo:
        newC = todo.pop(0)
        print("NewC: ", newC)
        index = newC[2]
        newstring = newC[1]
        string = string[:index] + newstring + string[index + 1:]
        print(string)
        return string
    else:
        return string


dictInit()

eg = [[(1, 'a'), (.34, 'b'), (.32, 'c')], [(1, 'e'), (.62, 'f')], [(1, 'g'), (.33, 'h')]]

sSpellAlg(eg)