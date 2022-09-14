#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:25:43 2021

@author: liuyilouise.xu
"""

from graphics import BulletinBoard, Poster
from graphics import Rectangle, Circle, TextBox

poster = Poster()
rect1 = Rectangle(10,10,"red")
rect2 = Rectangle(10,10,"red")
poster.pin(rect1, 0, 0)
poster.pin(rect2, 10, 10)
board = BulletinBoard(400, 500)
board.pin(poster, 100, 100)

element = board.element_at(100,100)
print(type(element))
element = board.element_at(105,105)
print(type(element))
element = board.element_at(100,110)
print(type(element))
element = board.element_at(110,110)
print(type(element))
element = board.element_at(110,100)
print(type(element))
element = board.element_at(101,99)
print(type(element))

#board.unpin(poster)
circ = Circle(20, "yellow")
board.pin(circ, 100, 130)

element = board.element_at(100,130)
print(type(element))
element = board.element_at(100,120)
print(type(element))
element = board.element_at(100,125)
print(type(element))
element = board.element_at(110,130)
print(type(element))
