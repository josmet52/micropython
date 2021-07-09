#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : tft_lobo_ttgo.py.py
----------------------------
use the tft display with examples
More details on : https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/display

CLASS : tft_lobo_ttgo
PROCESSOR : ESP32
OS : loboris micropython
uC : TTGO T-DISPLAY ESP32
Display type : ST 7789V 135x240

22.05.2021
jmb52.dev@gmail.com
"""

import display
import utime

class tft_lobo_ttgo:
    
    def __init__(self, padding=0):
        
        tft = display.TFT()
        tft.init(tft.ST7789, bgr=False, rot=tft.LANDSCAPE, miso=17, backl_pin=4, backl_on=1, mosi=19, clk=18, cs=5, dc=16,)
        tft.tft_writecmd(0x21) # correct the colors
        tft.setwin(40, 52, 279, 186) # adjust the size of the windows for the display 135x240
        self.tft = tft
        self.screen_width, self.screen_height = self.tft.winsize()  # get the size of the tft and initilize it
        
        self.COLORS = [[tft.BLACK, 'BLACK'], # 0
                  [tft.NAVY, 'NAVY'], # 1
                  [tft.DARKGREEN, 'DARKGREEN'], # 2
                  [tft.DARKCYAN, 'DARKCYAN'], # 3
                  [tft.MAROON, 'MAROON'], # 4
                  [tft.PURPLE, 'PURPLE'], # 5
                  [tft.OLIVE, 'OLIVE'], # 6
                  [tft.LIGHTGREY, 'LIGHTGREY'], # 7
                  [tft.DARKGREY, 'DARKGREY'], # 8
                  [tft.BLUE, 'BLUE'], # 9
                  [tft.GREEN, 'GREEN'], # 10
                  [tft.CYAN, 'CYAN'], # 11
                  [tft.RED, 'RED'], # 12
                  [tft.MAGENTA, 'MAGENTA'], # 13
                  [tft.YELLOW, 'YELLOW'], # 14
                  [tft.WHITE, 'WHITE'], # 15
                  [tft.ORANGE, 'ORANGE'], # 16
                  [tft.GREENYELLOW, 'GREENYELLOW'], # 17
                  [tft.PINK, 'PINK']] # 18
        self.FONTS = [[tft.FONT_Default, 'FONT_Default'], # size 13
                      [tft.FONT_DefaultSmall, 'FONT_DefaultSmall'], # size 10
                      [tft.FONT_DejaVu18, 'FONT_DejaVu18'], # size 19
                      [tft.FONT_DejaVu24, 'FONT_DejaVu24'], # size 24
                      [tft.FONT_Ubuntu, 'FONT_Ubuntu'], # size 15
                      [tft.FONT_Comic, 'FONT_Comic'], # size  25
                      [tft.FONT_Minya, 'FONT_Minya'], # size 20
                      [tft.FONT_Tooney, 'FONT_Tooney'], # size 32
                      [tft.FONT_Small, 'FONT_Small']]#, # size 8

    def clear_screen(self):
        self.tft.clear()
        
    def write_text(self, x=0, y=0, txt='missing test', color=None):
        if color == None:
            color = self.tft.YELLOW
        self.tft.text(x, y, txt, color)        
        
    def draw_rect(self, x_min=0, y_min=0, x_max=None, y_max=None , color=None):
        if x_max == None:
            x_max = self.screen_width
        if y_max == None:
            y_max = self.screen_height
        if color == None:
            color = self.tft.YELLOW
        self.tft.rect(x_min, y_min, x_max, y_max, color)
        
    def draw_line(self, x0=0, y0=0, x1=None, y1=None , color=None):
        if x1 == None:
            x1 = self.screen_width
        if y1 == None:
            y1 = self.screen_height
        if color == None:
            color = self.tft.YELLOW
        self.tft.line(x0, y0, x1, y1, color)
        
    def draw_circle(self, x=None, y=None, r=None , color=None, fill=None):
        if x == None:
            x = int(self.screen_width / 2)
        if y == None:
            y = int(self.screen_height / 2)
        if r == None:
            r = int(self.screen_height / 2)
        if color == None:
            color = self.tft.BLUE
        if fill == None:
            self.tft.circle(x, y, r, color)
        else:
            fill = self.tft.ORANGE
            self.tft.circle(x, y, r, color, fill)

    def draw_ellipse(self, x=None, y=None, rx=None, ry=None , color=None, fill=None):
        if x == None:
            x = int(self.screen_width / 2)
        if y == None:
            y = int(self.screen_height / 2)
        if rx == None:
            rx = int(self.screen_width / 2)
        if ry == None:
            ry = int(self.screen_height / 2)
        if color == None:
            color = self.tft.GREEN
        if fill == None:
            self.tft.ellipse(x, y, rx, ry, 15, color)
        else:
            fill = self.tft.MAGENTA
            self.tft.ellipse(x, y, rx, ry, 15, color, fill)

    def draw_triangle(self, x0=None, y0=None, x1=None, y1=None, x2=None, y2=None , color=None, fill=None):
        if x0 == None:
            x0 = 0
        if y0 == None:
            y0 = 0
        if x1 == None:
            x1 = int(self.screen_width / 2)
        if y1 == None:
            y1 = int(self.screen_height)
        if x2 == None:
            x2 = int(self.screen_width)
        if y2 == None:
            y2 = 0
        if color == None:
            color = self.tft.WHITE
        if fill == None:
            self.tft.triangle(x0, y0, x1, y1, x2, y2 ,color)
        else:
            fill = self.tft.LIGHTGREY
            self.tft.triangle(x0, y0, x1, y1, x2, y2 ,color, fill)
"""
Application example to use the display
with call off major functionalities.
More details on : https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/display
"""

if __name__ == '__main__':
    
    my_tft = tft_lobo_ttgo()  # initialize the class tft_lobo_ttgo
    utime.sleep(2)
    
    n_lines = 3 # define the number of lines on the display for the caclulus of vertical centering
    pad = 4 # space between two lines on the display
    screen_width, screen_height = my_tft.tft.winsize() # get the size of the tft screen
    
    while True:
    
        # draw two rectangles one smaller than the other
        my_tft.draw_rect()
        my_tft.draw_rect(pad, pad, screen_width - 2 * pad, screen_height - 2 * pad, my_tft.tft.RED)
        
        # draw two lines crossing
        my_tft.draw_line()
        my_tft.draw_line(pad, screen_height, screen_width, pad, my_tft.tft.RED)
        
        # draw some geometrical figures
        my_tft.draw_circle()
        my_tft.draw_ellipse()
        my_tft.draw_triangle()
        
        # write welcome text with default font
        txt = "ESP32 with Micropython!"
        my_tft.tft.text(
            int(screen_width/2)-int(my_tft.tft.textWidth(txt)/2),
            int(screen_height/2)-int(my_tft.tft.fontSize()[1]/2),
            txt,
            my_tft.COLORS[11][0])
        utime.sleep(2)
    
        # browse all the fonts and colors to appreciate the effect on the tft screen 
        my_tft.clear_screen()
        # use the font list
        for f in my_tft.FONTS:
            # use the colors list
            for c in my_tft.COLORS:
                
                my_tft.tft.font(f[0], color=c[0]) # select font and color
                font_height = my_tft.tft.fontSize()[1] # get the font height
                y0 = int((screen_height - (n_lines * font_height) - ((n_lines - 1) * pad)) / 2)
                
                for n_line in range(n_lines):
                    y_pos = y0 + n_line * (font_height + pad)
                    
                    if n_line == 0:
                        txt = f[1] # write the name of the used font
                        x_pos = int(screen_width/2) - int(my_tft.tft.textWidth(txt)/2) 
                        my_tft.write_text(x_pos, y_pos, txt, c[0])
                        
                    elif n_line == 1:
                        txt = 'size ' + str(my_tft.tft.fontSize()[0]) # write the size of the font
                        x_pos = int(screen_width/2) - int(my_tft.tft.textWidth(txt)/2) 
                        my_tft.write_text(x_pos, y_pos, txt, c[0])
                        
                    elif n_line == 2:
                        txt = c[1] # write the used color
                        x_pos = int(screen_width/2) - int(my_tft.tft.textWidth(txt)/2) 
                        my_tft.write_text(x_pos, y_pos, txt, c[0])
                    
#                 print(f[1] + ' - ' + c[1] + ' - ' + 'size ' + str(my_tft.tft.fontSize()[0]))
                utime.sleep(0.1)
                my_tft.clear_screen()
            print()

