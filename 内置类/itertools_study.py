from itertools import chain, combinations, count

x = [1, 2]
y = [[[1, 2], [4, 5]]]
z = 'ab'
c = chain(x, y, z)

for i in c:
    print(i)


# chain.from_iterable()
list(chain.from_iterable(['A', 'B', ['A', ['F', 'T']]]))

# combineations
list(combinations([1, 2, 3, 7, 10], 3))



from collections import Counter

Counter([1, 2, 3, 1]).keys()


