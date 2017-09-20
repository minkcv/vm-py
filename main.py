from machine.constants import *
from machine.vm import *
import pygame
import struct
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, COLOR_DEPTH)
pygame.display.set_caption("Vapor Spec")

bin_file = open("pong.bin", "rb")
# program_length is the number of 2 byte instructions in the program
program_length = struct.unpack("H", bin_file.read(2))[0]
program_code_string = bin_file.read(program_length * 2)
code = struct.unpack("H" * (program_length), program_code_string)
rom = None
vm = VM(code, rom, pygame, screen)

vm.run()

pygame.quit()
