from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import csv
import matplotlib.pyplot as plt
import random 
import tkinter
import cv2
from PIL import Image, ImageTk 
from itertools import count 
import os
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i],fontsize=25,rotation=45)
def main():
    global COUNTER
    web2csv()
    dbConn()
    csv2db()
    removeFILENAME()
    db2chart()
    if (COUNTER!=1):
        clear_label_image()
    make_label()
    COUNTER += 1
def web2csv():
    global FILENAME
    YEAR = str(1950+radiovalue.get())
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://www.statsf1.com/en/default.aspx")
    FILENAME = "f1drivers"+YEAR+".csv"
    try:
        driver.find_element_by_id("ctl00_HL_SeasonH").click()
        driver.find_element_by_link_text(YEAR).click()
        soup = BeautifulSoup(driver.page_source,"lxml")
        table = soup.select_one("#ctl00_CPH_Main_TBL_CHP_P")
        df = pd.read_html(str(table))
        df[0].to_csv(FILENAME)
    except NoSuchElementException:
        print(YEAR)
        print("選取元素不存在")
    driver.quit()

def dbConn():
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    sqlstr = '''DROP TABLE IF EXISTS "f1";'''
    cursor.execute(sqlstr)
    sqlstr = '''
        
        CREATE TABLE IF NOT EXISTS "f1" (
            "id"	INTEGER,
            "name"	TEXT NOT NULL,
            "points"	REAL NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
    '''
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()

def csv2db():
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    with open(FILENAME,"r",encoding="utf-8") as f:
        rows = csv.reader(f)
        count=0
        for row in rows:
            if (count<2):count+=1;
            else:
                name = row[2]
                points = row[-1]
                sqlstr = '''INSERT INTO f1("name","points")
                VALUES ("{}","{}")'''.format(name,points)
                cursor.execute(sqlstr)
    conn.commit()
    conn.close()

def db2chart():
    labels = []
    sizes = []
    colors = []
    total = 0 
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    sqlstr = '''SELECT * FROM "f1" '''
    cursor.execute(sqlstr)
    for item in cursor.fetchall():
        total += int(item[2])
        if item[2] != 0:
            labels.append(item[1])
            sizes.append(item[2])
    for i in range(len(labels)):
        r = lambda: random.randint(0,255)
        colors.append("#{0:02x}{1:02x}{2:02x}".format(r(),r(),r()))
    plt.figure(figsize=(25,12))
    plt.subplot(1,2,1)
    plt.title("Points per Driver",fontsize=30,pad=32)
    xticks = range(1,len(labels)+1)
    addlabels(labels,sizes)
    plt.xticks(rotation=45,fontsize=17)
    plt.yticks(rotation=90,fontsize=16)
    plt.bar(labels,sizes,color="blue",width=0.6)
    
    removeInd = []
    for i in range(len(sizes)):
        if ((sizes[i]/total)<0.01):
            removeInd.append(i)
    for i in range(len(removeInd)):
        x = labels.pop(removeInd[0])
        y = sizes.pop(removeInd[0])
    plt.subplot(1,2,2)
    plt.pie(sizes,labels=labels,colors=colors,autopct="%.1f%%",wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},textprops={'fontsize': 18})
    plt.axis("equal")
    plt.title("Points 2 Percentages",fontsize=30,pad=32)
    plt.savefig("chart.png")
    plt.close()
def make_label():
    global window
    global lab2
    width = 625
    height = 300
    image = cv2.imread('chart.png')
    img = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imwrite('chart.png', img)
    phimage = tkinter.PhotoImage(file="chart.png")
    lab2 = tkinter.Label(window, image=phimage)
    lab2.phimage = phimage
    lab2.grid(row=0,rowspan=row+2,column=6)
def clear_label_image():
    global lab2
    lab2.config(image="")
def exit():
    global window
    removeChartDB()
    window.destroy()
def removeFILENAME():
    global FILENAME
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
    else:
        print("CSV file does not exist")
def removeChartDB():
    global DBNAME
    if os.path.exists(DBNAME):
        os.remove(DBNAME)
    else:
        print("DB file does not exist")
    if os.path.exists("chart.png"):
        os.remove("chart.png")
    else:
        print("chart.png does not exist")
FILENAME=""
DBNAME = "f1db.db"
window = tkinter.Tk()
window.title("Get F1 Statistics")
window.geometry("1253x600")
img = Image.open("images/btnback.png")
img2 = ImageTk.PhotoImage(img)
background_image = tkinter.PhotoImage()
lab5 = tkinter.Label(window, image = img2)
lab5.place(x = 0, y = 0)
bg = tkinter.PhotoImage(file = "images/show.gif")

radiovalue = tkinter.IntVar()
class ImageLabel(tkinter.Label): 
    """a label that displays images, and plays them if they are gifs""" 
    def load(self, im): 
     if isinstance(im, str): 
      im = Image.open(im) 
     self.loc = 0 
     self.frames = [] 

     try: 
      for i in count(1): 
       self.frames.append(ImageTk.PhotoImage(im.copy())) 
       im.seek(i) 
     except EOFError: 
      pass 

     try: 
      self.delay = im.info['duration'] 
     except: 
      self.delay = 300 

     if len(self.frames) == 1: 
      self.config(image=self.frames[0]) 
     else: 
      self.next_frame() 

    def unload(self): 
     self.config(image=None) 
     self.frames = None 

    def next_frame(self): 
     if self.frames: 
      self.loc += 1 
      self.loc %= len(self.frames) 
      self.config(image=self.frames[self.loc]) 
      self.after(self.delay, self.next_frame) 
COUNTER = 1 # 紀錄Search次數
label4 = ImageLabel(window)
label4.place(x = 627, y = 0)
label4.load('images/show.gif')

lbl = ImageLabel(window) 
lbl.grid(row=0,column=0,columnspan=5)
lbl.load('images/f1.gif') 

yearlist = [i for i in range(1950,2022)]
radiovalue.set(0)
row=1
column=0
for i in range(len(yearlist)):
    if i % 5==0:row+=1
    tkinter.Radiobutton(window,text=yearlist[i],variable=radiovalue,value=i).grid(row=row,column=column)
    column += 1
    if column>=5:
        column=0   
btn1 = tkinter.Button(window,text="Search",command=main).grid(row=row+1,column=2)
btn2 = tkinter.Button(window,text="Delete",command=clear_label_image).grid(row=row+1,column=3)
btn3 = tkinter.Button(window,text="Close",command=exit).grid(row=row+1,column=4)

window.mainloop()
