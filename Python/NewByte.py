# # Function: 8 bit to 1 byte
# def temp_to_byte(temp):
#     b1 = temp + 40
#     return b1


# # Function: 1 byte to 8 bit
# def byte_to_temp(b1):
#     temp = b1 - 40
#     return temp


# # Function: ws and wd to 2 bytes
# def wind_to_byte(ws, wd):
#     b1 = wd // 2

#     if (wd % 2) == 1:
#         b2 = ws + 128  # wd is odd
#     else:
#         b2 = ws  # wd is even
#     return b1, b2


# # Function: 2 bytes to ws and wd
# def byte_to_wind(b1, b2):
#     if b2 > 127:
#         wd = b1 * 2 + 1
#         ws = b2 - 128
#     else:
#         wd = b1 * 2
#         ws = b2
#     return ws, wd


#Function: Convert wind direction and temperature from separate integers to 2 bytes
def windtemp_to_byte(wd, temp):
    temp += 40
    b1 = wd // 2
    if (wd%2) == 1:
        b2 = temp + 128 # wind dir is an odd number
    else:
        b2 = temp # wind dir is an even number
    return b1, b2

#Function: Convert wind direction and temperature from 2 bytes to separate integers
def byte_to_windtemp(b1, b2):
    if b2 > 127:
        wd = b1*2 + 1
        temp = b2 - 40 - 128
    else:
        wd = b1*2
        temp = b2 - 40
    return wd, temp

# wd = 3
# temp = 70
# b1, b2 = windtemp_to_byte(wd, temp)
# print(wd, temp)
# print(b1, b2)
# print(byte_to_windtemp(b1,b2))


for wd in range(0, 361):
    for temp in range(-40, 70):
        b1, b2 = windtemp_to_byte(wd, temp)
        #print(wd, temp, b1, b2)
        assert b1 < 255 and b2 < 255 and b1 >= 0 and b2 >= 0