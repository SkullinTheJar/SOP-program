import arcade
import random
import csv
import math
import time
import os

# Definerer højden og bredden af vinduet
width = 900
height = 600

# Funktion til hentning af data om solpletter
def GetData():
    dataFilePath = os.path.dirname(__file__) # Henter programmets mappes sti
    dataFile = open(dataFilePath + '/' + 'SunSpotNumbers.csv')
    fileReader = csv.reader(dataFile)
    dataList = list(fileReader)
    return dataList

# Klasse til at lave cirkler
class Circles():
    def __init__(self, x, y, radius, color):
        self.xCoord = x
        self.yCoord = y
        self.radius = radius
        self.color = color

    def DrawCircle(self):
        arcade.draw_circle_filled(self.xCoord, self.yCoord, self.radius, self.color)

# Klasse til at lave rektangler med en kant rundt om
class Button():
    def __init__(self, xLeft, xRight, yTop, yBottom, color):
        self.xLeft = xLeft
        self.xRight = xRight
        self.yTop = yTop
        self.yBottom = yBottom
        self.color = color
        self.edgeColor = arcade.color.GRAY
    
    def DrawButton(self):
        arcade.draw_lrtb_rectangle_filled(self.xLeft, self.xRight, self.yTop, self.yBottom, self.color)
        arcade.draw_lrtb_rectangle_outline(self.xLeft, self.xRight, self.yTop, self.yBottom, self.edgeColor, 2)

# Main-klassen
class Simulator(arcade.Window):
    # Opretter lister for dataene og objekterne, samt variabler der bruges senere 
    def __init__(self, width, height, title):
        super().__init__(width, height, title) # Kalder superklassen init-metode
        self.dataList = GetData()
        self.sunspotList = []
        self.buttonList = [
            Button(630, 720, 330, 290, arcade.color.GREEN),
            Button(760, 850, 330, 290, arcade.color.RED),
            Button(630, 690, 200, 160, arcade.color.DARK_GRAY),
            Button(720, 780, 200, 160, arcade.color.DARK_GRAY),
            Button(810, 870, 200, 160, arcade.color.DARK_GRAY)
            ]
        self.sun = Circles(width/3, height/2, 250, arcade.color.YELLOW)
        self.sunspotNumber = 0
        self.currentYear = 1749
        self.currentMonth = 1
        self.timer = 0
        self.spotsPerTime = 0
        self.spotsThisMonth = 0
        self.pause = True
        self.pace = 0.2

    def update(self, delta_time):
        if self.pause: # Hvis pause=True opdateres programmet ikke
            pass
        else:
            if self.timer >= 15: # Opdater måneden og clear alle solpletter
                self.currentMonth += 1
                self.sunspotList.clear()
                self.sunspotNumber = 0
                self.timer = 0
            if self.currentMonth >= 13: # Opdater året
                self.currentYear += 1
                self.currentMonth = 1
            if self.currentYear >= 2015: # Genstart hvis året er for stort  
                self.timer = 0
                self.currentMonth = 1
                self.currentYear = 1749
            # spotsThisMonth = månedens antal af solpletter rundet op
            self.spotsThisMonth = math.ceil(float(self.dataList[self.currentMonth + 12*(self.currentYear - 1749)][2]))
            # Beregn antallet af solpletter der skal tegnes pr. timer-værdi
            if self.spotsThisMonth >= 15:
                self.spotsPerTime = int(self.spotsThisMonth / 15)
            else:
                if self.timer == 15/3:
                    self.spotsPerTime = math.ceil(self.spotsThisMonth / 2)
                if self.timer == 15/3*2:
                    self.spotsPerTime = int(self.spotsThisMonth / 2)
            # Indsætter solpletter pr. timer-værdi med tilfældige coordinater i listen
            for x in range(0, self.spotsPerTime):
                x = random.randint(150, 450)
                y = random.randint(150, 450)
                radius = random.randint(4, 6)
                sunspot = Circles(x, y, radius, arcade.color.DARK_BROWN)
                self.sunspotList.append(sunspot)
                self.sunspotNumber += 1
            # Opdaterer timer, nulstiller solplet-listen, og venter lidt
            self.timer += 1
            self.spotsPerTime = 0
            time.sleep(self.pace)

    def on_draw(self): # Tegner objekter og tekst på skærmen
        arcade.start_render()
        arcade.draw_lrtb_rectangle_filled(width/3*2, width, height, 0, arcade.color.LIGHT_GRAY)
        self.sun.DrawCircle()
        for z in self.sunspotList:
            z.DrawCircle()
        for z in self.buttonList:
            z.DrawButton()
        arcade.draw_text('Year: ' + str(self.currentYear), width/10*7, height/100*90, arcade.color.BLACK, 20)
        arcade.draw_text('Month nr.: ' + str(self.currentMonth), width/10*7, height/100*80, arcade.color.BLACK, 20)
        arcade.draw_text('Sunspot nr.: ' + str(self.sunspotNumber), width/10*7, height/100*70, arcade.color.BLACK, 20)
        arcade.draw_text('START', 650, 300, arcade.color.BLACK, 16)
        arcade.draw_text('PAUSE', 780, 300, arcade.color.BLACK, 16)
        arcade.draw_text('Speed:', 715, 210, arcade.color.BLACK, 20)
        arcade.draw_text('1x', 650, 170, arcade.color.BLACK, 16)
        arcade.draw_text('2x', 740, 170, arcade.color.BLACK, 16)
        arcade.draw_text('3x', 830, 170, arcade.color.BLACK, 16)

    def on_mouse_motion(self, x, y, dx, dy):
        # Finder musens koordinater
        self.mouseX = x
        self.mouseY = y

    def on_mouse_press(self, x, y, button, modifiers): # Tjekker om der klikkes på startknappen
        # Hvis der trykkes START er pause=False
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouseX > 630 and self.mouseX < 720 and self.mouseY > 290 and self.mouseY < 330:
            self.pause = False
            self.buttonList[0].edgeColor = arcade.color.BLACK
            self.buttonList[1].edgeColor = arcade.color.GRAY
        # Hvis der trykkes PAUSE er pause=True
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouseX > 760 and self.mouseX < 850 and self.mouseY > 290 and self.mouseY < 330:
            self.pause = True
            self.buttonList[1].edgeColor = arcade.color.BLACK
            self.buttonList[0].edgeColor = arcade.color.GRAY
        # De næste 3 if-er tjekker om der trykkes på henholdsvis '1x', '2x' eller '3x' knappen
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouseX > 630 and self.mouseX < 690 and self.mouseY > 160 and self.mouseY < 200:
            self.pace = 0.2
            self.buttonList[2].edgeColor = arcade.color.BLACK
            self.buttonList[3].edgeColor = arcade.color.GRAY
            self.buttonList[4].edgeColor = arcade.color.GRAY
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouseX > 720 and self.mouseX < 780 and self.mouseY > 160 and self.mouseY < 200:
            self.pace = 0.1
            self.buttonList[3].edgeColor = arcade.color.BLACK
            self.buttonList[2].edgeColor = arcade.color.GRAY
            self.buttonList[4].edgeColor = arcade.color.GRAY
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouseX > 810 and self.mouseX < 870 and self.mouseY > 160 and self.mouseY < 200:
            self.pace = 0.06
            self.buttonList[4].edgeColor = arcade.color.BLACK
            self.buttonList[2].edgeColor = arcade.color.GRAY
            self.buttonList[3].edgeColor = arcade.color.GRAY

# Opretter vindue og kører det
mitVindue = Simulator(width, height, "Sunspot Simulator")
arcade.run()
