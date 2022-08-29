from tkinter import *
from tkinter import messagebox
import random
import time
import os
import sys



def dont_closing():
    messagebox.showwarning('禁止关闭','不要在未选择难度之前关闭窗口')
    yesno=messagebox.askyesno('退出','是否退出弹球游戏')
    if yesno:
        glwindow.destroy()
        sys.exit()
        exit()

def set_length(pd_length):
    global paddle_length
    paddle_length=pd_length
    glwindow.destroy()
    return 0

def get_length():
    global glwindow
    glwindow=Tk()
    paddle_length = 100
    glwindow.title('球拍长度')
    Label(glwindow,text='球拍的长度（这将关系到游戏的难度）').grid(row=0,column=0)
    Button(glwindow,text='初学',command=lambda:set_length(150)).grid(row=1,column=1)
    Button(glwindow,text='简单',command=lambda:set_length(125)).grid(row=1,column=2)
    Button(glwindow,text='正常',command=lambda:set_length(100)).grid(row=1,column=3)
    Button(glwindow,text='老手',command=lambda:set_length(87)).grid(row=1,column=4)
    Button(glwindow,text='艰难',command=lambda:set_length(75)).grid(row=1,column=5)
    Button(glwindow,text='噩梦',command=lambda:set_length(50)).grid(row=1,column=6)
    glwindow.protocol("WM_DELETE_WINDOW", dont_closing)
    glwindow.mainloop()

class Ball:
    def __init__(self,cv,paddle,color):
        self.canvas = cv
        self.paddle = paddle
        self.id = cv.create_oval(10,10,25,25,fill=color)
        self.canvas.move(self.id,200,100)
        starts = [-3,-2,-1,1,2,3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height=self.canvas.winfo_height()
        self.canvas_width=self.canvas.winfo_width()
        self.hit_bottom = False
    
    def hit_paddle(self,pos):
        global score
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                score += 1
                return True
        return False
    
    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True

class Paddle:
    def __init__(self,cv,color):
        self.canvas = cv
        self.id = cv.create_rectangle(0,0,paddle_length,10,fill = color)
        self.canvas.move(self.id,200,300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)
    
    def draw(self):
        self.canvas.move(self.id,self.x,0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0
    
    def turn_left(self,evt):
        self.x = -2
    
    def turn_right(self,evt):
        self.x = 2

def main():
    global score
    get_length()
    root=Tk()
    root.title("弹球游戏")
    root.resizable(0,0)
    score = 0
    cv = Canvas(root, width = 500, height = 400, bd = 0, highlightthickness = 0)
    background = PhotoImage(file='background.gif')
    cv.create_image(250,200,image=background)
    cv.pack()
    root.update()

    paddle = Paddle(cv,"green")
    ball = Ball(cv,paddle,"red")
    time.sleep(3)
    while True:
        if ball.hit_bottom == False:
            ball.draw()
            paddle.draw()
        else:
            messagebox.showinfo(title = '游戏结束',message='你的分数为'+str(score))
            yesno=messagebox.askyesno('再玩一次','是否要再玩一次？')
            if yesno:
                os.system('start 弹球游戏.py')
            root.destroy()
            break
        root.update_idletasks()
        root.update()
        time.sleep(0.001)
    sys.exit()
    exit()
if __name__ == '__main__':
    main()
