"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    HLT = 1
    LDI = 2
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.ir = None
        self.mar = None
        self.mdr = None
        self.reg = [0] * 8
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.fl = 0b00000000
        self.running = True
        


    def load(self):
        """Load a program into memory."""
        
        address = 0
        if len(sys.argv) < 2: 
            print('nope')
            sys.exit(1)
        with open(sys.argv[1]) as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0],2)
                except ValueError:
                    continue
                self.ram[address] = v
                address += 1
        #sys.exit(0)
        # For now, we've just hardcoded a program:
        """
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        """


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
        
            if(self.reg[reg_a]>self.reg[reg_b]):
                self.fl = 0b00000010
            elif (self.reg[reg_a] < self.reg[reg_b]):
                self.fl = 0b00000100                
               
            else:
                
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        while self.running:           
            ir = self.ram[self.pc]
            if ir == 0b00000001: 
                self.running = False
                self.pc += 1
                sys.exit(1)
            elif ir == 0b10000010:
                reg_num = self.ram[self.pc+1]
                value = self.ram[self.pc+2]
                self.reg[reg_num] = value
                self.pc += 3
            elif ir == 0b01000111:
                reg_num = self.ram[self.pc+1]
                print(self.reg[reg_num])
                self.pc += 2
            elif ir == 0b10100010:
                reg_a = self.ram[self.pc+1]
                reg_b = self.ram[self.pc+2]
                self.alu('MUL',  reg_a, reg_b)
                self.pc +=3
            elif ir == 0b01000101:
                self.reg[self.sp] -= 1
                value = self.reg[self.ram[self.pc + 1]]
                top_of_stack_addr = self.reg[self.sp]
                self.ram[top_of_stack_addr] = value
                self.pc += 2
            elif ir == 0b01000110:
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
                self.pc+=2
            elif ir == 0b01010000:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                subroutine_addr = self.reg[self.pc + 1]
                self.pc = subroutine_addr
            elif ir == 0b00010001:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
            elif ir == 0b10100111:
                reg_a = self.ram[self.pc+1]
                reg_b = self.ram[self.pc+2]
                self.alu('CMP', reg_a, reg_b)
                self.pc +=3
            elif ir == 0b01010100:
                self.pc = self.reg[self.ram[self.pc + 1]]
            elif ir == 0b01010101:
                if self.fl == 0b00000001:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2
            elif ir == 0b01010110:
                if self.fl != 0b00000001:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2
            elif ir == 0b10101000:
                self.reg[self.ram[self.pc + 1]] = self.reg[self.ram[self.pc + 1]] & self.reg[self.ram[self.pc + 2]]
                self.pc += 3
            elif ir == 0b10101010:
                self.reg[self.ram[self.pc + 1]] = self.reg[self.ram[self.pc + 1]] | self.reg[self.ram[self.pc + 2]]
                self.pc += 3
            




            


        pass
    

    def ram_read(addr):
        return self.ram[addr]

    def ram_write(value, addr):
        self.ram[addr] = value 
        return 
    # credit for this function is due to lucidprogramming's channel on yt
    def toggle_nth_bit(self, x:int, n:int):
        return x ^ (1 << n)

