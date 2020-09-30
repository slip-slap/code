global start


;section .text

start:
	push 1024
	call _malloc
    mov     rax, 0x2000004 ; write
    mov     rdi, 1 ; stdout
    mov     rsi, msg
    mov     rdx, msg.len
    syscall

    mov     rax, 0x2000001 ; exit
    mov     rdi, 0
    syscall

	


section .data

msg:    db      "Hell0, world!", 10
.len:   equ     $ - msg
