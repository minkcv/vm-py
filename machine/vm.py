from machine.opcodes import *
from machine.constants import *
from machine.ipu import *
from machine.gpu import *

class VM:
    def __init__(self, code, rom, pg, screen):
        self.pg = pg
        self.regs = [0] * REGISTER_COUNT
        self.code = code
        self.memory = [0] * (MEMORY_SEGMENT_COUNT * MEMORY_SEGMENT_SIZE)
        if rom != None:
            self.memory[ROM_SEGMENT_START * MEMORY_SEGMENT_SIZE:] = rom
        self.pc = 0
        self.ipu = IPU()
        self.gpu = GPU(screen)
        self.clock = pg.time.Clock()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for event in self.pg.event.get():
                if event.type == self.pg.QUIT:
                    self.pg.quit()
                else:
                    self.ipu.update(event, self.memory)
                
            bin_instr = self.code[self.pc]
            instr = self.decode(bin_instr)
            self.exec(instr)
            self.pc += 1
            self.gpu.update(self.memory)
            if self.gpu.active == 1:
                self.gpu.draw_background(self.memory)
                self.gpu.draw_sprites(self.memory)
            self.pg.display.flip()
            self.clock.tick(60)

    def decode(self, bin_instr):
        clean = 0x000F
        instr = {
            "opcode": bin_instr >> 12 & clean,
            "arg0": bin_instr >> 8 & clean,
            "arg1": bin_instr >> 4 & clean,
            "arg2": bin_instr & clean
        }
        return instr

    def exec(self, instr):
        op = instr["opcode"]
        a0 = instr["arg0"]
        a1 = instr["arg1"]
        a2 = instr["arg2"]
        if (op == EXT):
            if (a0 == EXT_HALT):
                self.pg.quit()
                self.running = False
            elif (a0 == EXT_CPY):
                self.regs[a1] = self.regs[a2]
            elif (a0 == EXT_NOT):
                self.regs[a1] = ~self.regs[a1]
            elif (a0 == EXT_LSL):
                self.regs[a1] = self.regs[a1] << self.regs[a2]
            elif (a0 == EXT_LSR):
                self.regs[a1] = self.regs[a1] >> self.regs[a2]
            elif (a0 == EXT_JMP):
                self.pc = self.regs[a1] * JUMP_SEGMENT_SIZE + self.regs[a2] # need -1 here?
            #elif (a0 == EXT_NOP):
        elif (op == ADD):
            self.regs[a0] = self.regs[a1] + self.regs[a2]
        elif (op == SUB):
            self.regs[a0] = self.regs[a1] - self.regs[a2]
        elif (op == ADDC):
            self.regs[a0] += (a1 << 4 & 0x00F0) + a2
        elif (op == SUBC):
            self.regs[a0] -= (a1 << 4 & 0x00F0) + a2
        elif (op == CMP):
            if self.regs[a1] < self.regs[a2]:
                self.regs[a0] = 0
            elif self.regs[a1] > self.regs[a2]:
                self.regs[a0] = 2
            else:
                self.regs[a0] = 1
        elif (op == JLT):
            if self.regs[a0] == 0:
                self.pc = self.regs[a1] * JUMP_SEGMENT_SIZE + self.regs[a2]
        elif (op == JGT):
            if self.regs[a0] == 2:
                self.pc = self.regs[a1] * JUMP_SEGMENT_SIZE + self.regs[a2]
        elif (op == JEQ):
            if self.regs[a0] == 1:
                self.pc = self.regs[a1] * JUMP_SEGMENT_SIZE + self.regs[a2]
        elif (op == LDR):
            self.regs[a0] = self.memory[a1 * MEMORY_SEGMENT_SIZE + a2]
        elif (op == STR):
            if self.regs[a1] < ROM_SEGMENT_START:
                self.memory[self.regs[a1] * MEMORY_SEGMENT_SIZE + self.regs[a2]] = self.regs[a0]
            else:
                print("Attempted illegal write to ROM")
                #exit
        elif (op == LRC):
            self.regs[a0] = (a1 << 4 & 0x00F0) + a2
        elif (op == AND):
            self.regs[a0] = self.regs[a1] & self.regs[a2]
        elif (op == OR):
            self.regs[a0] = self.regs[a1] | self.regs[a2]
        elif (op == XOR):
            self.regs[a0] = self.regs[a1] ^ self.regs[a2]
            