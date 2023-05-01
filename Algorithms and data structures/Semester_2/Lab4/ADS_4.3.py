def longest_increasing_sequence(N):
    # инициализация массива длин наибольших возрастающих подпоследовательностей
    lengths = [1] * len(N)
    # инициализация массива предшествующих элементов для восстановления последовательности
    prev_elements = [-1] * len(N)

    # поиск наибольшей возрастающей последовательности
    for i in range(1, len(N)):
        for j in range(i):
            if N[j] < N[i] and lengths[j] + 1 > lengths[i]:
                lengths[i] = lengths[j] + 1
                prev_elements[i] = j

    # восстановление наибольшей возрастающей последовательности
    max_length = max(lengths)
    end_index = lengths.index(max_length)
    sequence = []
    while end_index != -1:
        sequence.append(N[end_index])
        end_index = prev_elements[end_index]
    sequence.reverse()

    return sequence

N = [5, 1, 3, 7, 79, 4, 5, 6, 8, 9, 10, 1]
sequence = longest_increasing_sequence(N)
print("Наибольшая непрерывная возрастающая последовательность:", sequence)