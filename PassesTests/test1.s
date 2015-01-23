.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $28,%esp

	call input
	movl %eax, -4(%ebp)

	movl $5, -8(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -8(%ebp)

	movl $6, -12(%ebp)
	negl -12(%ebp)

	movl -8(%ebp), %eax
	movl %eax, -16(%ebp)
	movl -12(%ebp), %eax
	addl %eax, -16(%ebp)

	call input
	movl %eax, -20(%ebp)

	movl -16(%ebp), %eax
	movl %eax, -24(%ebp)
	movl -20(%ebp), %eax
	addl %eax, -24(%ebp)

	movl -24(%ebp), %eax
	movl %eax, -28(%ebp)

	pushl -28(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
