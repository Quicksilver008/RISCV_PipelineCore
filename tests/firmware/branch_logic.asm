# Covers branch flush plus logical and compare instructions.

    addi x1, x0, 1
    addi x2, x0, 1
    beq  x1, x2, taken
    addi x3, x0, 99

taken:
    addi x3, x0, 7
    addi x4, x0, 2
    or   x5, x3, x4
    and  x6, x5, x4
    slt  x7, x4, x3
    beq  x4, x3, done
    addi x8, x0, 11

done:
    addi x9, x0, 4
