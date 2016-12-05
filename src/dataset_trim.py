lines = open('datasets/small_census.txt').readlines()
f = open('datasets/age_trim.txt', 'w')

for line in lines:
    x = line.strip().replace(' ', '').split(',')
    y = '{}, {}\n'.format(x[0], x[14])
    f.write(y)
