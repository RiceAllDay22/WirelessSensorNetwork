import fram_test

fram = fram_test.get_fram()
print(fram)

def index_to_byte(index):
    b1 = index // 256
    b2 = index - b1*256
    return b1, b2

fram_counter = 0
print(fram_counter)

def fram_upload(row):
    global fram_counter
    for i in range(0, 6):
        fram[fram_counter] = row[i]
        fram_counter += 1
    return None

unix  = [0, 255, 10, 10, 10, 10]
data1 = [3, 21, 21, 31, 31, 41]
fram_upload(unix)
print(fram_counter)
fram_upload(data1)
print(fram_counter)

for i in range(0, fram_counter):
    print(fram[i])