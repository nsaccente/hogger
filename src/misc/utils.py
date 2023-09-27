from enum import IntFlag
from math import log2

class IntFlagUtils:
    @staticmethod
    def add_flags(flags: list[int | IntFlag]) -> int:
        return sum([2**flag for flag in flags])

    @staticmethod
    def decompose_int(x: int) -> list[int | IntFlag]:
        powers = []
        i = 1
        while i <= x:
            if i & x:
                powers.append(int(log2(i)))
            i <<= 1
        return powers
