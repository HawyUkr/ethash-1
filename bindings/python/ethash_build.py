# ethash: C/C++ implementation of Ethash, the Ethereum Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    "_ethash",
    r"""
    #include <ethash/keccak.h>
     """,
    include_dirs=['include'],
    libraries=['ethash'],
    library_dirs=['dist/lib']
)

ffibuilder.cdef("""

union ethash_hash256
{
    ...;
    char str[32];
};

union ethash_hash512
{
    ...;
    char str[64];
};

union ethash_hash256 ethash_keccak256(const uint8_t* data, size_t size);

union ethash_hash512 ethash_keccak512(const uint8_t* data, size_t size);

""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
