# вывод ключей
data = response.json()
    ids = data.keys() #-> list с ключами
    for id in data:
        print(id)