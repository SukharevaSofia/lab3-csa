; all labels start with _
; r0 - addr of hello world, is an iter to string
; r1 length of hello world
; r2 - current symbol
    ldc r0 HELLO_WORLD
    ld r1 r0
    dec r1
_LOOP:
; iter to next char
    inc r0
; load current symbol into r2
    ld r2 r0
; out current character
    out r2
; decrement loop counter
    dec r1
; loop
    jge r1 _LOOP
    hlt

HELLO_WORLD: "Hello World!"
