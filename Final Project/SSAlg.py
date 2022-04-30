dict = {}
baseString = ""


def dictInit():
    global dict
    text_file = open("data/Dictionary/oxford_dictionary_words.txt", "r")
    lines = text_file.read().split('\n')
    text_file.close()
    dict = set(lines)


def sSpellAlg(word):
    global baseString
    string = ""
    arr = []
    for i in range(len(word)):
        pos = word[i]
        string = string + pos.pop(0)[1]
        for j in range(len(pos)):
            arr.append((pos[j][0], pos[j][1], i))

    baseString = string
    arr.sort(key=lambda x: x[0], reverse=True)
    result = spellCheck(string, arr)
    return result


def spellCheck(string, todo):
    if string in dict or not todo:
        return string
    else:
        return spellCheck(replaceNext(baseString, todo), todo)


def replaceNext(string, todo):
    if todo:
        newC = todo.pop(0)
        index = newC[2]
        newstring = newC[1]
        string = string[:index] + newstring + string[index + 1:]
        return string
    else:
        return string


dictInit()
