print('LOADING THE PROGRAM')
print('-' * 50)

# LIBRERYS
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

# INSTALATION CONFIG
canPlay = False
IsInstall = False
caseInt = 0

#https://phyoxent.com/behainus/

online_version = "https://phyoxent.com/behainus/version.txt"
version_path = "./version.txt"


# CHECKING VERSION FUNCTION
def checkVer():
    global onlinever
    global localver
    global start_game_button
    global canPlay
    global caseInt
    print("CHECKING VERSION'S...")
    print("LOCAL VERSION")
    with open("version.txt", "r") as file:
        localver = file.read()
        print(localver)
    response = requests.get(online_version)
    onlinever = response.text
    print("SERVER VERSION")
    print(onlinever)
    if localver == onlinever:
        canPlay = True
    else:
        print('UPDATE REQUIRED')
        start_game_button.config(text="Update")
        canPlay = False
        caseInt = 1

 # adata = file.read()


# UNINSTALL GAME

def cleanInstall():
    global start_game_button
    global IsInstall
    global canPlay
    config = configparser.ConfigParser()

   # SETTING CONFIGURATION VALUES

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



# UNZIP GAME FUNCTION

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

# LAUNCH GAME FUNCTION

def launchGame():
    config1 = configparser.ConfigParser()
    config1.read('./config/defualt.ini')
    exeurl_section = config1['gameurl']
    exeurl = exeurl_section['name']
    subprocess.call(["./Launcher.exe", "--gamepath", exeurl])
    sys.exit()
    
# UPDATING THE GAME FUNCTION

def download_game_progress(count, block_size, total_size):
     global start_game_button
     #{count*block_size} bytes
     percent = int(count * block_size * 100 / total_size)
     print(f'Downloaded ({percent}%)', end='\r')
     start_game_button.config(text="Installing... %i" % percent)
          
        
# INSTALLING GAME FUNCTION

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

# DOWNLOADING GAME PROCESS

def download_game_progress1(count, block_size, total_size):
     global start_game_button
     #{count*block_size} bytes
     percent = int(count * block_size * 100 / total_size)
     print(f'Downloaded ({percent}%)', end='\r')
     start_game_button.config(text="Updating... %i" % percent)

# UPDATING GAME

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

# UNINSTALL GAME

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


# UNINSTALL GAME BUTTON FUNCTION    

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
           


# TITLE FOR THE MIX NAV        

tk_title = "Phyox LABS Launcher - Behind Us" 

# ROOT CONFIG

root=Tk()
root.title(tk_title) 
root.overrideredirect(True)
root.geometry('1020x600') 

# ROOT MINIMIZED/MAXIMIZED AS FALSE

root.minimized = False
root.maximized = False

# COLOR VARIABLE
WHITE = '#FFFFFF'
CGRAY = '#3F444A'
LGRAY = '#292D32'
DGRAY = '#25292e'
RGRAY = '#1B1D1F'

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)

# SETTING THE APP AS CONTAINER

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




# MINIMIZE THE APP

def minimize_me():
    root.attributes("-alpha",0) 
    root.minimized = True       

# DEMINIZE THE APP

def deminimize(event):

    root.focus() 
    root.attributes("-alpha",1) 
    if root.minimized == True:
        root.minimized = False                              
        

# BUTTONS FOR THE MIX NAV
close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

# SETTING THE WINDOW
window = Frame(root, bg=DGRAY,highlightthickness=0)



# MIX NAV CONFIG2
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
    
# FUNCTION FOR MOVE THE APP

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


# GETTING THE EVENTS

title_bar.bind('<Button-1>', get_pos)
title_bar_title.bind('<Button-1>', get_pos) 


close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)


root.bind("<FocusIn>",deminimize)
root.after(10, lambda: set_appwindow(root))




# CODIGO DEL GUI

# HOME CONFIG FOR HOVER
def config_open(e):
    pass

def button_hover(e):
    status_home["bg"] = LGRAY
    status_home["fg"] = WHITE
    status_home["font"] = "Arial 10 bold"
    status_home.config(text="IN DEVING...")

def button_hover_leave(e):
    status_home["bg"] = DGRAY
    status_home.config(text="")

# NEWS CONFIG FOR HOVER

def button_hover2(e):
    status_news["bg"] = LGRAY
    status_news["fg"] = WHITE
    status_news["font"] = "Arial 10 bold"
    status_news.config(text="IN DEVING...")

def button_hover_leave2(e):
    status_news["bg"] = DGRAY
    status_news.config(text="")

# OPTIONS CODING
# MAKING CONFIGURATION WINDOWS
# -
# -
# -
# --
def options_window():
    tk_title2 = "Phyox LABS Launcher - Configuration" 

    # ROOT CONFIG

    root2 =Tk()
    root2.title(tk_title2) 
    root2.overrideredirect(True)
    root2.geometry('400x300') 

    # ROOT MINIMIZED/MAXIMIZED AS FALSE

    root2.minimized = False
    root2.maximized = False

    root2.config(bg=LGRAY)
    title_bar = Frame(root2, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)

    # SETTING THE APP AS CONTAINER

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




    # MINIMIZE THE APP

    def minimize_me():
        root2.attributes("-alpha",0) 
        root2.minimized = True       

    # DEMINIZE THE APP

    def deminimize(event):

        root2.focus() 
        root2.attributes("-alpha",1) 
        if root2.minimized == True:
            root2.minimized = False                              
        

    # BUTTONS FOR THE MIX NAV
    close_button = Button(title_bar, text='  ×  ', command=root2.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
    minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
    title_bar_title = Label(title_bar, text=tk_title2, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

    # SETTING THE WINDOW
    window = Frame(root2, bg=LGRAY,highlightthickness=0)



# MIX NAV CONFIG2
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

    # FUNCTION FOR MOVE THE APP

    def get_pos(event): 
        if root2.maximized == False:
        
            xwin = root2.winfo_x()
            ywin = root2.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx


            def move_window(event): 
                root2.config(cursor="fleur")
                root2.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


            def release_window(event): 
                root2.config(cursor="arrow")


            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            root2.maximized = not root2.maximized


    # GETTING THE EVENTS

    title_bar.bind('<Button-1>', get_pos)
    title_bar_title.bind('<Button-1>', get_pos) 


    close_button.bind('<Enter>',changex_on_hovering)
    close_button.bind('<Leave>',returnx_to_normalstate)
    minimize_button.bind('<Enter>', changem_size_on_hovering)
    minimize_button.bind('<Leave>', returnm_size_on_hovering)


    root2.bind("<FocusIn>",deminimize)
    root2.after(10, lambda: set_appwindow(root))

    textinho = Label(root2, text="IN DEVING...", font="Arial 14 bold", bg=LGRAY, fg=WHITE)
    textinho.place(x=130, y=40)
# ENDING OF THE CONFIGURATION WINDOWS
# -
# -
# -
# --
# FRAME CODING
'''config_frame_open = tk.Frame()
config_frame_open.config(width=100, height=100, bg="black")
config_frame_open.pack()
'''
# CONFIGURATION FRAME (NAV IN THE LEFT)
config_frame = tk.Frame(root)
config_frame.config(width=70, height=600, bg=LGRAY)
config_frame.pack(side=tk.LEFT)


# HOME BUTTON

home = Button(config_frame, text="🏠", height=3, width=6, bd=0, bg=DGRAY, fg =WHITE)
home.place(x=10, y=26)

home.bind("<Enter>", button_hover)
home.bind("<Leave>", button_hover_leave)

# NEWS BUTTON IN THE CONFIGS NAV

news = Button(config_frame, text="📰", height=3, width=6, bd=0, bg=DGRAY, fg =WHITE)
news.place(x=10, y=96)

news.bind("<Enter>", button_hover2)
news.bind("<Leave>", button_hover_leave2)


label = Button(config_frame, text="⚙️", height=3, width=6, bd=0, bg=DGRAY, fg=WHITE, command=options_window)
label.place(x=10, y=490)

label.bind("<Button-1>", config_open)

start_frame = tk.Frame(root)
start_frame.config(width=950, height=600, bg=DGRAY)
start_frame.pack(side=tk.LEFT)

# POPUP MENSAJE HOME

status_home = Label(start_frame, text='', background=DGRAY, bd=10)
status_home.place(x=3, y=33)

# POPUP MENSAJE NEWS

status_news = Label(start_frame, text='', background=DGRAY, bd=10)
status_news.place(x=3, y=102)

# IMAGEN DEL LOGOTIPO
game_logo_environment = Canvas(start_frame, width= 180, height= 120, bg=DGRAY, highlightthickness=0)
game_logo_environment.config(bd=0)
game_logo_environment.place(x=370, y=20)

img= (PIL.Image.open("Media/behind-us-logo.png"))

resized_image= img.resize((160,100))
new_image= ImageTk.PhotoImage(resized_image)

game_logo_environment.create_image(10,10, anchor=NW, image=new_image)

# LOGOTIPO PHYOX
corp_logo_environment = Canvas(start_frame, width= 100, height= 50, bg=DGRAY, highlightthickness=0)
corp_logo_environment.config(bd=0)
corp_logo_environment.place(x=5, y=515)

img= (PIL.Image.open("Media/phyox-logo-3.png"))

resized_image= img.resize((80,30))
new_image_2= ImageTk.PhotoImage(resized_image)

corp_logo_environment.create_image( 10,10, anchor=NW, image=new_image_2)

# ACLARATIVE TEXT
version_text = Label(start_frame, text=f"Launcher version 0.0.3(0.0.0.0)", bg=DGRAY, fg=CGRAY)
version_text.place(x=615, y=510)
version_text = Label(start_frame, text=f"Copyright Phyox LABS™ 2023©", bg=DGRAY, fg=CGRAY)
version_text.place(x=607, y=530)

start_game_button = ttk.Button(start_frame, text="Wait...", width=18, height=3, bd=0, bg=LGRAY, fg =WHITE, font=("Arial 10 bold"), command=btnInstall)
start_game_button.place(x=785, y=493)


# CONFIG FOR THE CONFIGURATION



# CONFIGURACIÓN DE INSTALACIÓN
# ERROR EN INICIACIÓN DE JUEGO
error_arg = None

for arg in sys.argv:
    if arg.startswith('--error='):
        error_arg = arg.split('=')[1]

print('Error value:', error_arg)

if error_arg == None:
    pass
else:
    messagebox.showinfo("Error at staring game", error_arg)
    

# INSTALACIÓN
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
print('-' * 50)
print('THE PROGRAM END CORRECTLY')