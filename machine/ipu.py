from machine.constants import *

class IPU:
    def __init__(self, pg):
        self.j1_buttons = [
            pg.K_UP,
            pg.K_DOWN,
            pg.K_LEFT,
            pg.K_RIGHT,
            pg.K_RCTRL,
            pg.K_RALT,
            pg.K_RSHIFT,
            pg.K_RETURN
        ]
        self.j2_buttons = [
            pg.K_w,
            pg.K_s,
            pg.K_a,
            pg.K_d,
            pg.K_LCTRL,
            pg.K_LALT,
            pg.K_LSHIFT,
            pg.K_TAB
        ]

    def update(self, pg, memory):
        joystick1 = memory[JOYSTICK_SEG * MEMORY_SEGMENT_SIZE + JOYSTICK_1_OFFSET]
        joystick2 = memory[JOYSTICK_SEG * MEMORY_SEGMENT_SIZE + JOYSTICK_2_OFFSET]
        joystick1 = self.update_joystick(pg, self.j1_buttons, joystick1)
        joystick2 = self.update_joystick(pg, self.j2_buttons, joystick2)
        memory[JOYSTICK_SEG * MEMORY_SEGMENT_SIZE + JOYSTICK_1_OFFSET] = joystick1
        memory[JOYSTICK_SEG * MEMORY_SEGMENT_SIZE + JOYSTICK_2_OFFSET] = joystick2
        
    def update_joystick(self, pg, buttons, joystick):
        for i in range(0, 8):
            if pg.key.get_pressed()[buttons[i]] != 0:
                joystick |= 1 << i
            else:
                joystick &= ~(1 << i)
        
        return joystick