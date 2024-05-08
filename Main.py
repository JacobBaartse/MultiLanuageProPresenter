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
        return os.path.join(os.path.expanduser('~'), 'Downloads')


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
        self.labelTitle = tkinter.Label(self, text="Song name:")
        self.labelTitle.pack()
        self.labelTitle.place(x=5, y=20)
        self.entryTitle = tkinter.StringVar()
        self.entry1 = tkinter.Entry(self, textvariable=self.entryTitle, bg='#e0e0e0')
        self.entry1.config(width=57)
        self.entry1.place(x=95, y=20)

        self.labelTitleCount = tkinter.Label(self, text="Number of lines per slide:")
        self.labelTitleCount.pack()
        self.labelTitleCount.place(x=5, y=60)
        self.entryLineCount = tkinter.StringVar()
        self.entry2 = tkinter.Entry(self, textvariable=self.entryLineCount, bg="#e0e0e0")
        self.entry2.config(width=6)
        self.entry2.place(x=175, y=60)
        self.entryLineCount.set("2")

        self.ScrollBar = tkinter.Scrollbar(self)
        self.ScrollBar.config(command=self.multiple_view)
        self.ScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.songEntries = []
        for index, text_block_name in enumerate(text_block_names):
            self.labelSongText = tkinter.Label(self, text=text_block_name)
            self.labelSongText.pack()
            self.labelSongText.place(x=5+index*520, y=100)
            entrySongText = tkinter.Text(width=64, height=38)
            entrySongText.config(yscrollcommand=self.ScrollBar.set, bg='#e0e0e0')
            entrySongText.config(bg='#e0e0e0')
            entrySongText.pack()
            entrySongText.place(x=5+index*520, y=125)
            self.songEntries.append(entrySongText)

        with open("GroupNames.txt", "r") as group_names:
            labels = group_names.read().split("\n")
        label_string = ""
        num_labels_per_line = 13
        for index in range((len(labels)//num_labels_per_line)+1):
            label_string += "  ".join(labels[index*num_labels_per_line:(index+1)*num_labels_per_line]) + "\n"

        self.labelHint = tkinter.Label(self, text="Add group names to GroupNames.txt   \n" + label_string)
        self.labelHint.pack()
        self.labelHint.place(x=230, y=780)

        self.entryMessage = tkinter.Text(width=75, height=2)
        self.entryMessage.place(x=10, y=870)

        self.button = tkinter.Button(self, text=u"Save", command=self.on_button_save_click)
        self.button.place(x=150, y=830)

        self.button_open = tkinter.Button(self, text=u"Open recent", command=self.on_button_open_click)
        self.button_open.place(x=20, y=830)

    def on_button_open_click(self):
        file_path_string = filedialog.askopenfilename(initialdir=self.output_dir,
                                                      filetypes=[("song files", "*.pkl")])

        with open(file_path_string, 'rb') as f:
            loaded_dict = pickle.load(f)

        for index, text_block_name in enumerate(self.text_block_names):
            self.songEntries[index].delete(1.0, tkinter.END)  # required for linux

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
            try:
                max_line_count = int(self.entryLineCount.get())
            except:
                self.entryLineCount.set("2")
                max_line_count = 2

            save_song(text_block_names, song_texts, max_line_count, output_filename)

            self.entryMessage.delete('1.0', tkinter.END)
            self.entryMessage.insert(tkinter.END, 'import in Pro presenter: "file", "import", "import file", ' + output_filename)
        except Exception as ne:
            self.entryMessage.delete('1.0', tkinter.END)
            self.entryMessage.insert(tkinter.END, "ERROR" + str(ne))


if __name__ == "__main__":
    text_block_names = get_text_block_names()
    num_languages = len(text_block_names)

    output_dir = get_download_path()

    app = simpleapp_tk(None, output_dir=output_dir, text_block_names=text_block_names)

    gui_with = 540*num_languages
    app.geometry(str(gui_with) + "x930+0+0")
    app.title('Song editor for ProPresenter7')

    app.mainloop()
