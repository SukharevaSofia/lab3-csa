# Lab

## Вариант
- Сухарева Софья Сергеевна P33131
- Упрощённый
- asm | risc | harv | hw | instr | struct | stream | port | pstr | prob5

## Язык программирования
Язык ассемблера

Стратегия вычисления: последовательное исполнение инструкций ассемблера
Виды литералов: инструкции, строки, числа

Пример:
```asm
; all labels start with _
; r0 - addr of hello world, is an iter to string
; r1 length of hello world
; r2 - current symbol
    ldc r0 HELLO_WORLD ; load constant
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
    jge r1 _LOOP ; jump if greater or equal
    hlt

HELLO_WORLD: "Hello World!"
```

## Организация памяти
- Отдельная память для инструкций и данных
- 16 регистров по 8 байт
- Прямая адресация
- Хранение строк: загрузка в data memory при загрузке VM, храняться в виде паскаль строк
- Отображение программы на процессор: данные из структуры загружаются в две памяти с нулевых аддресов последовательно

### Строковые литералы
- Pascal строки
- Загружаются в начало data memory последовательно

## Система команд
- RISC
- Операции имеющие доступ к data memory: ld, sv

Цикл команд:
- Загрузка PC
- Получение инструкции из program memory по PC
- Инкремент PC
- Декодирование инструкции
- Выполнение команды

Набор инструкций:
- jump - безусловный переход к аргументу
- jge - переход к аргументу два при аргументе один >=0
- jne - переход к аргументу два при аргументе один !=0
- jeq - переход к аргументу два при аргументе один ==0
- in - прочтение из устройства ввода в указанный регистр
- out - запись из регистра в устройство вывода
- outn- numeric запись из регистра в устройство вывода
- mov - move из регистра 2 в рег 1
- ldc - загружает в регистр-арг1 коснтанту-арг2
- ld - загружает в рег1 из адреса2
- sv - сохраняет в адр1 из р2г
- inc - инкремент регистра
- dec - декремент регистра
- add - добавить регистр 2 к регистру 1
- sub - отнять регистр 2 от регистра 1
- mul - умножить регистр 1 на регистр 2
- div - разделить регистр 1 на регистр 2
- mod - остаток от деления регистра 1 на рег 2
- hlt - остановка модели

## Транслятор
```
python translator.py input_source output_bin
```

## Модель
```
python vm.py input_bin input_text
```

ControlUnit
```
      +1increment                                      
┌──────────────────────┐                               
│                      │                               
│                      │                               
│                      │          ┌──────────────┐     
│           ┌──────────┴─────────►│programmemory │     
│           │                     └┬─────────────┘     
│      ┌────┴─────────┐            │                   
│    ┌►│programcounter│            │                   
│    │ └──────────────┘            │                   
│    │                             │                   
│   ┌┴──┐                          │                   
└──►│MUX│                          ▼                   
    └───┘                    ┌───────┐                 
      ▲        ┌─────────────┤decoder│◄───┐            
      │        │             └─────┬─┘    │registers   
      └────────┘                   │      │            
        select next instr        signals  │            
                                   │      │            
                   ┌─────┐        ┌▼──────┴┐   ┌──────┐
                   │input├───────►│datapath├──►│output│
                   └─────┘        └────────┘   └──────┘
```


DataPath
```
             ┌───────────────────────────────────────────────┐       
             ▼                                               │       
     ┌───────────┐                  address                  │       
     │controlunit│                 ┌────────┐                │       
     └┬─────────┬┘                 │        │                │       
direct│         │                  ▼        │                │       
writes│         │          ┌───────────┐    │                │       
      │  ┌──────┼──────────┤DataMemory │    │                │       
      │  │      │          └───────────┘ ┌──┴────────┐       │       
      │  │      │                        │DataAddress│       │       
      │  │      └─────────────┐          └──┬────────┘       │       
      │  │                    │             │                │       
      │  │                  latch           │                │       
      │  │                 signals          │                │       
      │  │                    ┌─────────────┼────┐ ┌─────────┴──────┐
      │  │                    ▼             │    │ │ registers      │
      ▼  ▼                ┌────────────┐    │    └─┤                │
    ┌────────┐ left/right │            │    │      │                │
    │        ├───────────►│   ALU      │    │      └────────────────┘
    │MUX     │            │            │    │               ▲        
    │        │            │            │    │               │        
    │        │            └──────┬─────┘    │               │        
    └────────┘                   │          │               │        
      ▲                          ▼     ┌────┘               │        
      │                      ┌────────┬┘                    │        
   ┌──┴──┐                   │        │      ┌──────────┐   │        
   │input│                   │ MUX    ├────► │ output   │   │        
   └─────┘                   │        │      └──────────┘   │        
                             └─────┬──┘                     │        
                                   │                        │        
                                   │                        │        
                                   └────────────────────────┘        
```

## Тестирование

- Разработанные тесты проверяют функционал языка на узких местах
- CI загружает нужные библиотеки для работы, запускает golden тесты и линтер.
- Общее покрытие тестами - 93%

### hello.s
```hello.s
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
```

### cat.s
```cat.s
_LOOP:
  in r0
  out r0
  jump _LOOP
  hlt
```


#### hello_user_name.s

```hello_user_name.s
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
```

### prob5.s

```prob5.s
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

```

### example.s

```example.s
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
```
## Работа разработанных алгоритмов

- разбор на примере программы hello.s

### hello.s
```hello.s
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
```

### struct

```hello.json
{
  "program": [
    {
      "instr": "ldc",
      "args": [
        0,
        0
      ]
    },
    {
      "instr": "ld",
      "args": [
        1,
        0
      ]
    },
    {
      "instr": "dec",
      "args": [
        1
      ]
    },
    {
      "instr": "inc",
      "args": [
        0
      ]
    },
    {
      "instr": "ld",
      "args": [
        2,
        0
      ]
    },
    {
      "instr": "out",
      "args": [
        2
      ]
    },
    {
      "instr": "dec",
      "args": [
        1
      ]
    },
    {
      "instr": "jge",
      "args": [
        1,
        3
      ]
    },
    {
      "instr": "hlt",
      "args": []
    }
  ],
  "data": [
    {
      "variable_data": "Hello World!"
    }
  ]
}
```
### debug



```debug
DEBUG   vm:primary_loop  
ControlUnit: IP=0 DataPath: regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 0, instr: ldc, args: [0, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=1 DataPath: regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 1, instr: ld, args: [1, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=2 DataPath: regs = [0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 2, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=3 DataPath: regs = [0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 3, instr: inc, args: [0]

DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [1, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [1, 11, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [1, 11, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=7 DataPath: regs = [1, 10, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 7, instr: jge, args: [1, 3]

DEBUG   vm:primary_loop  
ControlUnit: IP=3 DataPath: regs = [1, 10, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 3, instr: inc, args: [0]

DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [2, 10, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [2, 10, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [2, 10, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=7 DataPath: regs = [2, 9, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 7, instr: jge, args: [1, 3]

DEBUG   vm:primary_loop  
ControlUnit: IP=3 DataPath: regs = [2, 9, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 3, instr: inc, args: [0]

DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [3, 9, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [3, 9, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [3, 9, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=7 DataPath: regs = [3, 8, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 7, instr: jge, args: [1, 3]

DEBUG   vm:primary_loop  
ControlUnit: IP=3 DataPath: regs = [3, 8, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 3, instr: inc, args: [0]

DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [4, 8, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [4, 8, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [4, 8, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=7 DataPath: regs = [4, 7, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 7, instr: jge, args: [1, 3]

DEBUG   vm:primary_loop  
ControlUnit: IP=3 DataPath: regs = [4, 7, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 3, instr: inc, args: [0]

DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [5, 7, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [5, 7, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [5, 7, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]



DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [11, 1, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [11, 1, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [11, 1, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=7 DataPath: regs = [11, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 7, instr: jge, args: [1, 3]

DEBUG   vm:primary_loop  
ControlUnit: IP=3 DataPath: regs = [11, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 3, instr: inc, args: [0]

DEBUG   vm:primary_loop  
ControlUnit: IP=4 DataPath: regs = [12, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 4, instr: ld, args: [2, 0]

DEBUG   vm:primary_loop  
ControlUnit: IP=5 DataPath: regs = [12, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 5, instr: out, args: [2]

DEBUG   vm:primary_loop  
ControlUnit: IP=6 DataPath: regs = [12, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 6, instr: dec, args: [1]

DEBUG   vm:primary_loop  
ControlUnit: IP=7 DataPath: regs = [12, -1, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 7, instr: jge, args: [1, 3]

DEBUG   vm:primary_loop  
ControlUnit: IP=8 DataPath: regs = [12, -1, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
address: 8, instr: hlt, args: []

INFO    vm:simulation    output_buffer: ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd', '!']
```

- [hello.s golden test](https://github.com/SukharevaSofia/lab3-csa/blob/main/golden/hello.yml)
- [cat.s golden test](https://github.com/SukharevaSofia/lab3-csa/blob/main/golden/cat.yml)
- [hello_user_name.s golden test](https://github.com/SukharevaSofia/lab3-csa/blob/main/golden/hello_user_name.yml)
- [prob5.s golden test](https://github.com/SukharevaSofia/lab3-csa/blob/main/golden/prob5.yml)
- [example.s golden test](https://github.com/SukharevaSofia/lab3-csa/blob/main/golden/example.yml)

