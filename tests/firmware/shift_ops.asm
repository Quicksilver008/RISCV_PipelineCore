# Covers register and immediate shift instructions.

    addi x1, x0, 1
    addi x2, x0, 8
    add  x3, x0, x1
    sll  x4, x1, x2
    srl  x5, x4, x2
    addi x6, x0, -8
    sra  x7, x6, x1
    slli x8, x1, 4
    srli x9, x8, 2
    srai x10, x6, 2
