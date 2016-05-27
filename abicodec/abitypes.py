from collections import namedtuple

ABITypes = namedtuple('ABItypes', 
                      ('INT',
                       'UINT',
                       'FIXED',
                       'UFIXED',
                       'BOOL',
                       'ADDRESS',
                       'BYTES'))(*range(7))
