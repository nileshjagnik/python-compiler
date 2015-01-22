.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	pushl $4
	call print_int_nl
	leave
	ret