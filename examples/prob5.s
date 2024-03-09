jump _MAIN

; notation
; input:
; r0 - number1
; r1 - number2
; output:
; r0 - result
; clobbers:
; r0 - r2
_NOD:
  jeq r0 _NOD_END
  jeq r1 _NOD_END
  mov r2 r0
  sub r2 r1
  jge r2 _NOD_POS
  jump _NOD_NEG
_NOD_POS:
  mod r0 r1
  jump _NOD
_NOD_NEG:
  mod r1 r0
  jump _NOD
_NOD_END:
  mov r2 r0
  sub r2 r1
  jge r2 _NOD_RET
  mov r0 r1
_NOD_RET:
  jump _NOK_FROM_NOD


; inputs:
; r3 - number1
; r4 - number2
; return:
; r3 res
; clobbers:
; r0-r5
_NOK:
mov r0 r3
mov r1 r4
jump _NOD
_NOK_FROM_NOD:
mul r3 r4
div r3 r0
jump _MAIN_LOOP_RET

; r7 res
; r8 iter
_MAIN:
ldc r7 1
ldc r8 1
_MAIN_LOOP:
inc r8
mov r3 r7
mov r4 r8
jump _NOK
_MAIN_LOOP_RET:
mov r7 r3
ldc r9 20
sub r9 r8
jge r9 _MAIN_LOOP

outn r7
ldc r7 10
out r7
hlt
