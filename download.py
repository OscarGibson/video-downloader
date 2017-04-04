import sys
import youtube_dl

from threading import Thread as tr
from threading import Lock



class videoDownloader():
    __options_pattern = ['username','password','outtmpl','format',\
    'noplaylist', 'logger', 'progress_hooks']

    def __init__(self, **kwargs):
        self.ydl_opts = self.__set_values(self.__options_pattern, kwargs)

    def set_options(self, **kwargs):
        self.ydl_opts = self.__set_values(self.__options_pattern, kwargs)

    def __set_values(self, options_pattern, kwargs):
        options = {}
        for name, value in kwargs.items():
            if (name in options_pattern):
                options[name] = value
        return options

    def print_kw(self):
        print(self.ydl_opts)

    def download(self, url):
        ydl_opts = self.ydl_opts
        info_dict = None

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                thread = tr(target= ydl.download, args= ([url], ))
                lock = Lock()
                with lock:
                    #thread = tr(target= ydl.download, args= ([url], ))
                    thread.start()


        except (RuntimeError, TypeError, NameError):
            print('ERROR: downloading fall')
            raise
        return info_dict

    def get_info(self, info, *args):
        all_info = {}

        for a in args:
            i = info.get(a, None)
            if i: all_info[a] = i

        return all_info
