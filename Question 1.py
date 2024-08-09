import json
import string
from collections import Counter
from itertools import repeat

def def_word_cnt(text):
  words = text.translate(str.maketrans('', '', string.punctuation)).lower().split()
  word_counts = dict(Counter(words))
  return word_counts

def write_to_json(word_counts, file_name):
  with open(file_name, 'w') as f:
    json.dump(word_counts, f)

# Create file names 
file_names = [f"result_{i+1}.json" for i in range(100)]

# Write word counts to JSON files 
list(map(lambda f: write_to_json(word_counts.copy(), f), file_names))
