UINTMAX = 1 << 256
INTMAX = 1 << 255
INTMIN = -INTMAX


def assert_bits(bits):
    assert bits%8==0, "Bits for ABI type not divisible by 8!"
    assert 0 < bits <= 256, "Bits for ABI type out of range!"


def assert_signed_size(bits, x):
    errmsg = "x not in correct range for signed int with {} bits!"
    assert -(1 << (bits - 1)) <= x < (1 << (bits - 1)), errmsg.format(bits)


def assert_unsigned_size(bits, x):
    errmsg = "x not in correct range for unsigned int with {} bits!"
    assert 0 <= x < (1 << bits), errmsg.format(bits)


def encode_num(x):
    hex(x)[2:].rjust(64, '0')


def abi_int(bits, x):
    assert_bits(bits)
    assert_signed_size(bits, x)
    return encode_num(x%UINTMAX)


def abi_uint(bits, x):
    assert_bits(bits)
    assert_unsigned_size(bits, x)
    return encode_nonfix(x)


def assert_fixed_bits(hi_bits, low_bits):
    assert hi_bits%8==0, "High bits must be divisible by 8!"
    assert low_bits%8==0, "Low bits must by divisible by 8!"
    assert 0 < (hi_bits + low_bits) <= 256, "High bits + low bits not in correct range!"


def abi_fixed(high, low, x):
    assert_fixed_bits(high, low)
    assert_signed_size(high, int(x))
    return encode_num(int(x*2**low)%INTMAX)


def abi_ufixed(high, low, x):
    assert_fixed_bits(high, low)
    assert_unsigned_size(high, int(x))
    return encode_num(int(x*2**low))


def abi_bytes_static(bytes_, x):
    assert 0 < bytes_ <= 32, "Byte size out of range!"
    assert len(x) <= bytes_, "x too big for byte size!"
    return x.ljust(32, '\x00').encode('hex')


def abi_bytes_dynamic(x):
    return encode_num(len(x)) + x.ljust(len(x) + (32 - len(x)%32), '\x00').encode('hex')

