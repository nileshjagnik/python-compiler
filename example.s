.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $24,%esp

	movl -8(%ebp), %eax
	movl %eax, -12(%ebp)
	negl -12(%ebp)

	movl -16(%ebp), %eax
	movl %eax, -20(%ebp)
	add $2, -20(%ebp)

	pushl -24(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
