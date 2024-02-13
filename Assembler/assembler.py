from intelhex import IntelHex
import sys

class Assembler:
    def __init__(self):
        self.labels = {}
        self.instructions = []
        self.current_address = 1

    def parse_line(self, line):
        line = line.upper()
        opcode, *args = line.split()
        if opcode[-1] == ':':
            # This is a label
            self.labels[opcode[:-1]] = self.current_address
            return None
        else:
            # This is an instruction
            self.current_address += 2
            return (opcode, args)

    def label2uint8(self, args):
        jmp_addr = self.labels[args[1]] if args[1] in self.labels else int(args[1], 0)
        if len(args) > 2 and args[2] == 'H':
            jmp_addr = jmp_addr >> 8
        else:
            jmp_addr = jmp_addr & 0xFF
        return jmp_addr

    def assemble_line(self, opcode, args):
        for i, arg in enumerate(args):
            if arg == 'ACC' or arg == 'R0':
                args[i] = '0'
            elif arg == 'R1':
                args[i] = '1'
            elif arg == 'R2':
                args[i] = '2'
            elif arg == 'R3':
                args[i] = '3'

        if opcode == 'NOP':
            self.instructions.append((0b0000 << 12))
        elif opcode == 'JMP':
            jmp_addr = self.labels[args[0]] if args[0] in self.labels else int(args[0], 0)
            self.instructions.append((0b0001 << 12) | jmp_addr)
        elif opcode == 'BRZ':
            jmp_addr = self.labels[args[0]] if args[0] in self.labels else int(args[0], 0)
            self.instructions.append((0b0010 << 12) | jmp_addr)
        elif opcode == 'BRNZ':
            jmp_addr = self.labels[args[0]] if args[0] in self.labels else int(args[0], 0)
            self.instructions.append((0b0011 << 12) | jmp_addr)
        elif opcode == 'BRC':
            jmp_addr = self.labels[args[0]] if args[0] in self.labels else int(args[0], 0)
            self.instructions.append((0b0100 << 12) | jmp_addr)
        elif opcode == 'BRNC':
            jmp_addr = self.labels[args[0]] if args[0] in self.labels else int(args[0], 0)
            self.instructions.append((0b0101 << 12) | jmp_addr)
        elif opcode == 'RJMP':
            self.instructions.append((0b0110 << 12))
        elif opcode == 'RSTORE':
            self.instructions.append((0b0111 << 12) | (0b00 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'RLOAD':
            self.instructions.append((0b0111 << 12) | (0b01 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'STORE':
            self.instructions.append((0b1000 << 12) | (0b00 << 10) | (int(args[0], 0) << 8) | int(args[1], 0))
        elif opcode == 'LOAD':
            self.instructions.append((0b1000 << 12) | (0b01 << 10) | (int(args[0], 0) << 8) | int(args[1], 0))
        elif opcode == 'MOVI':
            val = self.label2uint8(args)
            self.instructions.append((0b1000 << 12) | (0b10 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'ADDI':
            val = self.label2uint8(args)
            self.instructions.append((0b1000 << 12) | (0b11 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'SUBI':
            val = self.label2uint8(args)
            self.instructions.append((0b1001 << 12) | (0b00 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'ANDI':
            val = self.label2uint8(args)
            self.instructions.append((0b1001 << 12) | (0b01 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'ORI':
            val = self.label2uint8(args)
            self.instructions.append((0b1001 << 12) | (0b10 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'XORI':
            val = self.label2uint8(args)
            self.instructions.append((0b1001 << 12) | (0b11 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'ADDCI':
            val = self.label2uint8(args)
            self.instructions.append((0b1010 << 12) | (0b00 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'SUBBI':
            val = self.label2uint8(args)
            self.instructions.append((0b1010 << 12) | (0b01 << 10) | (int(args[0], 0) << 8) | val)
        elif opcode == 'MOV':
            self.instructions.append((0b1010 << 12) | (0b10 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'ADD':
            self.instructions.append((0b1010 << 12) | (0b11 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'SUB':
            self.instructions.append((0b1011 << 12) | (0b00 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'AND':
            self.instructions.append((0b1011 << 12) | (0b01 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'OR':
            self.instructions.append((0b1011 << 12) | (0b10 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'XOR':
            self.instructions.append((0b1011 << 12) | (0b11 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'ADDC':
            self.instructions.append((0b1100 << 12) | (0b00 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'SUBB':
            self.instructions.append((0b1100 << 12) | (0b01 << 10) | (int(args[0], 0) << 8) | (int(args[1], 0)) << 6)
        elif opcode == 'SETP':
            self.instructions.append((0b1101 << 12) | (0b00 << 10) | int(args[0], 0))
        elif opcode == 'OUT':
            self.instructions.append((0b1101 << 12) | (0b01 << 10) | (int(args[0], 0)) << 6)
        else:
            raise ValueError(f'Unknown instruction: {opcode}')

    def assemble_file(self, filename):
        with open(filename, 'r') as file:
            lines = [line.split(';')[0].strip() for line in file]
            parsed_lines = [self.parse_line(line) for line in lines if line]

        self.current_address = 1
        for parsed_line in parsed_lines:
            if parsed_line is not None:
                opcode, args = parsed_line
                self.assemble_line(opcode, args)


    def to_hex(self, filename):
        ih = IntelHex()
        ih[0] = 0
        for i, instruction in enumerate(self.instructions):
            print(f"{instruction:#018b}")
            ih[i*2+1] = (instruction >> 8) & 0xFF
            ih[i*2+2] = instruction & 0xFF

        ih.write_hex_file(filename)


asm = Assembler()

# Assemble source code file
asm.assemble_file(sys.argv[1])

# Output .hex file
asm.to_hex(sys.argv[2])
