# Sample program for RISCV_PipelineCore
# Exercises ALU ops, store/load, load-use hazard, and branch flush behavior.

    addi x1, x0, 5
    addi x2, x0, 7
    add  x3, x1, x2
    sub  x4, x3, x1
    sw   x4, 0(x0)
    lw   x5, 0(x0)
    addi x6, x5, 5
    beq  x6, x3, done
    addi x7, x0, 1

done:
    addi x7, x0, 2
