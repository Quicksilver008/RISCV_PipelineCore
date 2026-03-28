# Covers store/load plus RAW and load-use hazards.

    addi x1, x0, 12
    addi x2, x0, 3
    sw   x1, 0(x0)
    lw   x3, 0(x0)
    add  x4, x3, x2
    sw   x4, 4(x0)
    lw   x5, 4(x0)
    sub  x6, x5, x2
