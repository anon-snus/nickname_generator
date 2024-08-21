import random
import os
import concurrent.futures

def get_unique_filename(directory: str, base_filename: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    base_path = os.path.join(directory, base_filename)
    filename, extension = os.path.splitext(base_path)
    counter = 1
    new_filename = f"{filename}{extension}"
    while os.path.exists(new_filename):
        new_filename = f"{filename}_{counter}{extension}"
        counter += 1
    return new_filename

def reading(file):
    with open(file, 'r') as f:
        words = f.read().splitlines()
    return words

def generate_nick(words):
    while True:
        wcount = random.randint(1, 3)
        ncount = random.randint(0, 3)
        selected_words = random.sample(words, wcount)
        selected_numbers = [str(random.randint(0, 2048)) for _ in range(ncount)]
        components = selected_words + selected_numbers
        random.shuffle(components)
        nickname = ''.join(components)
        if not nickname[0].isdigit() and len(nickname) > 7:
            return nickname

def generate_nicks_concurrently(words, number_of_nicks, max_workers=4):
    nicks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(generate_nick, words) for _ in range(number_of_nicks)]
        for future in concurrent.futures.as_completed(futures):
            nicks.append(future.result())
    return nicks

number = int(input('Number of nicknames: '))
file = 'words.txt'
words = reading(file)

results_dir = 'results'
output_file = get_unique_filename(results_dir, 'wallets.txt')

# Устанавливаем количество потоков в зависимости от числа ядер процессора
max_workers = os.cpu_count()

# Генерация никнеймов с использованием многопоточности
nicks = generate_nicks_concurrently(words, number, max_workers=max_workers)

# Запись результатов в файл
with open(output_file, 'w') as f:
    for nick in nicks:
        f.write(nick + '\n')
