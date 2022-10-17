# вариант №6: рюкзак 3х3, болеет астмой => антидот, 15 очков выживания на старте

stuff_dict = {
    'в': (3, 25), 'п': (2, 15), 'б': (2, 15), 'а': (2, 20),
    'и': (1, 5), 'н': (1, 15), 'т': (3, 20), 'о': (1, 25),
    'ф': (1, 15), 'д': (1, 10), 'к': (2, 20), 'р': (2, 20)
}

# высчитываем количество очков выживания при отсутствии всех предметов
# и со стартовым количеством очков в соответствии с моим вариантом
points = -sum(v for _, v in stuff_dict.values()) + 15


def get_memtable(sd, max_w):
    items = list(sd.items())
    # пустой массив, содержащий на каждой позиции пару из списка
    # предметов и количества очков для этого списка предметов
    V = [[([], points) for _ in range(max_w + 1)] for _ in range(len(items) + 1)]

    for i in range(1, len(items) + 1):
        for j in range(1, max_w + 1):
            # начинаем с единиц, т.к. при i = 0 или j = 0 список не заполняется

            item = items[i - 1]
            n, w, v = item[0], item[1][0], item[1][1]

            # реализация алгоритма с заполнением каждой ячейки таблицы
            if w > j:
                V[i][j] = V[i - 1][j]
            else:
                # удвоенная ценность компенсирует минус в очках выживания
                V[i][j] = max(V[i - 1][j], (V[i - 1][j - w][0] + [n], V[i - 1][j - w][1] + v * 2), key=lambda x: x[1])
    return V


memtable = get_memtable(stuff_dict, 9)  # заполняем таблицу для 9 ячеек рюкзака
optimal = list(memtable[-1][-1])  # оптимальное решение — последняя ячейка таблицы
if 'д' not in optimal[0]:  # проверяем, не лежит ли уже необходимый астматику антидот в рюкзаке
    # если нет, то выбираем самый дешёвый по очкам предмет, занимающий одну позицию, и заменяем его на антидот
    item_to_replace = min(list(filter(lambda i: stuff_dict[i][0] == 1, optimal[0])), key=lambda i: stuff_dict[i][1])
    optimal[1] = optimal[1] - stuff_dict[item_to_replace][1] * 2 + stuff_dict['д'][1] * 2
    optimal[0].remove(item_to_replace)
    optimal[0].append('д')


# сортируем предметы по весу, чтобы правильно собрать рюкзак
optimal[0].sort(key=lambda i: stuff_dict[i][0], reverse=True)

# формируем распределение индексов для сборки рюкзака
# сначала идут индексы предметов, занимающих 3 ячейки, потом 2, потом 1
index, range1, range2 = [], list(range(len(optimal[0]) // 2 + 1)), list(range(-1, -len(optimal[0]) // 2, -1))
for i in range(max(len(range1), len(range2))):
    try:
        index.append(range1[i])
    except IndexError:
        pass
    try:
        index.append(range2[i])
    except IndexError:
        pass
# таким образом мы заполним рюкзак сначала самыми большими предметами, а затем скомбинируем маленькие

# собираем рюкзак
bag = []
for i in index:
    item = optimal[0][i]

    if stuff_dict[item][0] == 3:
        bag.extend([item] * 3)
    elif stuff_dict[item][0] == 2:
        bag.extend([item] * 2)
    elif stuff_dict[item][0] == 1:
        bag.extend([item])

print(''.join([f'[{bag[i]}],' if i % 3 != 2 else f'[{bag[i]}]\n' for i in range(len(bag))]))
print('Итоговые очки выживания:', optimal[1])
print('Том выживет с таким набором предметов' if optimal[1] > 0 else 'Зомби сожрут Тома заживо...') 
