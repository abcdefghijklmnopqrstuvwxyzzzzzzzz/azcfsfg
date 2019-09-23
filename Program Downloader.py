#!/usr/bin/env python3

import PySimpleGUI as sg
import os
import sys
import requests
import zipfile
import unrar
import pyunpack
from pyunpack import Archive
import urllib.request
import subprocess
from urllib.request import urlopen
import os, time, ctypes, random, base64, datetime, platform, shutil, subprocess, threading, webbrowser, importlib, traceback
from distutils.dir_util import copy_tree

rtbversion = "1.0"

# Load Config
try:
    import sys
    import json
    with open('config.json', 'r') as handle:
        config = json.load(handle)
        skin = config['skin']
        token_list = config['token_list']
        thread_count = config['thread_count']
        use_proxies = config['use_proxies']
        proxy_type = config['proxy_type']
        proxy_list = config['proxy_list']
        proxy_auth = config['proxy_auth']
        proxy_user = config['proxy_user']
        proxy_pass = config['proxy_pass']
        disable_theme_music = config['disable_theme_music']
        verbose = config['verbose']
        command_line_mode = config['command_line_mode']
        no_tk_mode = config['no_tk_mode']
        disable_cloudflare_check = config['disable_cloudflare_check']
        disable_update_check = config['disable_update_check']
        combine_uverified_and_verified = config['combine_uverified_and_verified']
        server_smasher_in_main_window = config['server_smasher_in_main_window']
        ignore_ffmpeg_missing = config['ignore_ffmpeg_missing']
        show_licence = config['show_licence']

except Exception:
    # TRY to fix itself
    print("Unable to read config file.\nImporting necessary modules and checking installation...")
    import os
    import sys
    import urllib.request
    import subprocess
    if not os.path.exists("themes/"):
        print("themes Directory not found.")
    print("Downloading config.json...")
    response = urllib.request.urlopen('https://gist.githubusercontent.com/abcdefghijklmnopqrstuvwxyzzzzzzzz/fae2f52ef0c5d5dacc8722f1323d5ea0/raw/1ade0f42167bc764d3134a0631be8a2e7b990f84/config.json')
    data = response.read()
    data = data.decode('utf-8')
    with open("config.json","w+") as handle:
        handle.write(data)
    print("Downloading requirements.txt...")
    response = urllib.request.urlopen('https://gist.githubusercontent.com/abcdefghijklmnopqrstuvwxyzzzzzzzz/65f31be1a2c98ef51c82e1341340cf1c/raw/2d236f8bc3b2b09dcb7077a110075d5b26bd330f/requirements.txt')
    data = response.read()
    data = data.decode('utf-8')
    with open("requirements.txt","w+") as handle:
        handle.write(data)
    print("Downloading Toolbox.py...")
    response = urllib.request.urlopen('https://gist.githubusercontent.com/abcdefghijklmnopqrstuvwxyzzzzzzzz/b32fcc81dc9c0d60826faa176189d6ca/raw/d107e6e8c7642cad61a8efaac2e5793066a3252c/Toolbox.py')
    data = response.read()
    data = data.decode('utf-8')
    try:
        os.mkdir("themes")
    except Exception:
        pass
    with open("themes/Toolbox.py","w+") as handle:
        handle.write(data)
		
"""import pip
requirements = open("requirements.txt").read().splitlines()
log = open("install.log", "w")
for package in requirements:
		print("Attempting to install {}".format(package))
		p = subprocess.call([sys.executable, "-m", "pip", "install", package, "--user", "--upgrade"],stdout=log, stderr=subprocess.STDOUT)
"""
# Load Skin
if not skin == "Toolbox":
    # Import Default Incase loaded skin has Missing Features/ Compatibility for older skins.
    mdl = importlib.import_module("themes.Toolbox")
    if "__all__" in mdl.__dict__:
        names = mdl.__dict__["__all__"]
    else:
        names = [x for x in mdl.__dict__ if not x.startswith("_")]
    globals().update({k: getattr(mdl, k) for k in names})

# Import New Skin
try:
    mdl = importlib.import_module("themes.{}".format(skin))
    if "__all__" in mdl.__dict__:
        names = mdl.__dict__["__all__"]
    else:
        names = [x for x in mdl.__dict__ if not x.startswith("_")]
    globals().update({k: getattr(mdl, k) for k in names})
except Exception as e:
    print("LAST USED THEME MISSING: {}".format(e))
    with open('config.json', 'r+') as handle:
        edit = json.load(handle)
        edit['skin'] = "Toolbox"
        handle.seek(0)
        json.dump(edit, handle, indent=4)
        handle.truncate()

colours = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
if menu1.lower() == 'random':
    menu1 = random.choice(colours)
if menu2.lower() == 'random':
    menu2 = random.choice(colours)
if not command_line_mode == 1:
    if use_preset_theme:
        sg.ChangeLookAndFeel(preset_window_theme)
    elif use_preset_theme is False:
        sg.SetOptions(background_color=background_color,
                     text_element_background_color=text_element_background_color,
                     element_background_color=element_background_color,
                     scrollbar_color=scrollbar_color,
                     input_elements_background_color=input_elements_background_color,
                     input_text_color=input_text_color,
                     button_color=button_color,
                     text_color=text_color)

# Clear() Function setting
if sys.platform.startswith('win32'):
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')
					 
# File Downloader (Updates, Etc.)
def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename
	
"""# Update
def run_update():
    if sys.platform.startswith('win32'):
        ctypes.windll.kernel32.SetConsoleTitleW("Program Downloader | Updating...")
    else:
        sys.stdout.write("\x1b]2;Program Downloader | Updating...\x07")
    update = requests.get('https://github.com/abcdefghijklmnopqrstuvwxyzzzzzzzz/azcfsfg/archive/master.zip')
    clear()
    print(colored("Update has been downloaded, Installing...",menu1))
    with open("update.zip", "wb") as handle:
        handle.write(update.content)
    try:
        shutil.copy("themes/Toolbox2.py", "Toolbox2_old.py")
    except Exception:
        pass
    try:
        shutil.unpack_archive("update.zip")
        copy_tree("azcfsfg-master/", ".")
        os.remove("update.zip")
        shutil.rmtree("azcfsfg-master/")
        with open('config.json', 'r+') as handle:
            edit = json.load(handle)
            edit['skin'] = skin
            edit['thread_count'] = thread_count
            edit['verbose'] = verbose
            edit['disable_theme_music'] = disable_theme_music
            edit['command_line_mode'] = command_line_mode
            edit['no_tk_mode'] = no_tk_mode
            edit['disable_cloudflare_check'] = disable_cloudflare_check
            edit['disable_update_check'] = disable_update_check
            edit['server_smasher_in_main_window'] = server_smasher_in_main_window
            edit['ignore_ffmpeg_missing'] = ignore_ffmpeg_missing
            edit['combine_uverified_and_verified'] = combine_uverified_and_verified
            edit['show_licence'] = show_licence
            handle.seek(0)
            json.dump(edit, handle, indent=4)
            handle.truncate()
    except Exception as e:
        print("Error Updating, {}".format(e))"""
		
if sys.platform.startswith('win32'):
    ctypes.windll.kernel32.SetConsoleTitleW("Mist's Program Downloader | Status: [Online]")
else:
    sys.stdout.write("\x1b]2;Mist's Program Downloader | Status: [Online]\x07")

# Layout

def main():
    global currentattacks
    global skin
    global token_list
    global thread_count
    global use_proxies
    global proxy_type
    global proxy_list
    global proxy_auth
    global proxy_user
    global proxy_pass
    global verbose
    global disable_theme_music
    global command_line_mode
    global no_tk_mode
    global disable_cloudflare_check
    global disable_update_check
    global server_smasher_in_main_window
    global ignore_ffmpeg_missing
    global show_licence
    clear()

    frame = [[sg.Text("- Guild Duplicator\n- Nickname Changer\n- Token Terminator\n- Hypesquad Changer\n- Token Checker")]]

    links_frame = [[sg.Button("Website", tooltip="My website.", size=(27,1))],
                                   [sg.Button("Duplicator", tooltip="Duplicates a server.", size=(27,1))],
                                   [sg.Button("Nickname Changer", tooltip="Cycles a nickname on a server.", size=(27,1))],
                                   [sg.Button("Token Terminator", tooltip="Terminates a token.", size=(27,1))],
                                   [sg.Button("Hypesquad Changer", tooltip="Changes your Hypesquad.", size=(27,1))],
                                   [sg.Button("Token Checker", tooltip="Checkes if token is valid or not.", size=(27,1))]]

    layout = [#[sg.Menu(menu_def)],
                  [sg.Frame("Available:", frame, font="Any 15", title_color=text_color), sg.Button("Updater", size=(10,1))],
                          [sg.Frame("Links:", links_frame, font="Any 15", title_color=text_color)]]
		  
    window = sg.Window("Program Downloader | v{}".format(rtbversion)).Layout(layout)
    while True:
            event, values = window.Read()
            if event is None or event == 'Exit':
                break
            if event == 'Account':
                sg.Popup("Mist v3#0645")
            elif event == 'Website':
                webbrowser.open("https://mistifiy.netlify.com")      
            elif event == 'Server':
                webbrowser.open("https://discord.gg/Mma5W6k")
            elif event == 'Github':
                webbrowser.open("https://github.com/zerckzzyOase/")
            elif event == 'Twitter':
                webbrowser.open("https://twitter.com/zerckzzy")
            elif event == 'Instagram':
                webbrowser.open("https://instagram.com/zerckzzy")
        
            elif event == 'Duplicator':
                if not os.path.exists("Downloads/"):
                    os.mkdir("Downloads")
                r = requests.get('https://mistifiedbackend.netlify.com/Duplicator.rar')
                with open("Downloads/Duplicator.rar", "wb") as code:
                    code.write(r.content)
                    sg.Popup('Guild Duplicator Downloaded!',title="Done!", keep_on_top=True)
                Archive("Downloads/Duplicator.rar").extractall("Downloads/")
                os.remove('Downloads/Duplicator.rar')

            elif event == 'Nickname Changer':
                if not os.path.exists("Downloads/"):
                    os.mkdir("Downloads")
                r = requests.get('https://mistifiedbackend.netlify.com/NChanger.rar')
                with open("Downloads/Nickname Changer.rar", "wb") as code:
                    code.write(r.content)
                    sg.Popup('Nickname Changer Downloaded!',title="Done!", keep_on_top=True)
                Archive("Downloads/Nickname Changer.rar").extractall("Downloads/")
                os.remove('Downloads/Nickname Changer.rar')
        
            elif event == 'Token Terminator':
                if not os.path.exists("Downloads/"):
                    os.mkdir("Downloads")
                r = requests.get('https://mistifiedbackend.netlify.com/Terminator.rar')
                with open("Downloads/Token Terminator.rar", "wb") as code:
                    code.write(r.content)
                    sg.Popup('Token Terminator Downloaded!',title="Done!", keep_on_top=True)
                Archive("Downloads/Token Terminator.rar").extractall("Downloads/")
                os.remove('Downloads/Token Terminator.rar')
            
            elif event == 'Hypesquad Changer':
                if not os.path.exists("Downloads/"):
                    os.mkdir("Downloads")
                r = requests.get('https://mistifiedbackend.netlify.com/HChanger.rar')
                with open("Downloads/Hypesquad Changer.rar", "wb") as code:
                    code.write(r.content)
                    sg.Popup('Hypesquad Changer Downloaded!',title="Done!", keep_on_top=True)
                Archive("Downloads/Hypesquad Changer.rar").extractall("Downloads/")
                os.remove('Downloads/Hypesquad Changer.rar')
        
            elif event == 'Token Checker':
                if not os.path.exists("Downloads/"):
                    os.mkdir("Downloads")
                r = requests.get('https://mistifiedbackend.netlify.com/Checker.rar')
                with open("Downloads/Token Checker.rar", "wb") as code:
                    code.write(r.content)
                    sg.Popup('Token Checker Downloaded!',title="Done!", keep_on_top=True)
                Archive("Downloads/Token Checker.rar").extractall("Downloads/")
                os.remove('Downloads/Token Checker.rar')
        
            elif event == 'Updater':
                window.Close()
                if "b" in rtbversion:
                    sg.Popup("You are using a test version, be careful.",non_blocking=True,keep_on_top=True,title="MPD Version {}".format(rtbversion))
#                devbuild = requests.get('https://raw.githubusercontent.com/DeadBread76/Raid-Toolbox/dev/version').text
#                devbuild = devbuild.split("|")
                masterbuild = requests.get('https://gist.githubusercontent.com/abcdefghijklmnopqrstuvwxyzzzzzzzz/47d81851984887bc87cb021383fd13b8/raw/6750429a2d1531a8d342d1fbd5e27571dd8e9ca3/asjdgvf').text
                masterbuild = masterbuild.split("|")
                layout = [
                    [sg.Text("Current Version: {}".format(rtbversion))],
                    [sg.Text("Master Branch Version: {}".format(masterbuild[0]),size=(30,1)), sg.Button("Download",size=(15,1),key="Master")],
                    #[sg.Text("Dev Branch Version: {}".format(devbuild[0]),size=(30,1)), sg.Button("Download Dev",size=(15,1),key="Dev")],
                ]
                window = sg.Window("Mist's Program Downloader v{} | Updater".format(rtbversion)).Layout(layout)
                event, values = window.Read()
                if event is None:
                    window.Close()
                    main()
                else:
                    yn = sg.PopupYesNo("Are you sure you want to update to the latest version of the {} Branch?".format(event), title="Update")
                    if yn == "Yes":
                        sg.PopupNonBlocking("Downloading Update...")
                        update = download_file('https://github.com/abcdefghijklmnopqrstuvwxyzzzzzzzz/azcfsfg/archive/{}.zip'.format(event.lower()))
                        shutil.unpack_archive(update)
                        copy_tree("azcfsfg-{}/".format(event.lower()), ".")
                        os.remove(update)
                        sg.Popup("Update complete, Press Ok to exit.")
                        os.kill(os.getpid(), 15)
                    else:
                        window.Close()
                        main()

"""            elif event == "Info":
                while True:
                    window.Close()
                    frame = [
                        [sg.Text("Mist - Creating RTB\nSynchronocy - Inspiring RTB and creating the base for ServerSmasher\nMattlau04 - Writing the Docs and helping me out with general shit\nAliveChive - Squek\ndirt - Creating Themes and Testing\nbukas - Using RTB on the daily and creating showcase video\nNextro - Termux Testing\nColt. - Termux Testing\nLucas. - Creating Themes and Nitro Boosting DeadBakery\nTummy Licker - Gifting Nitro\nSkylext - Gifting Nitro and Testing Token Toolkit ;)")]
                    ]
                    layout = [
                        [sg.Image(data=rtb_banner)],
                        [sg.Text("Version {}".format(rtbversion))],
                        [sg.Text("FuckKord 2019\n\n")],
                        [sg.Frame("Credits/Special Thanks:", frame, font="Any 15", title_color=text_color)],
                    ]
                    window = sg.Window("Mist's Raid ToolBox v{} | Info".format(rtbversion)).Layout(layout)
                    event, values = window.Read()
                    if event is None:
                        window.Close()
                        main()"""

if __name__ == '__main__':      
        main()
