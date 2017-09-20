from machine.constants import *

class GPU:

    def __init__(self, screen):
        self.screen = screen
        self.active = 0
        self.refreshed = False

    def update(self, memory):
        self.active = memory[GPU_FLAG_SEG * MEMORY_SEGMENT_SIZE + GPU_FLAG_OFFSET] & 0x1
        if self.active == 1:
            self.refreshed = not self.refreshed
            refreshed_i = int(self.refreshed)
            memory[GPU_FLAG_SEG * MEMORY_SEGMENT_SIZE + GPU_FLAG_OFFSET] &= 0xFD
            memory[GPU_FLAG_SEG * MEMORY_SEGMENT_SIZE + GPU_FLAG_OFFSET] |= (refreshed_i << 1)
        
    def draw_background(self, memory):
        color = memory[BACK_COLOR_SEG * MEMORY_SEGMENT_SIZE + BACK_COLOR_OFFSET]
        self.screen.fill(color)


    def draw_sprites(self, memory):
        for i in range(0, NUM_SPRITES):
            address = SPRITE_ATTR_SEG * MEMORY_SEGMENT_SIZE + i * SPRITE_ATTR_LENGTH
            active = memory[address] >> 7
            if active == 0:
                continue
            flipHor = memory[address] >> 6 & 0x1
            flipVer = memory[address] >> 5 & 0x1
            color_four_alpha = memory[address] >> 4 & 0x1
            x = memory[address + 1]
            y = memory[address + 2]
            width = memory[address + 3]
            height = memory[address + 4]
            if x + width > SCREEN_WIDTH or y + height > SCREEN_HEIGHT:
                continue
            segment_address = memory[address + 5]
            byte_address = memory[address + 6]
            colors = [0] * 4
            colors[0] = memory[address + 7]
            colors[1] = memory[address + 8]
            colors[2] = memory[address + 9]
            colors[3] = memory[address + 10]
            sprite_address = segment_address * MEMORY_SEGMENT_SIZE + byte_address
            for h in range(0, height):
                for w in range(0, width // 4):
                    # todo flips
                    four_pixels = memory[sprite_address + w + (h * width // 4)]
                    c0 = (four_pixels >> 6) & 0x3
                    c1 = (four_pixels >> 4) & 0x3
                    c2 = (four_pixels >> 2) & 0x3
                    c3 = four_pixels & 0x03
                    p0 = colors[c0]
                    p1 = colors[c1]
                    p2 = colors[c2]
                    p3 = colors[c3]
                    self.screen.set_at((x + w, y + h), p0)
                    self.screen.set_at((x + w + 1, y + h), p1)
                    self.screen.set_at((x + w + 2, y + h), p2)
                    self.screen.set_at((x + w + 3, y + h), p3)
