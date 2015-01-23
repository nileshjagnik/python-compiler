.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $532,%esp

	call input
	movl %eax, -4(%ebp)

	pushl -4(%ebp)
	call print_int_nl
	addl $4, %esp

	call input
	movl %eax, -8(%ebp)

	movl -8(%ebp), %eax
	movl %eax, -12(%ebp)
	negl -12(%ebp)

	movl -12(%ebp), %eax
	movl %eax, -16(%ebp)
	negl -16(%ebp)

	movl -16(%ebp), %eax
	movl %eax, -20(%ebp)
	negl -20(%ebp)

	movl -20(%ebp), %eax
	movl %eax, -24(%ebp)
	negl -24(%ebp)

	movl -24(%ebp), %eax
	movl %eax, -28(%ebp)
	negl -28(%ebp)

	movl -28(%ebp), %eax
	movl %eax, -32(%ebp)
	negl -32(%ebp)

	movl -32(%ebp), %eax
	movl %eax, -36(%ebp)
	negl -36(%ebp)

	pushl -36(%ebp)
	call print_int_nl
	addl $4, %esp

	call input
	movl %eax, -40(%ebp)

	call input
	movl %eax, -44(%ebp)

	movl -44(%ebp), %eax
	movl %eax, -48(%ebp)
	negl -48(%ebp)

	movl -48(%ebp), %eax
	movl %eax, -52(%ebp)
	negl -52(%ebp)

	movl -40(%ebp), %eax
	movl %eax, -56(%ebp)
	movl -52(%ebp), %eax
	addl %eax, -56(%ebp)

	call input
	movl %eax, -60(%ebp)

	movl -60(%ebp), %eax
	movl %eax, -64(%ebp)
	negl -64(%ebp)

	movl -64(%ebp), %eax
	movl %eax, -68(%ebp)
	negl -68(%ebp)

	movl -68(%ebp), %eax
	movl %eax, -72(%ebp)
	negl -72(%ebp)

	movl -72(%ebp), %eax
	movl %eax, -76(%ebp)
	negl -76(%ebp)

	movl -76(%ebp), %eax
	movl %eax, -80(%ebp)
	negl -80(%ebp)

	movl -80(%ebp), %eax
	movl %eax, -84(%ebp)
	negl -84(%ebp)

	movl -84(%ebp), %eax
	movl %eax, -88(%ebp)
	negl -88(%ebp)

	movl -88(%ebp), %eax
	movl %eax, -92(%ebp)
	negl -92(%ebp)

	movl -56(%ebp), %eax
	movl %eax, -96(%ebp)
	movl -92(%ebp), %eax
	addl %eax, -96(%ebp)

	movl -96(%ebp), %eax
	movl %eax, -100(%ebp)

	call input
	movl %eax, -104(%ebp)

	call input
	movl %eax, -108(%ebp)

	movl -108(%ebp), %eax
	movl %eax, -112(%ebp)
	negl -112(%ebp)

	movl -112(%ebp), %eax
	movl %eax, -116(%ebp)
	negl -116(%ebp)

	movl -104(%ebp), %eax
	movl %eax, -120(%ebp)
	movl -116(%ebp), %eax
	addl %eax, -120(%ebp)

	call input
	movl %eax, -124(%ebp)

	movl -124(%ebp), %eax
	movl %eax, -128(%ebp)
	negl -128(%ebp)

	movl -128(%ebp), %eax
	movl %eax, -132(%ebp)
	negl -132(%ebp)

	movl -132(%ebp), %eax
	movl %eax, -136(%ebp)
	negl -136(%ebp)

	movl -136(%ebp), %eax
	movl %eax, -140(%ebp)
	negl -140(%ebp)

	movl -140(%ebp), %eax
	movl %eax, -144(%ebp)
	negl -144(%ebp)

	movl -144(%ebp), %eax
	movl %eax, -148(%ebp)
	negl -148(%ebp)

	movl -148(%ebp), %eax
	movl %eax, -152(%ebp)
	negl -152(%ebp)

	movl -152(%ebp), %eax
	movl %eax, -156(%ebp)
	negl -156(%ebp)

	movl -120(%ebp), %eax
	movl %eax, -160(%ebp)
	movl -156(%ebp), %eax
	addl %eax, -160(%ebp)

	pushl -160(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $1, -164(%ebp)
	pushl $1
	call print_int_nl
	addl $4, %esp

	movl $1, -168(%ebp)
	negl -168(%ebp)

	movl -168(%ebp), %eax
	movl %eax, -172(%ebp)

	movl $1, -176(%ebp)
	negl -176(%ebp)

	pushl -176(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $10, -180(%ebp)
	movl -180(%ebp), %eax
	movl %eax, -184(%ebp)
	negl -184(%ebp)

	movl -184(%ebp), %eax
	movl %eax, -188(%ebp)

	pushl -180(%ebp)
	call print_int_nl
	addl $4, %esp

	movl -180(%ebp), %eax
	movl %eax, -192(%ebp)
	negl -192(%ebp)

	pushl -192(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $1, -196(%ebp)
	add $3, -196(%ebp)

	movl -196(%ebp), %eax
	movl %eax, -200(%ebp)

	movl $1, -204(%ebp)
	add $3, -204(%ebp)

	pushl -204(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $5, -208(%ebp)
	negl -208(%ebp)

	movl $1, -212(%ebp)
	movl -208(%ebp), %eax
	addl %eax, -212(%ebp)

	movl -212(%ebp), %eax
	movl %eax, -216(%ebp)

	movl $5, -220(%ebp)
	negl -220(%ebp)

	movl $1, -224(%ebp)
	movl -220(%ebp), %eax
	addl %eax, -224(%ebp)

	pushl -224(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $1, -228(%ebp)
	add $3, -228(%ebp)

	movl -228(%ebp), %eax
	movl %eax, -232(%ebp)

	pushl -232(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $5, -236(%ebp)
	negl -236(%ebp)

	movl $1, -240(%ebp)
	movl -236(%ebp), %eax
	addl %eax, -240(%ebp)

	movl -240(%ebp), %eax
	movl %eax, -244(%ebp)

	pushl -244(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $1, -248(%ebp)
	add $2, -248(%ebp)

	movl $3, -252(%ebp)
	negl -252(%ebp)

	movl -248(%ebp), %eax
	movl %eax, -256(%ebp)
	movl -252(%ebp), %eax
	addl %eax, -256(%ebp)

	movl $7, -260(%ebp)
	negl -260(%ebp)

	movl -256(%ebp), %eax
	movl %eax, -264(%ebp)
	movl -260(%ebp), %eax
	addl %eax, -264(%ebp)

	movl $8, -268(%ebp)
	negl -268(%ebp)

	movl -264(%ebp), %eax
	movl %eax, -272(%ebp)
	movl -268(%ebp), %eax
	addl %eax, -272(%ebp)

	movl -272(%ebp), %eax
	movl %eax, -276(%ebp)

	pushl -276(%ebp)
	call print_int_nl
	addl $4, %esp

	movl -180(%ebp), %eax
	movl %eax, -280(%ebp)
	movl -232(%ebp), %eax
	addl %eax, -280(%ebp)

	movl -280(%ebp), %eax
	movl %eax, -284(%ebp)
	movl -244(%ebp), %eax
	addl %eax, -284(%ebp)

	call input
	movl %eax, -288(%ebp)

	movl -284(%ebp), %eax
	movl %eax, -292(%ebp)
	movl -288(%ebp), %eax
	addl %eax, -292(%ebp)

	call input
	movl %eax, -296(%ebp)

	movl -296(%ebp), %eax
	movl %eax, -300(%ebp)
	negl -300(%ebp)

	movl -292(%ebp), %eax
	movl %eax, -304(%ebp)
	movl -300(%ebp), %eax
	addl %eax, -304(%ebp)

	movl -304(%ebp), %eax
	movl %eax, -308(%ebp)
	movl -276(%ebp), %eax
	addl %eax, -308(%ebp)

	movl -180(%ebp), %eax
	movl %eax, -312(%ebp)
	negl -312(%ebp)

	movl -308(%ebp), %eax
	movl %eax, -316(%ebp)
	movl -312(%ebp), %eax
	addl %eax, -316(%ebp)

	movl -316(%ebp), %eax
	movl %eax, -320(%ebp)
	movl -232(%ebp), %eax
	addl %eax, -320(%ebp)

	movl -320(%ebp), %eax
	movl %eax, -324(%ebp)

	pushl -324(%ebp)
	call print_int_nl
	addl $4, %esp

	movl -324(%ebp), %eax
	movl %eax, -328(%ebp)
	negl -328(%ebp)

	movl -328(%ebp), %eax
	movl %eax, -332(%ebp)
	negl -332(%ebp)

	movl -332(%ebp), %eax
	movl %eax, -336(%ebp)
	negl -336(%ebp)

	movl -336(%ebp), %eax
	movl %eax, -340(%ebp)
	negl -340(%ebp)

	movl -340(%ebp), %eax
	movl %eax, -344(%ebp)
	negl -344(%ebp)

	pushl -344(%ebp)
	call print_int_nl
	addl $4, %esp

	movl -180(%ebp), %eax
	movl %eax, -348(%ebp)
	negl -348(%ebp)

	movl -348(%ebp), %eax
	movl %eax, -352(%ebp)
	negl -352(%ebp)

	movl -232(%ebp), %eax
	movl %eax, -356(%ebp)
	negl -356(%ebp)

	movl -356(%ebp), %eax
	movl %eax, -360(%ebp)
	negl -360(%ebp)

	movl -360(%ebp), %eax
	movl %eax, -364(%ebp)
	negl -364(%ebp)

	movl -364(%ebp), %eax
	movl %eax, -368(%ebp)
	negl -368(%ebp)

	movl -368(%ebp), %eax
	movl %eax, -372(%ebp)
	negl -372(%ebp)

	movl -352(%ebp), %eax
	movl %eax, -376(%ebp)
	movl -372(%ebp), %eax
	addl %eax, -376(%ebp)

	movl -244(%ebp), %eax
	movl %eax, -380(%ebp)
	negl -380(%ebp)

	movl -380(%ebp), %eax
	movl %eax, -384(%ebp)
	negl -384(%ebp)

	movl -376(%ebp), %eax
	movl %eax, -388(%ebp)
	movl -384(%ebp), %eax
	addl %eax, -388(%ebp)

	movl $7, -392(%ebp)
	negl -392(%ebp)

	movl -388(%ebp), %eax
	movl %eax, -396(%ebp)
	movl -392(%ebp), %eax
	addl %eax, -396(%ebp)

	movl $8, -400(%ebp)
	negl -400(%ebp)

	movl -400(%ebp), %eax
	movl %eax, -404(%ebp)
	negl -404(%ebp)

	movl -404(%ebp), %eax
	movl %eax, -408(%ebp)
	negl -408(%ebp)

	movl -408(%ebp), %eax
	movl %eax, -412(%ebp)
	negl -412(%ebp)

	movl -412(%ebp), %eax
	movl %eax, -416(%ebp)
	negl -416(%ebp)

	movl -416(%ebp), %eax
	movl %eax, -420(%ebp)
	negl -420(%ebp)

	movl -396(%ebp), %eax
	movl %eax, -424(%ebp)
	movl -420(%ebp), %eax
	addl %eax, -424(%ebp)

	movl -324(%ebp), %eax
	movl %eax, -428(%ebp)
	negl -428(%ebp)

	movl -428(%ebp), %eax
	movl %eax, -432(%ebp)
	negl -432(%ebp)

	movl -424(%ebp), %eax
	movl %eax, -436(%ebp)
	movl -432(%ebp), %eax
	addl %eax, -436(%ebp)

	movl -436(%ebp), %eax
	movl %eax, -440(%ebp)

	pushl -440(%ebp)
	call print_int_nl
	addl $4, %esp

	movl -180(%ebp), %eax
	movl %eax, -444(%ebp)
	negl -444(%ebp)

	movl -444(%ebp), %eax
	movl %eax, -448(%ebp)
	negl -448(%ebp)

	movl -232(%ebp), %eax
	movl %eax, -452(%ebp)
	negl -452(%ebp)

	movl -452(%ebp), %eax
	movl %eax, -456(%ebp)
	negl -456(%ebp)

	movl -456(%ebp), %eax
	movl %eax, -460(%ebp)
	negl -460(%ebp)

	movl -460(%ebp), %eax
	movl %eax, -464(%ebp)
	negl -464(%ebp)

	movl -464(%ebp), %eax
	movl %eax, -468(%ebp)
	negl -468(%ebp)

	movl -448(%ebp), %eax
	movl %eax, -472(%ebp)
	movl -468(%ebp), %eax
	addl %eax, -472(%ebp)

	movl -244(%ebp), %eax
	movl %eax, -476(%ebp)
	negl -476(%ebp)

	movl -476(%ebp), %eax
	movl %eax, -480(%ebp)
	negl -480(%ebp)

	movl -472(%ebp), %eax
	movl %eax, -484(%ebp)
	movl -480(%ebp), %eax
	addl %eax, -484(%ebp)

	movl $7, -488(%ebp)
	negl -488(%ebp)

	movl -484(%ebp), %eax
	movl %eax, -492(%ebp)
	movl -488(%ebp), %eax
	addl %eax, -492(%ebp)

	movl $8, -496(%ebp)
	negl -496(%ebp)

	movl -496(%ebp), %eax
	movl %eax, -500(%ebp)
	negl -500(%ebp)

	movl -500(%ebp), %eax
	movl %eax, -504(%ebp)
	negl -504(%ebp)

	movl -504(%ebp), %eax
	movl %eax, -508(%ebp)
	negl -508(%ebp)

	movl -508(%ebp), %eax
	movl %eax, -512(%ebp)
	negl -512(%ebp)

	movl -512(%ebp), %eax
	movl %eax, -516(%ebp)
	negl -516(%ebp)

	movl -492(%ebp), %eax
	movl %eax, -520(%ebp)
	movl -516(%ebp), %eax
	addl %eax, -520(%ebp)

	movl -324(%ebp), %eax
	movl %eax, -524(%ebp)
	negl -524(%ebp)

	movl -524(%ebp), %eax
	movl %eax, -528(%ebp)
	negl -528(%ebp)

	movl -520(%ebp), %eax
	movl %eax, -532(%ebp)
	movl -528(%ebp), %eax
	addl %eax, -532(%ebp)

	pushl -532(%ebp)
	call print_int_nl
	addl $4, %esp

	movl $0, %eax
	leave
	ret
