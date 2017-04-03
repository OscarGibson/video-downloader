import sys, os, io

import tkinter as tk
from download import videoDownloader

LARGE_FONT = ('Veranda', 12)

from contextlib import contextmanager

class GUIToDownloader(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky='nswe')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    class IORedirector():
       def __init__(self,text_area, oldstdout=None):
          self.text_area = text_area
          self.oldstdout = oldstdout
    class StdoutRedirector(IORedirector):
       def write(self,message):
          self.text_area.configure(state = 'normal')
          self.text_area.insert('end', message)
          self.text_area.see('end')
          #self.text_area.configure(state = 'disabled')
          if self.oldstdout:
                pass#self.oldstdout.write('message was inserted\n')

       def flush(self):
           pass

    def enable_disable(self,check, *target):
        for t in target:
            if check:
                t.configure(state='normal')
            else:
                t.configure(state='disabled')

    def output_data(self,into,**kwargs):

        stek = []
        sys.stdout = self.StdoutRedirector(into, sys.stdout)

        d = {}
        url = kwargs['url']
        d['outtmpl'] = self.format_path(kwargs['path'])
        d['newline'] = True

        if kwargs['format']:
            d['fromat'] = 'bestaudio/best'
        if kwargs['auth']:
            d['username'] = kwargs['uname']
            d['password'] = kwargs['password']
        if not(kwargs['playlist']):
            d['noplaylist'] = True

        vd = videoDownloader(**d)
        vd.download(url)

    def format_path(self, path):
        if path and (path[len(path)-1] != '/'):
            path += '/'
        path += '%(title)s.%(ext)s'
        return path


    def __init__(self, parent, controler):
        tk.Frame.__init__(self, parent)

        page_label = 'Welcome to video downloader'

        main_label = tk.Label(self, text=page_label, font=LARGE_FONT)

        download_button = tk.Button(self, text='DOWNLOAD', command= lambda:\
        self.output_data(into=text_output_box,format=check_var.get(), \
        playlist=radio_var.get(), \
        auth=check_up_var.get(), url=url_entry.get(), path=path_entry.get(), \
        uname=uname_entry.get(), password=pass_entry.get()))

        check_var = tk.IntVar()
        radio_var = tk.IntVar()
        check_up_var = tk.IntVar()

        checkHD_label = tk.Label(self, text='HD')
        checkHD = tk.Checkbutton(self, text = "HD", variable = check_var, \
                         onvalue = 1, offvalue = 0, height=2, \
                         width = 10)

        url_label = tk.Label(self, text="Enter URL to download")
        url_entry = tk.Entry(self, bd= 2)

        path_label = tk.Label(self, text="Path to files download")
        path_entry = tk.Entry(self, bd= 2)

        check_UP = tk.Checkbutton(self, text='Is user name and password required?',\
        variable= check_up_var, onvalue= 1, offvalue= 0, command=\
        lambda: self.enable_disable(check_up_var.get(),uname_entry,pass_entry))

        uname_label = tk.Label(self, text="Enter user name")
        uname_entry = tk.Entry(self, bd= 2, state='disabled')

        pass_label = tk.Label(self, text="Enter password")
        pass_entry = tk.Entry(self, bd= 2, state='disabled')

        playlist_radio = tk.Radiobutton(self, text="playlist", \
            variable=radio_var, value=1)

        single_video_radio = tk.Radiobutton(self, text="single video", \
            variable=radio_var, value=0)

        text_output_box = tk.Text(self, wrap= 'word', height= 11, width= 50,\
        state= 'disabled')

        main_label.grid(row=0, sticky='we', padx=10)

        url_label.grid(row=1,column=0, sticky='w')
        url_entry.grid(row=1,column=1)

        path_label.grid(row=2,column=0, sticky='w')
        path_entry.grid(row=2,column=1)

        check_UP.grid(row=3,column=0)

        uname_label.grid(row=4,column=0, sticky='w')
        uname_entry.grid(row=4,column=1)

        pass_label.grid(row=5,column=0, sticky='w')
        pass_entry.grid(row=5,column=1)

        checkHD.grid(column=2,row=1)

        playlist_radio.grid(column=2,row=2, sticky='w')
        single_video_radio.grid(column=2,row=3, sticky='w')

        download_button.grid(column=2,row=4, rowspan= 2)

        text_output_box.grid(row=6, column=0, columnspan=2)
