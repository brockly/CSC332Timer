from random import randint

def question_generator():
    first = [x for x in range(1,12)]
    second = [y for y in range(2,21)]

    print(len(first))
    print(len(second))
    
    answer_list = []
    for x in first:
        for y in second:
            answer_list.append(x*y)

    # print(answer_list)
    random_first = randint(1, len(first))
    random_second = randint(2, len(second))
    print(random_first)
    print(random_second)

question_generator()