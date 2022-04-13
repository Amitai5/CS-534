import pickle
import random
import os

import tqdm


def generate_misspelled_word(wordlist, word):
    replace_char = random.randint(0, 26) + 97
    replace_indx = random.randint(0, len(word) - 1)
    misspelled = word[:replace_indx] + chr(replace_char) + word[replace_indx+1:]

    # Ensure word does not already exist
    while misspelled in wordlist:
        replace_char = random.randint(0, 26) + 97
        replace_indx = random.randint(0, len(word) - 1)
        misspelled = word[:replace_indx] + chr(replace_char) + word[replace_indx+1:]
    return misspelled


wordlist = []
with open(os.curdir + "\\data\\Dictionary\\oxford_dictionary_words.txt") as file:
    wordlist = [line.rstrip("\n") for line in file]


misspell_word_gen = 15
misspelled_wordpairs = []
for word in tqdm.tqdm(wordlist):
    for i in range(misspell_word_gen):
        misspelled_word = generate_misspelled_word(wordlist, word)
        misspelled_wordpairs.append([misspelled_word, word])

# Save the dataset
pickle.dump(os.curdir + "\\data\\Dictionary\\misspelled_words_dataset.pkl")

print("Oxford Dictionary Dataset Count:", len(wordlist))
print("Misspelled Word Count: ", len(misspelled_wordpairs))