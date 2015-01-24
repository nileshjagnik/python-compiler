.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $204,%esp

	movl $1, -4(%ebp)

	movl $1, -8(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -8(%ebp)

	movl -8(%ebp), %eax
	movl %eax, -12(%ebp)

	call input
	movl %eax, -16(%ebp)

	movl -16(%ebp), %eax
	movl %eax, -20(%ebp)
	movl -12(%ebp), %eax
	addl %eax, -20(%ebp)

	movl -20(%ebp), %eax
	movl %eax, -24(%ebp)

	movl $1, -28(%ebp)
	addl $2, -28(%ebp)

	movl -28(%ebp), %eax
	movl %eax, -32(%ebp)
	addl $3, -32(%ebp)

	movl -32(%ebp), %eax
	movl %eax, -36(%ebp)
	addl $4, -36(%ebp)

	movl -36(%ebp), %eax
	movl %eax, -40(%ebp)
	addl $5, -40(%ebp)

	movl -40(%ebp), %eax
	movl %eax, -44(%ebp)
	addl $6, -44(%ebp)

	movl -44(%ebp), %eax
	movl %eax, -48(%ebp)
	addl $7, -48(%ebp)

	movl -48(%ebp), %eax
	movl %eax, -52(%ebp)
	addl $8, -52(%ebp)

	movl -52(%ebp), %eax
	movl %eax, -56(%ebp)
	addl $9, -56(%ebp)

	movl -56(%ebp), %eax
	movl %eax, -60(%ebp)
	addl $10, -60(%ebp)

	movl -60(%ebp), %eax
	movl %eax, -64(%ebp)

	call input
	movl %eax, -68(%ebp)

	movl -64(%ebp), %eax
	movl %eax, -72(%ebp)
	movl -68(%ebp), %eax
	addl %eax, -72(%ebp)

	movl -72(%ebp), %eax
	movl %eax, -76(%ebp)

	movl $1, -80(%ebp)

	call input
	movl %eax, -84(%ebp)

	call input
	movl %eax, -88(%ebp)

	movl -84(%ebp), %eax
	movl %eax, -92(%ebp)
	movl -88(%ebp), %eax
	addl %eax, -92(%ebp)

	movl -92(%ebp), %eax
	movl %eax, -96(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -96(%ebp)

	call input
	movl %eax, -100(%ebp)

	movl -100(%ebp), %eax
	movl %eax, -104(%ebp)

	movl $1, -108(%ebp)
	negl -108(%ebp)

	movl -108(%ebp), %eax
	movl %eax, -112(%ebp)

	movl $10, -116(%ebp)
	movl -76(%ebp), %eax
	addl %eax, -116(%ebp)

	movl -116(%ebp), %eax
	movl %eax, -120(%ebp)
	movl -80(%ebp), %eax
	addl %eax, -120(%ebp)

	movl -120(%ebp), %eax
	movl %eax, -124(%ebp)
	movl -104(%ebp), %eax
	addl %eax, -124(%ebp)

	movl -124(%ebp), %eax
	movl %eax, -128(%ebp)

	movl -4(%ebp), %eax
	movl %eax, -132(%ebp)
	movl -12(%ebp), %eax
	addl %eax, -132(%ebp)

	pushl -132(%ebp)
	call print_int_nl
	addl $4, %esp

	call input
	movl %eax, -136(%ebp)

	movl -136(%ebp), %eax
	movl %eax, -140(%ebp)
	addl $7, -140(%ebp)

	call input
	movl %eax, -144(%ebp)

	movl -140(%ebp), %eax
	movl %eax, -148(%ebp)
	movl -144(%ebp), %eax
	addl %eax, -148(%ebp)

	movl -148(%ebp), %eax
	movl %eax, -152(%ebp)

	movl -152(%ebp), %eax
	movl %eax, -156(%ebp)
	movl -4(%ebp), %eax
	addl %eax, -156(%ebp)

	movl -156(%ebp), %eax
	movl %eax, -160(%ebp)

	pushl -160(%ebp)
	call print_int_nl
	addl $4, %esp

	movl -4(%ebp), %eax
	movl %eax, -164(%ebp)
	movl -12(%ebp), %eax
	addl %eax, -164(%ebp)

	movl -164(%ebp), %eax
	movl %eax, -168(%ebp)
	movl -112(%ebp), %eax
	addl %eax, -168(%ebp)

	call input
	movl %eax, -172(%ebp)

	movl -172(%ebp), %eax
	movl %eax, -176(%ebp)
	negl -176(%ebp)

	movl -168(%ebp), %eax
	movl %eax, -180(%ebp)
	movl -176(%ebp), %eax
	addl %eax, -180(%ebp)

	movl -180(%ebp), %eax
	movl %eax, -184(%ebp)

	movl -184(%ebp), %eax
	movl %eax, -188(%ebp)
	addl $7, -188(%ebp)

	movl -188(%ebp), %eax
	movl %eax, -192(%ebp)

	call input
	movl %eax, -196(%ebp)

	movl -196(%ebp), %eax
	movl %eax, -200(%ebp)
	movl -192(%ebp), %eax
	addl %eax, -200(%ebp)

	movl -200(%ebp), %eax
	movl %eax, -204(%ebp)

	pushl -204(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
