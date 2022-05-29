# Генератором разбиваем список на равные части, по умочанию на 10 частей

def chunk_generator(lst, n=10):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]
