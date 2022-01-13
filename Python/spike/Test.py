from sys import stdin, stdout

stdout.buffer.write(bytes([10]))
print(stdin.buffer.read(10))