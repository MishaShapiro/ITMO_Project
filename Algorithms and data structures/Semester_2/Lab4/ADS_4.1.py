exponats = [(1, 3), (1, 3), (4, 10), (7, 5), (2, 100), (7, 5), (7, 5), (8, 5), (2, 100)] # (Weight, Price)
repeats = 3
max_weight = 8

def weight_index_finder(element):
    return element[1] / element[0]

def sorted_exponats_finder(weight_index, exponats):
    sorted_exponats = []
    for i in sorted(weight_index.values(), reverse=1):
        for j in exponats:
            if weight_index[j] == i:
                sorted_exponats.append(j)
    return sorted_exponats

def price_finder(mass):
    price = 0
    for i in mass:
        price += i[1]
    return price

weight_index = {}

for i in exponats:
    if not(i in weight_index.keys()):
        weight_index[i] = weight_index_finder(i)

sorted_exponats = sorted_exponats_finder(weight_index, exponats)

result_list = []

for i in range(repeats):
    now_weight = 0
    copy_list = []
    for j in range(0, len(sorted_exponats)):
        if now_weight + sorted_exponats[j][0] <= max_weight:
            result_list.append(sorted_exponats[j])
            now_weight += sorted_exponats[j][0]
        else:
            copy_list.append(sorted_exponats[j])
    sorted_exponats = copy_list[::]

print(price_finder(result_list))
