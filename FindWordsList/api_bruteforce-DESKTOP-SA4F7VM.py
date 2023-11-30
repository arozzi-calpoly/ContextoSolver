import requests

url = 'https://api.contexto.me/machado/en/game/436/'

words = open('words.txt', 'r').read().splitlines()

bad_words = []
good_words = []

i = 0
for word in words:
    i += 1
    print(f"\r{i} words completed       ", end='', flush=True)
    word_url = url + word
    r = requests.get(url = word_url)
    data = r.json()

    if 'error' in data:
        bad_words.append(word)
    else:
        good_words.append(word)

good_output = '\n'.join(good_words)
bad_output = '\n'.join(bad_words)

with open("api_bad_words.txt", 'w+') as f:
    f.write(bad_output)


with open("api_good_words.txt", 'w+') as f:
    f.write(good_output)