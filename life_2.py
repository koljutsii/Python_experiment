#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	import tkinter as tk
except:
	import Tkinter as tk
	
def paint(event):	
	i = int(event.y/cell_size)
	j = int(event.x/cell_size)
	if (column > j > 0 and lines > i > 0):
		canvas.itemconfig(cell_matrix[int(i*column+j)], state=tk.NORMAL, tags=('vis','0'))

def refresh():
	shift = [-1-column,-column,1-column,-1,1,column-1,column,column+1]
	matrix_len = len(cell_matrix)
	for i in range(matrix_len):
		k = 0
		for j in shift:
			if (matrix_len > i+j >= 0):
				if (canvas.gettags(cell_matrix[i+j])[0] == 'vis'):
					k += 1
		current_tag = canvas.gettags(cell_matrix[i])[0]
		if(k == 3):
			canvas.itemconfig(cell_matrix[i], tags=(current_tag, 'to_vis'))
		elif (k <= 1 or k >= 4):
			canvas.itemconfig(cell_matrix[i], tags=(current_tag, 'to_hid'))
		elif (k == 2 and canvas.gettags(cell_matrix[i])[0] == 'vis'):
			canvas.itemconfig(cell_matrix[i], tags=(current_tag, 'to_vis'))

def repaint():
	matrix_len = len(cell_matrix)
	for i in range(matrix_len):			
		if (canvas.gettags(cell_matrix[i])[1] == 'to_hid'):
			canvas.itemconfig(cell_matrix[i], state=tk.HIDDEN, tags=('hid','0'))
		elif (canvas.gettags(cell_matrix[i])[1] == 'to_vis'):
			canvas.itemconfig(cell_matrix[i], state=tk.NORMAL, tags=('vis','0'))
			
def start_clicked():
	global stop_value
	stop_value = 1
	step()
	
def clear_clicked():
	global stop_value
	stop_value = 0
	matrix_len = len(cell_matrix)
	for i in range(matrix_len):
		canvas.itemconfig(cell_matrix[i], state=tk.HIDDEN, tags=('hid','0'))

def stop_clicked():
	global stop_value
	stop_value	= 0

def step():
	global stop_value
	if stop_value == 1:
		refresh()
		repaint()
		canvas.after(100,step)

win_width = 300
win_height = 300
button_place = 32
cell_matrix = []
cell_size = 10
column = int(win_width/cell_size)
lines = int(win_height/cell_size)
fill_color = "green"
stop_value = 0

root = tk.Tk()
root.title('Life')
root.geometry('%dx%d' % (win_width, win_height+button_place))
canvas = tk.Canvas(root, width=win_width, height=win_height, bg='grey94')
canvas.pack(fill=tk.BOTH)

frame = tk.Frame(root)
start_button = tk.Button(frame, text='Старт', command=start_clicked)
clear_button = tk.Button(frame, text='Очистить', command=clear_clicked)
stop_button = tk.Button(frame, text='Стоп', command=stop_clicked)
start_button.pack(side='left')
clear_button.pack(side='left')
stop_button.pack(side='right')
frame.pack(side='bottom')

ox = oy = 0
while oy <= win_height - cell_size:
	while ox <= win_width - cell_size:
		square = canvas.create_rectangle(ox+1, oy+1, ox+cell_size-1, oy+cell_size-1, state=tk.HIDDEN, fill=fill_color, tags=('hid','0'))
		cell_matrix.append(square)
		ox = ox + cell_size
	ox = 0
	oy = oy + cell_size
	
canvas.bind('<Button-1>', paint, '+')
canvas.bind('<B1-Motion>', paint, '+')

root.mainloop()
