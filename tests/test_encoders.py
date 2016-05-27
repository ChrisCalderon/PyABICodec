# coding=utf-8
from abicodec import encoders
import pytest

class TestEncoders(object):
    def test_abi_int(self):
        abi_int = encoders.abi_int
        assert abi_int(32, 69) == '0000000000000000000000000000000000000000000000000000000000000045'
        assert abi_int(64, -1) == 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        with pytest.raises(AssertionError):
            abi_int(16, 65536)
        with pytest.raises(AssertionError):
            abi_int(31, 69)
        with pytest.raises(AssertionError):
            abi_int(8, -129)

    def test_abi_uint(self):
        abi_uint = encoders.abi_uint
        assert abi_uint(32, 69) == '0000000000000000000000000000000000000000000000000000000000000045'
        assert abi_uint(8, 255) == '00000000000000000000000000000000000000000000000000000000000000ff'
        with pytest.raises(AssertionError):
            abi_uint(64, -1)
        with pytest.raises(AssertionError):
            abi_uint(16, 65536)
        with pytest.raises(AssertionError):
            abi_uint(31, 69)
        with pytest.raises(AssertionError):
            abi_uint(8, 256)

    def test_abi_bool(self):
        abi_bool = encoders.abi_bool
        assert abi_bool(0) == '0000000000000000000000000000000000000000000000000000000000000000'
        assert abi_bool(False) == '0000000000000000000000000000000000000000000000000000000000000000'
        assert abi_bool(1) == '0000000000000000000000000000000000000000000000000000000000000001'
        assert abi_bool(True) == '0000000000000000000000000000000000000000000000000000000000000001'
        assert abi_bool(-1) == '0000000000000000000000000000000000000000000000000000000000000001'

    def test_abi_address(self):
        abi_address = encoders.abi_address
        with pytest.raises(AssertionError):
            abi_address('0x2a65aca4d5fc5b5c859090a6c34d164135398226')

        assert abi_address(242045027043577165691557393543700327659040506406) == '0000000000000000000000002a65aca4d5fc5b5c859090a6c34d164135398226'
        
    def test_abi_fixed(self):
        abi_fixed = encoders.abi_fixed
        assert abi_fixed((128, 128), 8.5) == '0000000000000000000000000000000880000000000000000000000000000000'
        assert abi_fixed((128, 128), 2.125) == '0000000000000000000000000000000220000000000000000000000000000000'
        assert abi_fixed((128, 128), -8.5) == 'fffffffffffffffffffffffffffffff780000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_fixed((160, 128), -8.5)
        with pytest.raises(AssertionError):
            abi_fixed((64, 0), 8.6)
        
    def test_abi_ufixed(self):
        abi_ufixed = encoders.abi_ufixed
        assert abi_ufixed((128, 128), 8.5) == '0000000000000000000000000000000880000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_ufixed((128, 128), -8.5)

    def test_abi_bytes(self):
        abi_bytes = encoders.abi_bytes
        assert abi_bytes(10, 'lolol') == '6c6f6c6f6c000000000000000000000000000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_bytes(10, 'lololololol')

    def test_static_array(self):
        ABITypes = encoders.ABITypes
        abi_static_array = encoders.abi_static_array
        assert abi_static_array(ABITypes.INT, 32, [69, -1]) == '0000000000000000000000000000000000000000000000000000000000000045ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        with pytest.raises(AssertionError):
            abi_static_array(ABITypes.INT, 8, [-300, 2011])
        assert abi_static_array(ABITypes.UINT, 8, [120, 240]) == '000000000000000000000000000000000000000000000000000000000000007800000000000000000000000000000000000000000000000000000000000000f0'
        with pytest.raises(AssertionError):
            abi_static_array(ABITypes.UINT, 8, [-120, 120])
        assert abi_static_array(ABITypes.BOOL, None, ['ay', 'lmao', '']) == '000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000' 
        assert abi_static_array(ABITypes.ADDRESS, None, [1, 2, 3]) == '000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000003'
        with pytest.raises(AssertionError):
            abi_static_array(ABITypes.ADDRESS, None, [1, 2, -3])
        assert abi_static_array(ABITypes.FIXED, (128, 128), [8.5, 2.125, -24.625]) == '00000000000000000000000000000008800000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000ffffffffffffffffffffffffffffffe760000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_static_array(ABITypes.FIXED, (8, 8), [300.25, -150.625])
        assert abi_static_array(ABITypes.UFIXED, (128, 128), [8.5, 2.125, 24.625]) == '0000000000000000000000000000000880000000000000000000000000000000000000000000000000000000000000022000000000000000000000000000000000000000000000000000000000000018a0000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_static_array(ABITypes.UFIXED, (128, 128), [8.5, 2.125, -24.625])
        assert abi_static_array(ABITypes.BYTES, 10, ['lolol', 'aylmaooo']) == '6c6f6c6f6c00000000000000000000000000000000000000000000000000000061796c6d616f6f6f000000000000000000000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_static_array(ABITypes.BYTES, 10, ['Lorem ipsum dolor sit amet,', ' consectetur adipiscing elit'])
    
    def test_abi_bytes_dynamic(self):
        abi_bytes_dynamic = encoders.abi_bytes_dynamic
        assert abi_bytes_dynamic('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.') == '000000000000000000000000000000000000000000000000000000000000007b4c6f72656d20697073756d20646f6c6f722073697420616d65742c20636f6e73656374657475722061646970697363696e6720656c69742c2073656420646f20656975736d6f642074656d706f7220696e6369646964756e74207574206c61626f726520657420646f6c6f7265206d61676e6120616c697175612e0000000000'
        with pytest.raises(UnicodeEncodeError):
            abi_bytes_dynamic(u'Съешь же ещё этих мягких французских булок, да выпей чаю')

    def test_abi_string(self):
        abi_string = encoders.abi_string
        assert abi_string(u'Съешь же ещё этих мягких французских булок, да выпей чаю') == '0000000000000000000000000000000000000000000000000000000000000066d0a1d18ad0b5d188d18c20d0b6d0b520d0b5d189d19120d18dd182d0b8d18520d0bcd18fd0b3d0bad0b8d18520d184d180d0b0d0bdd186d183d0b7d181d0bad0b8d18520d0b1d183d0bbd0bed0ba2c20d0b4d0b020d0b2d18bd0bfd0b5d0b920d187d0b0d18e0000000000000000000000000000000000000000000000000000'

    def test_abi_dynamic_array(self):
        abi_dynamic_array = encoders.abi_dynamic_array
        ABITypes = encoders.ABITypes
        assert abi_dynamic_array(ABITypes.INT, 32, [69, -1]) == '00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000045ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        with pytest.raises(AssertionError):
            abi_dynamic_array(ABITypes.INT, 8, [-300, 2011])
        assert abi_dynamic_array(ABITypes.UINT, 8, [120, 240]) == '0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000007800000000000000000000000000000000000000000000000000000000000000f0'
        with pytest.raises(AssertionError):
            abi_dynamic_array(ABITypes.UINT, 8, [-120, 120])
        assert abi_dynamic_array(ABITypes.BOOL, None, ['ay', 'lmao', '']) == '0000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000' 
        assert abi_dynamic_array(ABITypes.ADDRESS, None, [1, 2, 3]) == '0000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000003'
        with pytest.raises(AssertionError):
            abi_dynamic_array(ABITypes.ADDRESS, None, [1, 2, -3])
        assert abi_dynamic_array(ABITypes.FIXED, (128, 128), [8.5, 2.125, -24.625]) == '000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000008800000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000ffffffffffffffffffffffffffffffe760000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_dynamic_array(ABITypes.FIXED, (8, 8), [300.25, -150.625])
        assert abi_dynamic_array(ABITypes.UFIXED, (128, 128), [8.5, 2.125, 24.625]) == '00000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000880000000000000000000000000000000000000000000000000000000000000022000000000000000000000000000000000000000000000000000000000000018a0000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_dynamic_array(ABITypes.UFIXED, (128, 128), [8.5, 2.125, -24.625])
        assert abi_dynamic_array(ABITypes.BYTES, 10, ['lolol', 'aylmaooo']) == '00000000000000000000000000000000000000000000000000000000000000026c6f6c6f6c00000000000000000000000000000000000000000000000000000061796c6d616f6f6f000000000000000000000000000000000000000000000000'
        with pytest.raises(AssertionError):
            abi_dynamic_array(ABITypes.BYTES, 10, ['Lorem ipsum dolor sit amet,', ' consectetur adipiscing elit'])
    
