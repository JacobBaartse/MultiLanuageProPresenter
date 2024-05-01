#!/usr/bin/python

import tkinter as tkinter
import tkinter.filedialog as filedialog
import os
from SongEditorPro7Generic import save_song, get_text_block_names
import pickle


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


class simpleapp_tk(tkinter.Tk):
    def __init__(self, parent, output_dir="", text_block_names=None):
        self.output_dir = output_dir
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.labelMessageText = None
        self.text_block_names = text_block_names

    def multiple_view(self, *args):
        for songEntry in self.songEntries:
            songEntry.yview(*args)

    def initialize(self):
        self.entryTitle = tkinter.StringVar()
        self.entry1 = tkinter.Entry(self, textvariable=self.entryTitle, bg='#e0e0e0')
        self.entry1.config(width=57)
        self.entry1.place(x=5, y=30)

        self.labelTitle = tkinter.Label(self, text="Title")
        self.labelTitle.pack()
        self.labelTitle.place(x=5, y=5)

        self.ScrollBar = tkinter.Scrollbar(self)
        self.ScrollBar.config(command=self.multiple_view)
        self.ScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.songEntries = []
        for index, text_block_name in enumerate(text_block_names):
            self.labelSongText = tkinter.Label(self, text=text_block_name)
            self.labelSongText.pack()
            self.labelSongText.place(x=5+index*620, y=125)
            entrySongText = tkinter.Text(width=75, height=37)
            entrySongText.config(yscrollcommand=self.ScrollBar.set, bg='#e0e0e0')
            entrySongText.config(bg='#e0e0e0')
            entrySongText.pack()
            entrySongText.place(x=5+index*620, y=150)
            self.songEntries.append(entrySongText)

        self.labelHint = tkinter.Label(self, text="For available group names see GroupNames.txt")
        self.labelHint.pack()
        self.labelHint.place(x=10, y=800)

        self.entryMessage = tkinter.Text(width=75, height=2)
        self.entryMessage.place(x=10, y=870)

        self.button = tkinter.Button(self, text=u"Save", command=self.on_button_save_click)
        self.button.place(x=300, y=830)

        self.button_open = tkinter.Button(self, text=u"Open recent", command=self.on_button_open_click)
        self.button_open.place(x=100, y=830)

    def on_button_open_click(self):
        file_path_string = filedialog.askopenfilename(initialdir=self.output_dir,
                                                      filetypes=[("song files", "*.pkl")])

        with open(file_path_string, 'rb') as f:
            loaded_dict = pickle.load(f)
        for index, text_block_name in enumerate(self.text_block_names):
            self.songEntries[index].insert(tkinter.END, "\n".join(loaded_dict[text_block_name]))
        file_path_string.replace("\\", "/")
        self.entryTitle.set(file_path_string.replace(".pkl", "").split("/")[-1])

    def on_button_save_click(self):
        title = self.entryTitle.get()
        for char in r":\\|/?*&^%$#@!~`'\";,.<>"+"\r\n":
            title.replace(char, " ")

        title = title.strip()
        song_texts = {}
        for index, text_block_name in enumerate(text_block_names):
            song_texts[text_block_name] = self.songEntries[index].get("1.0", tkinter.END).split("\n")

        try:
            title = title.rstrip()
            output_filename = os.path.join(self.output_dir, title)
            save_song(text_block_names, song_texts, output_filename)

            self.entryMessage.delete('1.0', tkinter.END)
            self.entryMessage.insert(tkinter.END, 'import in Pro presenter: "file", "import", "import file", ' + output_filename)
        except NameError as ne:
            self.entryMessage.delete('1.0', tkinter.END)
            self.entryMessage.insert(tkinter.END, "ERROR" + str(ne))


if __name__ == "__main__":
    text_block_names = get_text_block_names()
    num_languages = len(text_block_names)

    output_dir = get_download_path()

    app = simpleapp_tk(None, output_dir=output_dir, text_block_names=text_block_names)

    gui_with = 640*num_languages
    app.geometry(str(gui_with) + "x930+0+0")
    app.title('Song editor for ProPresenter7')

    app.mainloop()
