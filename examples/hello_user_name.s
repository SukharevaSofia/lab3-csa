    ldc r0 STR1
    ld r1 r0
    dec r1
_LOOP1:
    inc r0
    ld r2 r0
    out r2
    dec r1
    jge r1 _LOOP1


    ldc r0 10
    out r0

    ldc r0 STR2
    ld r1 r0
    dec r1

_LOOP2:
    inc r0
    ld r2 r0
    out r2
    dec r1
    jge r1 _LOOP2

; Now we are waiting for user input
    
    ldc r4 END
    ldc r5 10
_LOOP3:
    inc r4
    in r0
    sv r0 r4
    sub r0 r5
    jne r0 _LOOP3

    ldc r5 END
    sub r4 r5
    ldc r5 END
    sv r4 r5

    ldc r0 END
    ld r1 r0
    dec r1
_LOOPEH:
    inc r0
    ld r2 r0
    out r2
    dec r1
    jge r1 _LOOPEH


    ldc r0 STR3
    ld r1 r0
    dec r1
_LOOP4:
    inc r0
    ld r2 r0
    out r2
    dec r1
    jge r1 _LOOP4

    ldc r0 END
    ld r1 r0
    dec r1
_LOOP5:
    inc r0
    ld r2 r0
    out r2
    dec r1
    jge r1 _LOOP5

    hlt

HELLO_WORLD: "Hello World!"
STR1: "> What is your name?"
STR2: "< "
STR3: "> Hello, "
END: "_"
