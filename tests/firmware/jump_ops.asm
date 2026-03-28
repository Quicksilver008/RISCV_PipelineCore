# Covers jal and jalr, including jump-result writeback and flush behavior.

    addi x1, x0, 4
    jal  x5, target
    addi x2, x0, 99

target:
    addi x2, x0, 7
    addi x3, x0, 20
    jalr x6, 12(x3)
    addi x4, x0, 77
    addi x7, x0, 1

landing:
    addi x4, x0, 9
