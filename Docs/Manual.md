# Programmer's Manual

This guide provides an in-depth overview of the assembly language instructions, memory model, and execution model. It is designed to enable programmers to start developing software for this unique CPU architecture.

## Execution Cycle Overview

Every instruction requires exactly 3 clock cycles.
This uniformity simplifies timing and performance calculations for programs.

## Registers

The CPU contains four registers, each serving a specific purpose:

1. **ACC (Accumulator):** Primary register for arithmetic and logic operations.
2. **R1, R2, R3 (General Purpose):** Can be used for data storage, addressing, and intermediate calculations.
3. **Flags (zero, carry/borrow)** are not directly accessible from software, but can affect other instructions.
4. **Program counter** is not directly accessible from software.

## Memory Architecture

- **RAM:** 2048 bytes, divided into 8 pages of 256 bytes each. Addresses are 8-bit within each page.
- **ROM (Program Memory):** 4096 bytes, addressed with a 12-bit address space, used to store the program code.

## Labels and Comments

- **Labels:** Defined by any line ending with a colon (:). They serve as markers or pointers to specific lines in the code for jumps and branches. Also, can be used as constant for immediate instructions.
- **Comments:** Any text following a semicolon (;) on a line is treated as a comment and ignored by the assembler.

## Assembler

Requires python 3 and intelhex (_pip install intelhex)_ to be installed.

**Usage:** _python assembler.py source\_file.asm out\_file.hex_

## Instruction Set

### Flow Control

**NOP**

- **Arguments:** None.
- **Purpose:** Performs no operation for one instruction cycle.
- **Example:** NOP ; This line does nothing

**JMP**

- **Arguments:** Address (12-bit) or Label.
- **Purpose:** Unconditionally jumps to the specified memory address or label.
- **Example:** JMP 0x0A3 ; Jumps to address 0x0A3 or JMP LOOP\_END ; Jumps to the label LOOP\_END

**BRZ**

- **Arguments:** Address (12-bit) or Label.
- **Purpose:** Branches to the specified address or label if the result of the last arithmetic or logical operation is zero.
- **Example:** BRZ ZERO\_LABEL ; Branch if last result was zero

**BRNZ**

- **Arguments:** Address (12-bit) or Label.
- **Purpose:** Branches to the specified address or label if the result of the last arithmetic or logical operation is not zero.
- **Example:** BRNZ CONTINUE ; Branch if last result was not zero

**BRC**

- **Arguments:** Address (12-bit) or Label.
- **Purpose:** Branches to the specified address or label if the last operation resulted in a carry.
- **Example:** BRC CARRY\_LABEL ; Branch if there was a carry

**BRNC**

- **Arguments:** Address (12-bit) or Label.
- **Purpose:** Branches to the specified address or label if the last operation did not result in a carry.
- **Example:** BRNC NO\_CARRY ; Branch if there was no carry

**RJMP**

- **Arguments:** None.
- **Purpose:** Jumps to an address specified by combining R2 and R3 (R2 as the high byte and R3 as the low byte). Can be used to return from subroutine. Save return address before jump to subroutine, then use RJMP to return.
- **Example:** RJMP ; Jump to address specified by R2:R3

### Memory Operations

**RSTORE**

- **Arguments:** Source Register, Register with RAM Address.
- **Purpose:** Writes the content of a source register to a RAM address contained in another register.
- **Example:** RSTORE R1 R2 ; Store R1's content into the address stored in R2

**RLOAD**

- **Arguments:** Destination Register, Register with RAM Address.
- **Purpose:** Reads data from a RAM address contained in one register into a destination register.
- **Example:** RLOAD R1 R3 ; Load into R1 the content at the address stored in R3

**STORE**

- **Arguments:** Source Register, Destination RAM Address (8-bit).
- **Purpose:** Writes the content of a source register to a specified RAM address.
- **Example:** STORE R1 0xFF ; Store R1's content into RAM address 0xFF

**LOAD**

- **Arguments:** Destination Register, Source RAM Address (8-bit).
- **Purpose:** Reads data from a specified RAM address into a destination register.
- **Example:** LOAD R2 0xB0 ; Load into R2 the content at RAM address 0xB0

**SETP**

- **Arguments:** Constant (3-bit).
- **Purpose:** Sets the current memory page for RAM access.
- **Example:** SETP 0x5 ; Set current memory page to 5

### Data Manipulation

**MOVI**

- **Arguments:** Destination Register, Constant (8-bit) or Label, optionally the 'H' flag.
- **Purpose:** Loads a constant value into a register. You can use Label instead of numerical constant to pass a ROM address. Any given value will be truncated to 8 bit. Use 'H' flag to pass high byte of the value.
- **Example:** MOVI R1 0x1F ; Load 0x1F into R1
- **Example 2:** MOVI R1 RETURN\_LABEL ; Loads low byte of the address, pointed by RETURN\_LABEL into R1
- **Example 2:** MOVI R1 RETURN\_LABEL H ; Loads high byte of the address, pointed by RETURN\_LABEL into R1
- **Example 3:** MOVI R1 0x1A2B H ; Loads 0x1A into R1

**MOV**

- **Arguments:** Destination Register, Source Register.
- **Purpose:** Copies the value from one register to another.
- **Example:** MOV R3 R1 ; Copy R1's content into R3

**OUT**

- **Arguments:** Source Register.
- **Purpose:** Outputs the content of the specified source register, typically to an I/O device.
- **Example:** OUT R1 ; Outputs the content of R1

### Arithmetic and Logical Operations with Immediate Values

#### ADDI, SUBI, ANDI, ORI, XORI

- **Arguments:** Destination Register, Constant (8-bit) or Label, optionally the 'H' flag.
- **Purpose:** Performs the specified operation (addition, subtraction, bitwise AND, OR, XOR) between the accumulator (ACC) and a constant. The result is then stored in the destination register.
- **Example (ADDI):**ADDI R1 0x09 ; Adds 9 to ACC and stores the result in R1

#### ADDCI, SUBBI

- **Arguments:** Destination Register, Constant (8-bit) or Label, optionally the 'H' flag.
- **Purpose:** Adds or subtracts a constant to/from ACC, considering the carry or borrow flag from the previous operation. The result is stored in the destination register.
- **Example (ADDCI):**ADDCI R1 0x02 ; Adds 2 to ACC with carry and stores the result in R1
- **Note:** ADDCI and SUBBI instructions utilize the carry/borrow flag from a previous operation to perform addition or subtraction, respectively. This is particularly useful for multi-byte arithmetic operations, allowing for the propagation of carry or borrow across multiple operations.

### Arithmetic and Logical Operations with Register Values

#### ADD, SUB, AND, OR, XOR

- **Arguments:** Destination Register, Second Operand Register.
- **Purpose:** Performs the specified operation (addition, subtraction, bitwise AND, OR, XOR) between ACC and the second operand register. The result is stored in the destination register.
- **Example (ADD):**ADD R2 R3 ; Adds the content of R3 to ACC and stores the result in R2

#### ADDC, SUBB

- **Arguments:** Destination Register, Second Operand Register.
- **Purpose:** Adds or subtracts the second operand register to/from ACC, considering the carry or borrow flag from the previous operation. The result is stored in the destination register.
- **Example (ADDC):**ADDC R1 R2 ; Adds R2 to ACC with carry and stores the result in R1
- **Note:** ADDC and SUBB instructions are designed to work with the carry/borrow flag resulting from a previous operation. They enable precise control over arithmetic operations that span multiple bytes by considering the carry/borrow, thus facilitating complex calculations that require carry or borrow propagation.

**Examples**

- **Running light**
```asm
START:
MOVI ACC 1
OUT ACC
SHIFT:
ADD ACC ACC
BRZ START
OUT ACC
JMP SHIFT
```

