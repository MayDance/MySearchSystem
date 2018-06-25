def vb_encode_number(n):
    byte_array = bytearray(1)
    byte_array[0] = n % 128
    while n >= 128:
        n = int(n / 128)
        byte_array = bytearray(1)+byte_array
        byte_array[0] = n % 128
    byte_array[len(byte_array) - 1] += 128
    return byte_array


def vb_encode(number_list):
    byte_array = bytearray()
    for n in number_list:
        byte_array += vb_encode_number(n)
    return byte_array


def vb_decode(byte_array):
    number_list = []
    n = 0
    for i in range(len(byte_array)):
        if byte_array[i] < 128:
            n = n * 128 + byte_array[i]
        else:
            n = n * 128 + byte_array[i] - 128
            number_list.append(n)
            n = 0
    return number_list
