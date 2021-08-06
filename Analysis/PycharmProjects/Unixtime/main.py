
t = 1628124950
SECONDS_FROM_1970_TO_2000 = 946684800
t -= SECONDS_FROM_1970_TO_2000

ss = t % 60
t /= 60
mm = t % 60
t /= 60
hh = t % 24
print(ss)
print(mm)
print(hh)
days = t/24
print(days)

yOff = 0
leap = yOff% 4 == 0
print(leap)