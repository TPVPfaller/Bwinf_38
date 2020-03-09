from collections import defaultdict

person1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
bounds1 = ['9:00', '20:00']
person2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
bounds2 = ['10:00', '18:30']

times = defaultdict()

for i in range(24):
    for j in range(2):
        if i < 10:
            if j == 0:
                times['0' + str(i) + ':' + '00'] = True
            if j == 1:
                times['0' + str(i) + ':' + '30'] = True
        else:
            if j == 0:
                times[str(i) + ':' + '00'] = True
            if j == 1:
                times[str(i) + ':' + '30'] = True

