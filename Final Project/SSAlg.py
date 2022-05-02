baseString = ""
dict = {}


def dictInit():
    global dict
    text_file = open("data/Dictionary/oxford_dictionary_words.txt", "r")
    lines = text_file.read().split('\n')

    text_file.close()
    dict = set(lines)


def sSpellAlg(word):
    global baseString
    arr = [(1, "")]

    for i in range(len(word)):
        arr = addlettercombo(arr, word[i])

    arr.sort(key=lambda x: x[0], reverse=True)
    default = arr[0]
    result = spellCheck(arr)

    if result is None:
        result = default
    return result[1], result[0]


def spellCheck(todo):
    string = todo.pop(0)
    if string[1] in dict:
        return string
    elif not todo:
        return None
    else:
        return spellCheck(todo)


def addlettercombo(arr, c):
    newarr = []
    for i in range(len(arr)):
        for j in range(len(c)):
            nprob = arr[i][0]
            nstr = arr[i][1]
            nprob = nprob * c[j][0]
            nstr = nstr + c[j][1]
            if nprob > .01:  # cutoff threshold
                newarr.append((nprob, nstr))
    return newarr


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
