.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $12,%esp

	call input
	movl %eax, -4(%ebp)

	movl -4(%ebp), %eax
	movl %eax, -8(%ebp)
	negl -8(%ebp)

	movl -8(%ebp), %eax
	movl %eax, -12(%ebp)
	add $2, -12(%ebp)

	pushl -12(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
