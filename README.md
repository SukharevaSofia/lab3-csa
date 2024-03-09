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
```

## Тестирование
