from cmu_112_graphics import *
import random
from tkinter import *

# Programmer: chengzhi zhang(chengzhz)

# now I only have click and draw feature, but in the future I'll use drag and drop

# Feature1: drag and drop widgets to put on UI mock up. If not put on mock-up, then pop
# Feature2: hit bake button and it will show how it looks on a real phone by using mock-up
# Feature3: Color palette feature for choosing, and will match the other two colors for you
# Feature4: Back and force menu for go forward and backward
# Feature5: able to customize round corner

##########################################
# Intro Mode
##########################################

def IntroMode_redrawAll(app, canvas):
    font = ("Courier", 18)

    canvas.create_text(app.width/2, 150, text='UI designer',
                       font=("Courier", 24), fill='black')

    canvas.create_rectangle(app.width/4, 200, app.width/4+140, 250, fill="orange", width=0)
    canvas.create_text(app.width/4, 200,
                       text='my designs',
                       fill='black', font=font, anchor="nw")

    canvas.create_rectangle(2*app.width/4, 200, 2*app.width/4+140, 250, fill="orange", width=0)
    canvas.create_text(2*app.width/4, 200, text='instructions',
                       fill='black', font=font, anchor="nw")

    canvas.create_rectangle(3*app.width/4, 200, 3*app.width/4+140, 250, fill="orange", width=0)
    canvas.create_text(3*app.width/4, 200, text='start',
                       fill='black', font=font, anchor="nw")

def IntroMode_mousePressed(app, event):
    if 3*app.width/4 <= event.x <= 3*app.width/4+140 and 200 <= event.y <= 250:
        app.mode = 'mainMode'

##########################################
# Main Mode
##########################################

def mainMode_redrawAll(app, canvas):
    canvas.create_image(app.width * 1/3, app.margin * 4, image=ImageTk.PhotoImage(app.mockUp), anchor="nw")
    canvas.create_image(app.width * 2/3, app.margin * 4, image=ImageTk.PhotoImage(app.mockUp), anchor="nw")
    canvas.create_image(200, 400, image=ImageTk.PhotoImage(app.colorPicker), anchor="nw")
    canvas.create_image(20, 400, image=ImageTk.PhotoImage(app.colorWheel), anchor="nw")
    for widget in app.widgets:
        widget.redraw(app, canvas)
    drawWidgetsBox(app, canvas)
    drawUIBox(app, canvas)
    drawInstructions(app, canvas)
    # drawGrid(app,canvas)

def mainMode_mousePressed(app, event):
    # if click on a widget , then use that widget

    if 890 <= event.x and 560 <= event.y:
        app.mode = 'bakeMode'
    else:
        app.widgets.append(chooseRandomWidget(app, event))




def mainMode_keyPressed(app, event):
    if (event.key == 'p'):
        app.mode = 'IntroMode'
    if (event.key == 'd') and (len(app.widgets) >= app.startWidgetList):
        app.widgets.pop()



##########################################
# Bake Mode
##########################################

def bakeMode_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_image(0, 0, image=ImageTk.PhotoImage(app.bakeImg), anchor="nw")
    canvas.create_text(app.width / 2, app.margin,
                       text='Press any key or press mouse to back to the mainMode',
                       fill='black', font=("Courier", 14))

def bakeMode_keyPressed(app, event):
    app.mode = 'mainMode'

def bakeMode_mousePressed(app, event):
    app.mode = 'mainMode'

##########################################
# Main App
##########################################

def getRandomColor():
    colors = ['orange', 'maroon', 'salmon']
    return random.choice(colors)

class Widget:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class button(Widget):
    def __init__(self, x, y, color, text, width, height):
        super().__init__(x, y, color)
        self.text = text
        self.height= height
        self.width=width
    def redraw(self, app, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height,
                                fill=self.color, width=0)
        canvas.create_text(self.x + 0.5 * self.width, self.y + 0.5 * self.height,
                           text = f'{self.text}', anchor="center")
    def findCorners(self): # return all four corners to check if there's any corner exceeds border
        return(self.x, self.y, self.x + self.width, self.y + self.height)

class radioButton(Widget):
    def __init__(self, x, y, color, text):
        super().__init__(x, y, color)
        self.text = text
    def redraw(self, app, canvas):
        canvas.create_oval(self.x, self.y, self.x + app.radioSize, self.y + app.radioSize,
                         outline=self.color, width = 2) # outline
        canvas.create_oval(self.x + 1/3 * app.radioSize, self.y + 1/3 * app.radioSize,
                           self.x + 2/3 * app.radioSize, self.y + 2/3 * app.radioSize,
                           fill = self.color, width=0) # inside circle
        canvas.create_text(self.x + 1/2 * app.radioSize + app.padding, self.y + 1/2 * app.radioSize,
                           text=f'{self.text}', anchor="w")
    def findCorners(self):  # return all four corners to check if there's any corner exceeds border
        return (self.x, self.y, self.x + self.width, self.y + self.height)

class checkBox(Widget):
    def __init__(self, x, y, color, text):
        super().__init__(x, y, color)
        self.text = text
    def redraw(self, app, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + app.checkBoxSize, self.y + app.checkBoxSize,
                                outline=self.color, width=2)
        canvas.create_text(self.x + app.padding, self.y + 1/2 * app.radioSize,
                           text=f'{self.text}', anchor="w")

class textInput(Widget):
    def __init__(self, x, y, color, text,width,height):
        super().__init__(x, y, color)
        self.text = text
        self.width = width
        self.height = height
    def redraw(self, app, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height,
                                outline="grey", width=1)
        canvas.create_text(self.x + app.margin, self.y + (0.5) * self.height,
                           text=f'{self.text}', anchor="w", fill = "grey")

class slider(Widget):
    def __init__(self, x, y, color, width):
        super().__init__(x, y, color)
        self.width = width
    def redraw(self, app, canvas):
        canvas.create_line(self.x , self.y, self.x + self.width * 1/3 , self.y,
                           width=2, fill='grey')
        canvas.create_line(self.x + self.width * 1/3, self.y, self.x + self.width, self.y,
                           width=2, fill='orange')
        canvas.create_oval(self.x + self.width * 1/3 - (0.5) * app.radioSize, self.y - (0.5) * app.radioSize, \
                           self.x + self.width * 1/3 + (0.5) * app.radioSize, self.y + (0.5) * app.radioSize,
                           fill='orange', width=0)  # outline

class textbox(Widget):
    def __init__(self, x, y, color,width,lineHeight):
        super().__init__(x, y, color)
        self.width = width
        self.text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s."
        self.lineHeight = lineHeight
    def redraw(self, app, canvas):
        lines = int(len(self.text) // self.width) + 1
        for i in range(lines):
            currText = self.text[i * self.width:(i+1) * self.width]
            canvas.create_text(self.x , self.y + i * self.lineHeight,
                               text=f'{currText}', anchor="w", fill="grey")

class image(Widget):
    def __init__(self, x, y, color, width):
        super().__init__(x, y, color)
        self.width = width
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.decoImg), anchor="nw")

class icon(Widget):
    def __init__(self, x, y, color, width):
        super().__init__(x, y, color)
        self.width = 10
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.icon), anchor="nw")

def chooseRandomWidget(app, event):
    x = event.x
    y = event.y
    color = "orange"
    text = "text"
    widgetsList = [button, radioButton, checkBox, textInput, slider, textbox, image]
    #               x                               x           x       x
    newWidget = random.choice(widgetsList)
    if checkWithinBoundary(app,event):
        if newWidget == slider:
            return newWidget(x, y, color, 200)
        if newWidget == textbox:
            return newWidget(x, y, text, 40, 16)
        if newWidget == textInput:
            return newWidget(x, y, color, text, 200,30)
        if newWidget == button:
            return newWidget(x, y, color, text, 200, 30)
        if newWidget == image:
            return newWidget(x, y, color, 300)
    return newWidget(x, y, color, text)

def checkWithinBoundary(app,event):
    return True # check if all the boundaries are within the drawing area

def appStarted(app):
    app.mode = 'IntroMode'
    app.margin = 10
    app.height = 600
    app.width = 1000
    app.padding = 20
    app.cellwidth = 10
    app.cellheight= 10
    app.rows = 60
    app.cols = 100
    app.section = int(app.height/3)
    app.mockUp = app.scaleImage(app.loadImage("mockUp.png"), 2/3)
    app.colorWheel = app.scaleImage(app.loadImage("colorWheel.png"), 1/3)
    app.colorPicker = app.scaleImage(app.loadImage("colorPicker.png"), 1/10)
    app.decoImg = app.scaleImage(app.loadImage("decoImg.jpg"), 1 / 2)
    app.icon = app.scaleImage(app.loadImage("icon2.png"), 1 / 10)
    app.bakeImg = app.scaleImage(app.loadImage("bakeUI.jpg"), 1)
    app.radioSize = 10
    app.checkBoxSize = 10
    app.startWidgetList = 15 # prevent pop the wrong widget
    app.widgets = [
        button(30, 50, "orange", "Button1",100,30),
        button(140, 50, "grey", "Button2",100,30),
        radioButton(30, 100, "orange", "Banana"),
        radioButton(30, 120, "orange", "Apple"),
        checkBox(120, 100, "orange", "I accept"),
        checkBox(120, 120, "orange", "I prefer not to say"),
        textInput(30, 150, "orange", "enter your text here",200,30),
        slider(30, 200, "orange",200),
        textbox(30, 230, "black", 40, 16),
        image(180, 230, "black", 200)
    ]  # this is for all the widgets
    app.widgets.append(button(890, 560, "orange", "Bake UI",100,30))
    app.widgets.append(button(500, 560, "darkgrey", "< last",100,30))
    app.widgets.append(button(600, 560, "grey", "> next",100,30))
    app.widgets.append(icon(40, 340, "black", 20))

def drawInstructions(app,canvas):
    canvas.create_text(app.width / 2, app.margin,
                       text='Use existing widgets to design your own UI, d for delete item and p for restart',
                       fill='black', font =("Courier", 14))
    canvas.create_text(100, 22,
                       text='Widgets Library',
                       fill='black', font =("Courier", 12), anchor = "nw")
    canvas.create_text(600, 22,
                       text='Your UI canvas',
                       fill='black', font =("Courier", 12), anchor = "nw")
    canvas.create_rectangle(10, 380, 320, 400, fill = "orange", width = 0)
    # canvas.create_rectangle(10, 40, 320, 560, outline='black')
    canvas.create_text(20, 380,
                       text='Color Palette for picking colors',
                       fill='black', font=("Courier", 12), anchor="nw")

def drawGrid(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = None, outline = "white")

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    x0 = col * app.cellwidth
    x1 = (col+1) * app.cellwidth
    y0 = row * app.cellheight
    y1 = (row+1) * app.cellheight
    return (x0, y0, x1, y1)

def drawWidgetsBox(app, canvas):
    canvas.create_rectangle(10, 20, 320,40, fill = "orange", width = 0)
    canvas.create_rectangle(10, 40, 320, 560, outline='black')

def drawUIBox(app, canvas):
    canvas.create_rectangle(330, 40, 990, 560, outline = 'black')
    canvas.create_rectangle(330, 20, 990, 40, fill='orange', width = 0)



# first scene for instructions(also can not exist)

runApp(width=1000, height=600)
