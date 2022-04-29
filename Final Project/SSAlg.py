dict = {}
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
    X

dictInit()