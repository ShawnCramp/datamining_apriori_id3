lines = open('datasets/small_census.txt').readlines()
f = open('datasets/trim.txt', 'w')

for line in lines:
    x = line.strip().replace(' ', '').split(',')
    y = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(x[0], x[1], x[3], x[5], x[6], x[7], x[8], x[9], x[13], x[14])
    f.write(y)
