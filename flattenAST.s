.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $24,%esp

	movl -4(%ebp), %eax
	movl %eax, -8(%ebp)
	add $2, -8(%ebp)

	movl -8(%ebp), %eax
	movl %eax, -12(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -12(%ebp)

	movl -12(%ebp), %eax
	movl %eax, -16(%ebp)
	add $4, -16(%ebp)

	movl -16(%ebp), %eax
	movl %eax, -20(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -20(%ebp)

	movl $0, %eax
	leave
	ret
