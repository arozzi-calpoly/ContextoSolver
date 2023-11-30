import requests
from time import time

def format_second_duration(total_num_seconds):
    total_num_seconds = int(total_num_seconds)
    hours = total_num_seconds // 3600
    minutes = (total_num_seconds % 3600) // 60
    seconds = total_num_seconds % 60
    return f"{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

url = 'https://api.contexto.me/machado/en/game/436/'

words = open('wordsleft.txt', 'r').read().splitlines()
seen_good_words = open('api_good_words_so_far.txt', 'r').read().splitlines()
seen_bad_words = open('api_bad_words_so_far.txt', 'r').read().splitlines()

words = list(set(words) - set(seen_good_words) - set(seen_bad_words))

fbad = open("api_bad_words.txt", 'w+')
fgood = open("api_good_words.txt", 'w+')


start_time = time()
num_words = len(words)
for i, word in enumerate(words):
    word_url = url + word
    response = requests.get(url = word_url, timeout=(10, 30))
    try:
        data = response.json()
    except Exception:
        print("Got error decoding JSON. Response:")
        print(response.content)
        continue

    if 'error' in data:
        fbad.write(word + '\n')
    else:
        fgood.write(word + '\n')

    if i % 100 == 0:
        current_time = time()
        elapsed_time = current_time - start_time
        proportion_complete = i / num_words
        if proportion_complete == 0:
            continue
        estimated_total_time = elapsed_time / proportion_complete
        estimate_time_remaining = estimated_total_time - elapsed_time
        
        print(f"\r{i}/{num_words} words completed  -  {format_second_duration(estimate_time_remaining)} remaining    ", end='', flush=True)

fbad.close()
fgood.close()