import sys
import youtube_dl

class videoDownloader():
    __options_pattern = ['username','password','outtmpl','format','noplaylist']

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
                try:
                    ydl.extract_info(url)
                except Exception as e:
                    print('ERROR: invalid URL')
                    raise

        except (RuntimeError, TypeError, NameError):
            print('ERROR: downloading fall')
            #sys.exit(1)
        return info_dict

    def get_info(self, info, *args):
        all_info = {}

        for a in args:
            i = info.get(a, None)
            if i: all_info[a] = i

        return all_info
