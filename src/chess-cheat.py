#!/usr/bin/env python

DELAY = 100
DRAW_ALPHA = 0.3
ARROW_ALPHA = 0.6

from pyscreenshot import grab
from stockfish import Stockfish
import tkinter as tk
from chess_cheat_utils.board import Board
from timeout_decorator import timeout, TimeoutError
from multiprocessing import cpu_count
from math import atan2, sin, cos
from PIL import Image
from os import remove
from functools import lru_cache

def reorder_rect(x1, y1, x2, y2):
	nx1 = min(x1, x2)
	ny1 = min(y1, y2)
	nx2 = max(x1, x2)
	ny2 = max(y1, y2)
	return nx1, ny1, nx2, ny2

def arrow(r, a, move, corners, active):
	if not move: return
	dx = (corners[2] - corners[0]) // 8
	dy = (corners[3] - corners[1]) // 8
	dx2 = dx // 2
	dy2 = dy // 2
	dx3 = dx // 3
	dy3 = dy // 3
	corners[0] += r.bx1
	corners[1] += r.by1
	corners[2] += r.bx1
	corners[3] += r.by1
	move = [ord(move[0])-97, int(move[1])-1, ord(move[2])-97, int(move[3])-1]
	if active == 'b':
		move = [7 - v for v in move]
	move[1] = 7 - move[1]
	move[3] = 7 - move[3]
	move = [int(corners[0] + v*dx + dx2) if i % 2 == 0 else int(corners[1] + v*dy + dy2) for i, v in enumerate(move)]

	x1 = min(move[0], move[2])
	y1 = min(move[1], move[3])
	x2 = max(move[0], move[2])
	y2 = max(move[1], move[3])
	x = False
	y = False
	if x1 == x2:
		x1 -= dx3
		x2 += dx3
	if y1 == y2:
		y1 -= dy3
		y2 += dy3
	alpha = atan2(y2 - y1, x2 - x1)
	x1 += int(dx3 * cos(alpha))
	y1 += int(dy3 * sin(alpha))
	x2 -= int(dx3 * cos(alpha))
	y2 -= int(dy3 * sin(alpha))
	x_size = x2 - x1
	y_size = y2 - y1

	if move[0] < move[2]:
		ax1 = 0
		ax2 = x_size
	elif move[0] > move[2]:
		ax1 = x_size
		ax2 = 0
	else:
		ax1 = ax2 = x_size // 2
	if move[1] < move[3]:
		ay1 = 0
		ay2 = y_size
	elif move[1] > move[3]:
		ay1 = y_size
		ay2 = 0
	else:
		ay1 = ay2 = y_size // 2

	a.c.delete('all')
	a.c.create_rectangle(0, 0, x_size, y_size, fill='white')
	a.c.create_line(ax1, ay1, ax2, ay2, arrow=tk.LAST, arrowshape=(30,40,20), width=10)
	a.geometry('{}x{}+{}+{}'.format(x_size, y_size, x1, y1))
	a.c.dx = x1
	a.c.dy = y1
	a.c.x_size = x_size
	a.c.y_size = y_size
	a.deiconify()

def init_arrow(r):
	a = tk.Toplevel(r)
	a.overrideredirect(True)
	a.wait_visibility(a)
	a.attributes('-alpha', ARROW_ALPHA)
	a.attributes('-topmost', True)
	a.geometry('0x0')

	c = tk.Canvas(a)
	c.dx = c.dy = c.x_size = c.y_size = 0
	c.pack(fill=tk.BOTH, expand=True)
	a.c = c
	return a

def init_draw(r):
	d = tk.Toplevel(r)
	d.wait_visibility(d)
	d.attributes('-fullscreen', True)
	d.attributes('-alpha', DRAW_ALPHA)
	d.attributes('-topmost', True)

	c = tk.Canvas(d)
	r.bx1, r.by1, r.bx2, r.by2 = 0, 0, 0, 0
	d.bx1, d.by1, d.bx2, d.by2 = 0, 0, 0, 0

	def save_boundaries():
		r.bx1, r.by1, r.bx2, r.by2 = reorder_rect(d.bx1, d.by1, d.bx2, d.by2)

	def down(e):
		d.bx1, d.by1 = e.x, e.y
		save_boundaries()
		c.delete('all')
	def move(e):
		d.bx2, d.by2 = e.x, e.y
		save_boundaries()
		c.delete('all')
		c.create_rectangle(r.bx1, r.by1, r.bx2, r.by2, width=10)
	def up(e):
		d.bx2, d.by2 = e.x, e.y
		save_boundaries()
		c.delete('all')
		c.create_rectangle(r.bx1, r.by1, r.bx2, r.by2, width=10)
		d.withdraw()
		r.paused = False

	c.bind('<Button-1>', down)
	c.bind('<B1-Motion>', move)
	c.bind('<ButtonRelease-1>', up)

	c.pack(fill=tk.BOTH, expand=True)
	d.withdraw()
	return d

def init_window():
	r = tk.Tk()
	r.title('Chess-Cheat')
	r.minsize(190, 20)
	r.attributes('-topmost', True)
	r.paused = False
	r.screenwidth = r.winfo_screenwidth()
	r.screenheight = r.winfo_screenheight()

	v = tk.StringVar()
	white = tk.Radiobutton(r, text='White', variable=v, value='w', indicatoron=0)
	black = tk.Radiobutton(r, text='Black', variable=v, value='b', indicatoron=0)
	white.select()

	l = tk.Label(r, text='')

	d = init_draw(r)

	def draw():
		r.paused = True
		d.deiconify()
	od = tk.Button(r, text='Board', command=draw)

	white.pack()
	black.pack()
	od.pack()
	l.pack()

	a = init_arrow(r)

	return r, v, l, a

def subtract(b, f, fa):
	return (b - f * fa) / (1 - fa)

def subtract_arrow(r, a, i, bounds):
	pixels = i.load()
	a.c.postscript(file='arrow.eps', pagewidth='{}p'.format(a.c.x_size))
	with Image.open('arrow.eps') as arrow:
		for x in range(arrow.size[0] - 1):
			for y in range(1, arrow.size[1]):
				x_s = int(x + a.c.dx - bounds[0])
				y_s = int(y + a.c.dy - bounds[1])
				if x_s >= 0 and y_s >= 0 and x_s < i.size[0] and y_s < i.size[1]:
					pixels[x_s,y_s] = tuple(map(lambda pair: int(subtract(pair[0], pair[1], ARROW_ALPHA)), zip(pixels[x_s,y_s], arrow.getpixel((x,y)))))
	remove('arrow.eps')
	return i

def screenshot(r, a):
	bounds = (0, 0, r.screenwidth, r.screenheight) 
	if (r.bx1 or r.by1 or r.bx2 or r.by2) and r.bx1 != r.bx2 and r.by1 != r.by2:
		bounds = (r.bx1, r.by1, r.bx2, r.by2)
		i = grab(bbox=bounds)
	else:
		i = grab()
	return subtract_arrow(r, a, i, bounds)

@timeout(.7, use_signals=False)
@lru_cache
def run_fish(s, fen):
	return s.get_best_move()

def cheat(r, v, l, a, s, b):
	if not r.paused:
		fen, corners = b.fen(screenshot(r, a), v.get())

		#print('Corners: {}'.format(corners))
		#print('FEN: {}'.format(fen))

		if fen:
			s.set_fen_position(fen)
			try:
				move = run_fish(s, fen)
			except TimeoutError:
				s = create_fish()
				r.configure(background='red')
			else:
				#print('Move: {}'.format(move))
				l.config(text=move)
				r.configure(background='green')
				arrow(r, a, move, corners, v.get())
		else:
			r.configure(background='red')

	r.after(DELAY, cheat, r, v, l, a, s, b)

def create_fish():	
	s = Stockfish(parameters={'Threads':cpu_count(), 'Minimum Thinking Time': 500})
	return s

def main():
	s = create_fish()
	b = Board()
	r, v, l, a = init_window()
	r.after(100, cheat, r, v, l, a, s, b)
	r.mainloop()
	b.close()

if __name__ == '__main__':
	main()
