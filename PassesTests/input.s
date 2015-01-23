.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $20,%esp

	call input
	movl %eax, -4(%ebp)

	call input
	movl %eax, -8(%ebp)

	movl -4(%ebp), %eax
	movl %eax, -12(%ebp)
	movl -8(%ebp), %eax
	addl %eax, -12(%ebp)

	movl -12(%ebp), %eax
	movl %eax, -16(%ebp)

	call input
	movl %eax, -20(%ebp)

	pushl -20(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
