import fram_test

print('Hello There')

fram = fram_test.get_fram()
print(fram)

def index_to_byte(index):
    b1 = index // 256
    b2 = index - b1*256
    return b1, b2

index = 0
bi1, bi2 = index_to_byte(index)

fram[0], fram[1] = bi1, bi2
print(fram[0], fram[1])

print('')
print()
#fram_main.test()
