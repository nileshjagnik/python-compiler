.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $16,%esp

	call input
	movl %eax, -4(%ebp)

	movl -4(%ebp), %eax
	movl %eax, -8(%ebp)

	call input
	movl %eax, -12(%ebp)

	call input
	movl %eax, -16(%ebp)

	pushl -16(%ebp)
	call print_int_nl
	addl $4, %esp

	pushl -8(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
