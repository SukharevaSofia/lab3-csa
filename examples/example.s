; reads in a number as a string from input
; parses it, divides it by two and outputs that
  ldc r0 10
  ldc r1 0x30
_LOOP:
  in r2
  mov r3 r2
  sub r3 r0
  jeq r3 _EXIT

  mul r6 r0
  sub r2 r1
  add r6 r2
  jump _LOOP
_EXIT:
  ldc r2 2
  div r6 r2
  outn r6
  hlt
