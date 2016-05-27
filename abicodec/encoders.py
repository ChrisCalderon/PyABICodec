from .abitypes import ABITypes

UINTMAX = 1 << 256
INTMAX = 1 << 255
INTMIN = -INTMAX


##### Assertions ######


def assert_int_bits(bits):
    assert bits%8==0, "Bits for ABI type not divisible by 8!"
    assert 0 < bits <= 256, "Bits for ABI type out of range!"


def assert_signed_size(bits, x):
    errmsg = "x not in correct range for signed int with {} bits!"
    assert -(1 << (bits - 1)) <= x < (1 << (bits - 1)), errmsg.format(bits)


def assert_unsigned_size(bits, x):
    errmsg = "x not in correct range for unsigned int with {} bits!"
    assert 0 <= x < (1 << bits), errmsg.format(bits)


def assert_fixed_bits(hi_bits, low_bits):
    assert hi_bits%8==0, "High bits must be divisible by 8!"
    assert low_bits%8==0, "Low bits must by divisible by 8!"
    assert 0 < hi_bits, "High bits can't be 0!"
    assert 0 < low_bits, "Low bits can't be 0!"
    assert 0 < (hi_bits + low_bits) <= 256, "High bits + low bits not in correct range!"


##### Static Type Encoders #####


def encode_num(x):
    return hex(x)[2:].rstrip('L').rjust(64, '0')


def abi_int(bits, x):
    assert_int_bits(bits)
    assert_signed_size(bits, x)
    return encode_num(x%UINTMAX)


def abi_uint(bits, x):
    assert_int_bits(bits)
    assert_unsigned_size(bits, x)
    return encode_num(x)


def abi_bool(b):
    return encode_num(bool(b))


def abi_address(a):
    return abi_uint(160, a)


def abi_fixed(high_low, x):
    high, low = high_low
    assert_fixed_bits(high, low)
    assert_signed_size(high, int(x))
    return encode_num(int(x*2**low)%UINTMAX)


def abi_ufixed(high_low, x):
    high, low = high_low
    assert_fixed_bits(high, low)
    assert_unsigned_size(high, int(x))
    return encode_num(int(x*2**low))


def abi_bytes(bytes_, x):
    assert 0 < bytes_ <= 32, "Byte size out of range!"
    assert len(x) <= bytes_, "x too big for byte size!"
    return x.ljust(32, '\x00').encode('hex')


STATIC_ENCODER_BY_TYPE = {
    ABITypes.INT: abi_int,
    ABITypes.UINT: abi_uint,
    ABITypes.BOOL: abi_bool,
    ABITypes.FIXED: abi_fixed,
    ABITypes.UFIXED: abi_ufixed,
    ABITypes.ADDRESS: abi_address,
    ABITypes.BYTES: abi_bytes,
}


def abi_static_array(type, bits, x):
    if type in (ABITypes.BOOL, ABITypes.ADDRESS):
        encoder = STATIC_ENCODER_BY_TYPE[type]
    else:
        _encoder = STATIC_ENCODER_BY_TYPE[type]
        encoder = lambda y: _encoder(bits, y)
    return ''.join(map(encoder, x))
    

##### Dynamic Type Encoders #####


def abi_bytes_dynamic(x):
    l = len(x)
    padded_x_len = l if l%32==0 else l + 32 - l%32
    padded_x = x.ljust(padded_x_len, '\x00')
    return encode_num(len(x)) + padded_x.encode('hex')


def abi_string(x):
    if isinstance(x, unicode):
        return abi_bytes_dynamic(x.encode('utf8'))
    else:
        return abi_bytes_dynamic(x)


def abi_dynamic_array(type, bits, x):
    return encode_num(len(x)) + abi_static_array(type, bits, x)
