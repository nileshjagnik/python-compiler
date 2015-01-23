.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $12,%esp

	movl $1, -8(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -8(%ebp)

	movl -8(%ebp), %eax
	movl %eax, -12(%ebp)
	negl -12(%ebp)

	pushl -12(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
