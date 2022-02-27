#This calculator lets you add, multiply, and divide


from tkinter import *

root = Tk()

Results = Entry(root, width=50, borderwidth=5)
Results.grid(row=0,column=0, columnspan=3, padx=10, pady=10)

def show_number(num):
	Results.insert(100, str(num))
	
def clear_input():
	Results.delete(0, END)

def add():
	Results.insert(100, ' + ')

def multiply():
	Results.insert(100, ' x ')

def divide():
	Results.insert(100, ' / ')

def equals():
	calculation = str(Results.get())
	split_calculation = calculation.split(' ')
	total = 0
	skip = "+x/"

	for i in range(len(split_calculation)):
		if split_calculation[i] in skip:
			continue
		elif split_calculation[i] == split_calculation[0]:
			try:
			    total += float(split_calculation[i])
			except TypeError:
			    total += int(split_calculation[i])
		else:
			if split_calculation[i-1] == '+':
				total += int(split_calculation[i])
			elif split_calculation[i-1] == 'x':
				total *= int(split_calculation[i])
			elif split_calculation[i-1] == '/':
				total /= int(split_calculation[i]) 
	
	Results.delete(0, 'end')
	Results.insert(1, str(total))







Button1 = Button(root,text="1", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(1))
Button2 = Button(root,text="2", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(2))
Button3 = Button(root,text="3", padx = 46, pady = 20, borderwidth=10,command= lambda: show_number(3))
Button4 = Button(root,text="4", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(4))
Button5 = Button(root,text="5", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(5))
Button6 = Button(root,text="6", padx = 46, pady = 20, borderwidth=10,command= lambda: show_number(6))
Button7 = Button(root,text="7", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(7))
Button8 = Button(root,text="8", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(8))
Button9 = Button(root,text="9", padx = 46, pady = 20, borderwidth=10,command= lambda: show_number(9))
Button0 = Button(root,text="0", padx = 40, pady = 20, borderwidth=10,command= lambda: show_number(0))
Button_add = Button(root,text="+", padx = 40, pady = 20, borderwidth=10,command= add)
Button_multiply = Button(root,text="x", padx = 101, pady = 20, borderwidth=10,command= multiply)
Button_divide = Button(root,text="/", padx = 101, pady = 20, borderwidth=10,command= divide)
Button_clear = Button(root,text="Clear", padx = 101, pady = 20, borderwidth=10,command= lambda: clear_input())
Button_equal = Button(root,text="=", padx = 40, pady = 20, borderwidth=10,command= lambda: equals())


Button1.grid(row=1,column=0)
Button2.grid(row=1,column=1)
Button3.grid(row=1,column=2)

Button4.grid(row=2,column=0)
Button5.grid(row=2,column=1)
Button6.grid(row=2,column=2)

Button7.grid(row=3,column=0)
Button8.grid(row=3,column=1)
Button9.grid(row=3,column=2)

Button0.grid(row=4,column=0)
Button_add.grid(row=5,column=0)
Button_multiply.grid(row=4,column=1, columnspan=2)
Button_divide.grid(row=5,column=1, columnspan=2)

Button_clear.grid(row=6,column=1, columnspan=2)
Button_equal.grid(row=6,column=0)



root.mainloop()