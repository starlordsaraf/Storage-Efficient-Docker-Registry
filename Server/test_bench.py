def pop_func (seq):
    pop_list = []
    count_dict = dict()
    threshold = 0.2
    total = 0

    for i in seq:
        total += 1
        if i not in count_dict:
            count_dict[i] = 1
        else:
            count_dict[i] += 1

        pop_frac = count_dict[i] / total

        if pop_frac >= threshold:
            if i in pop_list:
                continue
            else:
                pop_list.append(i)

        else:
            if i in pop_list:
                pop_list.pop(i)
            else:
                continue

    print()
    print("List of popular images is")

    for i in pop_list:
        print(i)

print("Enter Sequence:")
seq = list(map(str,input().split()))
pop_func(seq)