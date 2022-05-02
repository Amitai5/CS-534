import copy


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
    # [ [ ( float, char ), ( float, char ) ] [ ( float, char ), ( float, char ) ] ]
    # [ [ ( float, char ) ] ]
    # List of positions where each position has a list of ordered pairs where each order pair contains a
    # float percentage and a char value
    # eg = [[(1, 'a'), (.87, 'b'), (.32, 'c')], [(1, 'e'), (.62, 'f')], [(1, 'g'), (.33, 'h')]]
    # need to all be lowercase
    string = ""
    arr = [(1, "")]
    print(word)
    # new struct: [(.00, "string")]

    for i in range(len(word)):
        # pos = word[i]
        arr = addlettercombo(arr, word[i])
        # string = string + pos.pop(0)[1]

    # print(string)
    # baseString = string
    arr.sort(key=lambda x: x[0], reverse=True)
    print(arr)
    default = arr[0]
    result = spellCheck(arr)
    if result is None:
        print("no alternative found")
        result = default
    print("result: ", result[1])
    print("prob: ", result[0])
    return result[1]



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
            newstr = copy.deepcopy(arr[i])
            nprob = arr[i][0]
            nstr = arr[i][1]
            print("newstr: ", newstr)
            print("c: ", c)
            print("c[j]: ", c[j])
            # newstr[0] = newstr[0] * c[j][0]
            # newstr[1] = newstr[1] + c[j][1]
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


eg = [[(1, 'e'), (.34, 'a'), (.32, 'b')], [(1, 'e'), (.62, 'x')], [(1, 't'), (.33, 'g')]]

sSpellAlg(eg)

