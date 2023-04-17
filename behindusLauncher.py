print('Loading!')

from PIL import ImageTk, Image
import PIL.Image
from tkinter import *
import tkinter as tk
import tkinter as ttk
import os
import urllib.request
import requests
from ctypes import windll
from tkinter import messagebox
import sys
import zipfile
import subprocess
import configparser
import threading
import shutil


canPlay = False
IsInstall = False
caseInt = 0

#https://phyoxent.com/behainus/

online_version = "https://phyoxent.com/behainus/version.txt"
version_path = "./version.txt"



def checkVer():
    global start_game_button
    global canPlay
    global caseInt
    print('Checking For Version...')
    print("Local Version:")
    with open("version.txt", "r") as file:
        localver = file.read()
        print(localver)
    response = requests.get(online_version)
    onlinever = response.text
    print("Server Version:")
    print(onlinever)
    if localver == onlinever:
        canPlay = True
    else:
        print('Game need to update')
        start_game_button.config(text="Update")
        canPlay = False
        caseInt = 1

 # adata = file.read()



def cleanInstall():
    global start_game_button
    global IsInstall
    global canPlay
    config = configparser.ConfigParser()

   # set the configuration values

    current_directory1 = os.getcwd()
    inis1 = '\config\config.ini'
    configsetting = current_directory1 + inis1


    config['installing'] = {'IsInstall': 'True'}
    with open(configsetting, 'w') as configfile:
        config.write(configfile)
    canPlay = True
    IsInstall = True
    start_game_button.config(state='normal')
    start_game_button.config(text="Play")




def unzipgame():
    with zipfile.ZipFile('Game.zip', 'r') as zip_ref:
        print("Extrating ZipFile")
        zip_ref.extractall('GameData')
    if os.path.exists("./Game.zip"):
        print("Removing ZipFile")
        os.remove("./Game.zip")
        cleanInstall()
    else:
        print("Cannot Find Zip File")

def launchGame():
    config1 = configparser.ConfigParser()
    config1.read('./config/defualt.ini')
    exeurl_section = config1['gameurl']
    exeurl = exeurl_section['name']
    subprocess.call(["./Launcher.exe", "--gamepath", exeurl])
    sys.exit()
    

def download_game_progress(count, block_size, total_size):
     global start_game_button
     #{count*block_size} bytes
     percent = int(count * block_size * 100 / total_size)
     print(f'Downloaded ({percent}%)', end='\r')
     start_game_button.config(text="Installing... %i" % percent)
          
        

def installGame():
    print('Installing...')
    global start_game_button
    start_game_button.config(text="Installing... Wait")
    print('Downloading Game ')
    try:

      download_game = 'https://phyoxent.com/behainus/Game.zip'    #Change for diferent game
      urllib.request.urlretrieve(download_game, 'Game.zip', download_game_progress)

      print('Downloading Version Text')
      download_vers = 'https://phyoxent.com/behainus/version.txt'    #Change for diferent game
      urllib.request.urlretrieve(download_vers, 'version.txt')  
      start_game_button.config(text="Cleaning install...")
      unzipgame()
    except:
        print("Error at instalation")

def download_game_progress1(count, block_size, total_size):
     global start_game_button
     #{count*block_size} bytes
     percent = int(count * block_size * 100 / total_size)
     print(f'Downloaded ({percent}%)', end='\r')
     start_game_button.config(text="Updating... %i" % percent)

def update():
    global start_game_button
    print("Updating...")
    download_game = 'https://phyoxent.com/behainus/Game.zip'
    urllib.request.urlretrieve(download_game, 'Game.zip', download_game_progress1)
    start_game_button.config(text="Cleaning update...")
    os.remove("./version.txt")
    download_vers = 'https://phyoxent.com/behainus/version.txt'    #Change for diferent game
    urllib.request.urlretrieve(download_vers, 'version.txt')  
    unzipgame()

def unistall():
    print("Unistalling")
    os.remove("./version.txt")
    shutil.rmtree("./GameData")
    config1 = configparser.ConfigParser()
    current_directory2 = os.getcwd()
    inis2 = '\config\config.ini'
    configsetting1 = current_directory2 + inis2
    config1['installing'] = {'IsInstall': 'False'}
    with open(configsetting1, 'w') as configfile:
        config1.write(configfile)

    

def btnInstall():
    global canPlay
    global IsInstall
    global caseInt
    global start_game_button
    print("Cheking data")
    if canPlay & IsInstall == True:
        launchGame()
    else:
        if caseInt == 0:
            start_game_button.config(state='disabled')
            download_thread = threading.Thread(target=installGame)
            download_thread.start()
        elif caseInt == 1:
            start_game_button.config(state='disabled')
            update_thread = threading.Thread(target=update)
            update_thread.start()
           

        
    
tk_title = "Phyox LABS Launcher - Behind Us" 

root=Tk()
root.title(tk_title) 
root.overrideredirect(True)
root.geometry('1020x600') 

root.minimized = False
root.maximized = False

# VARIABLES DE COLOR
WHITE = "#FFFFFF"
LGRAY = '#292D32'
DGRAY = '#25292e'
RGRAY = '#1B1D1F'

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)


def set_appwindow(mainWindow): 
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080

    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    

def minimize_me():
    root.attributes("-alpha",0) 
    root.minimized = True       


def deminimize(event):

    root.focus() 
    root.attributes("-alpha",1) 
    if root.minimized == True:
        root.minimized = False                              
        


close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)


window = Frame(root, bg=DGRAY,highlightthickness=0)


title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH)


def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'
    
    
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=RGRAY


def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=LGRAY
    
    
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=RGRAY
    

def get_pos(event): 
    if root.maximized == False:
 
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        
        def move_window(event): 
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


        def release_window(event): 
            root.config(cursor="arrow")
            
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        root.maximized = not root.maximized

title_bar.bind('<Button-1>', get_pos)
title_bar_title.bind('<Button-1>', get_pos) 


close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)


root.bind("<FocusIn>",deminimize)
root.after(10, lambda: set_appwindow(root))




# CODIGO DEL GUI   

config_frame = tk.Frame(root)
config_frame.config(width=70, height=600, bg=LGRAY)
config_frame.pack(side=tk.LEFT)

home = Button(config_frame, text="🏠", height=3, width=6, bd=0, bg=DGRAY, fg =WHITE)
home.place(x=10, y=190)

label = Button(config_frame, text="⚙️", height=3, width=6, bd=0, bg=DGRAY, fg=WHITE)
label.place(x=10, y=490)


start_frame = tk.Frame(root)
start_frame.config(width=950, height=600, bg=DGRAY)
start_frame.pack(side=tk.LEFT)

'''# IMAGEN DEL LOGOTIPO
game_logo_environment = Canvas(start_frame, width= 180, height= 120, bg=DGRAY, highlightthickness=0)
game_logo_environment.config(bd=0)
game_logo_environment.place(x=370, y=20)

img= (PIL.Image.open("behind-us-logo.png"))

resized_image= img.resize((160,100))
new_image= ImageTk.PhotoImage(resized_image)

game_logo_environment.create_image(10,10, anchor=NW, image=new_image)

# LOGOTIPO PHYOX
corp_logo_environment = Canvas(root, width= 100, height= 50, bg=DGRAY, highlightthickness=0)
corp_logo_environment.config(bd=0)
corp_logo_environment.place(x=80, y=545)

img= (PIL.Image.open("phyox-logo-3.png"))

resized_image= img.resize((80,30))
new_image_2= ImageTk.PhotoImage(resized_image)

corp_logo_environment.create_image(10,10, anchor=NW, image=new_image_2)'''

'''start_game_button = tk.Button(start_frame, text="Unistall", height=3, width=18, command=unistall)
start_game_button.place(x=550, y=470)
'''
start_game_button = ttk.Button(text="Wait...", width=18, height=3, bd=0, bg=LGRAY, fg =WHITE, font=("Arial 10 bold"), command=btnInstall)
start_game_button.place(x=830, y=525)

error_arg = None

for arg in sys.argv:
    if arg.startswith('--error='):
        error_arg = arg.split('=')[1]

print('Error value:', error_arg)

if error_arg == None:
    pass
else:
    messagebox.showinfo("Error at staring game", error_arg)
    
def init():
    global IsInstall

   
    current_directory = os.getcwd()
    print(current_directory)
    inis = '\config\config.ini'
    configsetting = current_directory + inis
    print(configsetting)

    config = configparser.ConfigParser()
    config.read(configsetting)
    install_section = config['installing']
        
    isInstallCF = install_section['isinstall']

    if isInstallCF == 'True':
            IsInstall = True
            global start_game_button
            start_game_button.config(text="Play")
    else:
            IsInstall = False
    



    if IsInstall == True:
        checkVer()
    # if os.path.exists(version_path):
    #    checkVer()
    #   start_game_button.config(text="Play")###
    else:
        try:
            start_game_button.config(text="Install")
          
        except:
            print('Cannot Get Version Text')
            
        

init()

root.mainloop()
print('The program closed correctly!')