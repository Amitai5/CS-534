import pickle
import random
import os

import tqdm

gen_types = 4
misspell_word_gen = 32


def gen_misspelled(gen_type, word):
    misspelled = ""
    replace_idx = random.randint(0, len(word) - 1)

    if gen_type == 0:  # Randomly swap letter
        replace_char = random.randint(0, 26) + 97
        misspelled = word[:replace_idx] + chr(replace_char) + word[replace_idx + 1:]
    elif gen_type == 1:  # Randomly double a letter
        misspelled = word[:replace_idx] + word[replace_idx] + word[replace_idx:]
    elif gen_type == 2:  # Randomly remove a letter
        misspelled = word[:replace_idx] + word[replace_idx + 1:]
    elif gen_type == 3:  # Randomly add a letter
        replace_char = random.randint(0, 26) + 97
        misspelled = word[:replace_idx] + chr(replace_char) + word[replace_idx:]
    return misspelled


def get_misspelled(gen_type, wordlist, word):
    misspelled = gen_misspelled(gen_type, word)

    # Ensure word does not already exist
    tries = 0
    while tries < 10 and wordlist.__contains__(misspelled):
        misspelled = gen_misspelled(gen_type, word)
        tries += 1

    if tries == 0:
        return misspelled
    return None


wordlist = set()
with open(os.curdir + "\\data\\Dictionary\\oxford_dictionary_words.txt") as file:
    for line in file:
        wordlist.add(line.rstrip("\n"))

misspelled_wordpairs = []
for word in tqdm.tqdm(wordlist):
    for i in range(misspell_word_gen):
        misspelled_word = get_misspelled(i % gen_types, wordlist, word)
        if misspelled_word is not None:
            misspelled_wordpairs.append([misspelled_word, word])

# Save the dataset
save_file = open(os.curdir + "\\data\\Dictionary\\misspelled_words_dataset.pkl", 'wb')
pickle.dump(misspelled_wordpairs, save_file)

print("Oxford Dictionary Dataset Count:", len(wordlist))
print("Misspelled Word Count: ", len(misspelled_wordpairs))
print("Percentage Not Generated: ", (len(misspelled_wordpairs) / len(wordlist)) / misspell_word_gen)
