#fiss and buzzz

list = [1,2,3,4]

i = 1 

for i in range(1, 1+100):
    number = ''
    print(f"Number is : {i}")
    if i % 2 == 0:
        number += 'Fiss'
        #print(f'Fiss: {i}')
    if i % 3 == 0:
        number += 'Buzz'
        #print(f'Buzz : {i}')
    if i % 5 == 0:
        number += 'Bizz'
        #print(f'bizz : {i}')
    
    print(number)