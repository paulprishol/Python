from tkinter import *
from tkinter.ttk import Combobox, Checkbutton

def click():
    alf = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    num = txt1.get()
    
    if txt3.get().isdigit() == False and txt3.get() != '':
        lblviv.configure(text = "НЕЛЬЗЯ, использование букв в to base")
        return
    
    if txt2.get().isdigit() == False and txt2.get() != '':
        lblviv.configure(text = "НЕЛЬЗЯ, использование букв при вводе")
        return
    
    to_base = int(comb2.get())
    if chk_state2.get() == True:
        to_base = int(txt3.get())
        
    from_base = int(comb1.get())
    if chk_state1.get() == True:
        from_base = int(txt2.get())
    
    for i in range(len(num)): # 1 вариант некорректного ввода
        if num[i] not in alf:
            lblviv.configure(text = "НЕЛЬЗЯ, использование букв при вводе")
            return    
        
    if (to_base < 2) or (to_base > 10) or (from_base < 2) or (from_base > 10): #1 вариант некорректного ввода
        lblviv.configure(text = "НЕЛЬЗЯ, работаем только с СС 2-10")
        return
    
    for i in range(len(num)): # 3 вариант некорректного ввода
        if int(num[i]) >= from_base:
            lblviv.configure(text = "НЕЛЬЗЯ, некорректный ввод")
            return
    
    # Перевод числа из произвольной СС в 10СС
    izn = num[::-1]
    if izn == '0':
        lblviv.configure(text = "Результат: 0")
        return
    ss = from_base
    ch = 0
    for i in range(len(izn)):
        ch += int(izn[i]) * ss ** i
    
    # Перевод десятичного в произвольную СС
    res = ''
    while ch != 0:
        res += str(ch % to_base)
        ch = ch // to_base   
    lblviv.configure(text = "Результат: " + str(res)[::-1])

def gasi1():
    if chk_state1.get() == True:
        comb1['state'] = 'disabled'
        txt2.configure(state = 'normal')
    else:
        comb1['state'] = "readonly"
        txt2.configure(state = 'disabled')

def gasi2():
    if chk_state2.get() == True:
        comb2['state'] = 'disabled'
        txt3.configure(state = 'normal')
    else:
        comb2['state'] = "readonly"
        txt3.configure(state = 'disabled')


window = Tk() #Окно программы
window.title("Перевод из одной СС в другую")
window.geometry('400x400')
window['bg'] = 'azure2'

 
lblviv = Label(window, text="", bg = 'azure2', font=("Arial Bold", 15)) # Вывод (переставить потом)
lblviv.place(x = 20, y = 350)


lbl1 = Label(window, text="Исходное число:",  bg = 'azure2', font = ("Calibri", 13)) #Надпись №1 
lbl1.place(x = 30, y = 100)

txt1 = Entry(window, width=20, justify = RIGHT, font = ("Calibri", 13)) #Окошко для ввода №1
txt1.place(x = 165, y = 100)

lbl2 = Label(window, text="Из СС:", bg = 'azure2', font = ("Calibri", 13)) #Надпись №2 
lbl2.place(x = 105, y = 130)

comb1 = Combobox(window, width = 18, state="readonly", font = ("Calibri", 13))
comb1['values'] = (2, 8, 10)  
comb1.current(2)  #вариант по умолчанию  
comb1.place(x = 165, y = 130)

chk_state1 = IntVar()
chk1 = Checkbutton(window, text='(другая СС)', var=chk_state1, onvalue=1, offvalue=0, command = gasi1) #галочка №1 
chk1.place(x = 70, y = 160)

txt2 = Entry(window, width=20, justify = RIGHT, font = ("Calibri", 13), state = 'disabled') #Окошко для ввода №2
txt2.place(x = 165, y = 160)

lbl3 = Label(window, text="В СС:", bg = 'azure2', font = ("Calibri", 13)) #Надпись №2 
lbl3.place(x = 115, y = 190)

comb2 = Combobox(window, width = 18, state="readonly", font = ("Calibri", 13))  
comb2['values'] = (2, 8, 10)  
comb2.current(0)  #вариант по умолчанию  
comb2.place(x = 165, y = 190)

chk_state2 = IntVar()
chk2 = Checkbutton(window, text='(в другую СС)', var=chk_state2, onvalue=1, offvalue=0, command = gasi2)  
chk2.place(x = 58, y = 220)

txt3 = Entry(window, width=20, justify = RIGHT, font = ("Calibri", 13), state = 'disabled') #Окошко для ввода №3
txt3.place(x = 165, y = 220)

btn = Button(window, text="Перевести", command = click, bg = 'sky blue', font = ("Calibri", 13)) #Кнопочка
btn.place(x = 150, y = 280)

window.mainloop()
