from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *
import tkinter as tk

pygame.init()

MAX_SIZE = "500x440"
MIN_SIZE = "500x120"

def exit_app():
    """
    Quit mp3 player gracefully.
    :return:
    """
    app.app_running = False
    app.destroy()
    window.quit()


class FrameApp(Frame):
    def __init__(self, master):
        super(FrameApp, self).__init__(master)

        self.app_running = True
        self.grid()
        self.paused = False
        self.stopped = False
        self.playlist = list()
        self.actual_song = 0
        self.max_size = True

        # Row 1
        self.main_box = Frame(self)
        self.main_box.grid(row=1, column=1, columnspan=5, padx=8, pady=8)

        self.b1 = Button(self.main_box, text="\u25B6", command=self.play_music, bg='Lavender', width=4)
        self.b1.grid(row=1, column=1)

        self.b2 = Button(self.main_box, text="\u25B6", command=self.toggle, bg='Lavender', width=4)
        self.b2.grid(row=1, column=2)

        self.b3 = Button(self.main_box, text="|\u25C0\u25C0", command=self.previous_song, bg='Lavender', width=4)
        self.b3.grid(row=1, column=3)

        self.b4 = Button(self.main_box, text="\u25B6\u25B6|", command=self.next_song, bg='Lavender', width=4)
        self.b4.grid(row=1, column=4)

        self.b5 = Button(self.main_box, text="\u25A0", command=self.stop_song, bg='Lavender', width=4)
        self.b5.grid(row=1, column=5)

        self.l6 = Label(self.main_box, text=" ", bg='white', width=4)
        self.l6.grid(row=1, column=6)

        self.b7 = Button(self.main_box, text="min", command=self.resize, bg='Lavender', width=4)
        self.b7.grid(row=1, column=7)

        self.l8 = Label(self.main_box, text=" ", bg='white', width=2)
        self.l8.grid(row=1, column=8)

        self.b9 = Button(self.main_box, text="exit", command=exit_app, bg='Lavender', width=4)
        self.b9.grid(row=1, column=9)

        # Row 2, 3
        self.second_box = Frame(self)
        self.second_box.grid(row=2, column=1, columnspan=5, padx=8, pady=8)

        self.song_label = Label(self.second_box, fg='Black', font=('Helvetica 12 bold italic', 10), bg='white')
        self.song_label.grid(sticky=('n', 's', 'w', 'e'), row=0, column=1, columnspan=5, pady=8)

        self.album_label = Label(self.second_box, fg='Black', font=('Helvetica 12 bold italic', 10), bg='Lavender', wraplength=380)
        self.album_label.grid(sticky=('n', 's', 'w', 'e'), row=1, column=1, columnspan=5, pady=8)

        self.b0 = Button(self.second_box, text="ADD TO PLAYLIST", command=self.add_to_list, bg='Lavender', width=15)
        self.b0.grid(row=2, column=1, pady=8)

        self.b6 = Button(self.second_box, text="CLEAR PLAYLIST", command=self.clear_list, bg='Lavender', width=15)
        self.b6.grid(row=2, column=2)

        # Row 4
        self.container_box = Frame(self)
        self.container_box.grid(row=10, column=1, columnspan=5, padx=8, pady=8)

        self.play_list = Listbox(self.container_box, font='Helvetica 10', bg='white', width=50, height=14,
                                 selectmode=SINGLE)
        self.play_list.pack(side=LEFT, fill=BOTH)
        self.play_list.bind("<<ListboxSelect>>", self.select_song)

        self.scrollbar = Scrollbar(self.container_box)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        self.play_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.play_list.yview)

        # set event to not predefined value in pygame
        self.SONG_END = pygame.USEREVENT + 1

    def add_to_list(self):
        """
        Opens window to browse data on disk and adds selected songs to play list
        :return: None
        """
        directory = askopenfilenames()
        # appends song directory on disk to playlist in memory
        for song_dir in directory:
            self.playlist.append(song_dir)

        self.play_list.delete(0, END)  # Clear the song list box

        for key, item in enumerate(self.playlist):
            # appends song to listbox
            song = EasyID3(item)
            print(f'SONG {song}')
            if 'title' in song.keys():
                song_data = (str(key + 1) + ' : ' + song['title'][0])
            else:
                song_data = (str(key + 1) + ' : ' + item)
            self.play_list.insert(key, song_data)
        self.play_list.select_set(self.actual_song)

    def clear_list(self):
        """
        Stops music and clears the playlist
        :return:
        """
        self.stop_song()
        self.album_label['text'] = " "
        self.song_label['text'] = " "
        self.playlist.clear()
        self.play_list.select_clear(0, END)
        self.play_list.delete(0, END)  # Clear the song list box
        self.actual_song = 0

    def now_playing(self):
        """
        Makes string of current playing song data over the text box
        :return: string - current song data
        """
        self.play_list.select_clear(0, END)
        self.play_list.select_set(self.actual_song)
        song = EasyID3(self.playlist[self.actual_song])
        if 'title' in song.keys():
            song_data = str(self.actual_song + 1) + " : " + \
                        str(song['title'][0]) + " - " + str(song['artist'])
            self.album_label['text'] = str(song['album'][0])
        else:
            song_data = str(self.play_list.selection_get())
            self.album_label['text'] = 'ALBUM HERE'
        return song_data

    def play_music(self):
        """
        Loads current song, plays it, sets event on song finish
        :return: None
        """
        if self.play_list.size() > 0:

            directory = self.playlist[self.actual_song]
            print(directory)
            pygame.mixer.music.load(directory)
            pygame.mixer.music.play(1, 0.0)
            pygame.mixer.music.set_endevent(self.SONG_END)
            self.paused = False
            self.b2.config(text='||')
            self.song_label['text'] = self.now_playing()

    def check_music(self):
        """
        Listens to END_MUSIC event and triggers next song to play if current
        song has finished
        :return: None
        """
        for event in pygame.event.get():
            if event.type == self.SONG_END and not self.stopped:
                self.next_song()

    def toggle(self):
        """
        Toggles current song
        :return: None
        """
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.b2.config(text='||')
        elif not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.b2.config(text='\u25B6')

    def get_next_song(self):
        """
        Gets next song number on playlist
        :return: int - next song number
        """
        if self.actual_song + 2 <= len(self.playlist):
            return self.actual_song + 1
        else:
            return 0

    def next_song(self):
        """
        Plays next song
        :return: None
        """
        self.actual_song = self.get_next_song()
        self.play_music()

    def get_previous_song(self):
        """
        Gets previous song number on playlist and returns it
        :return: int - previous song number on playlist
        """
        if self.actual_song - 1 >= 0:
            return self.actual_song - 1
        else:
            return len(self.playlist) - 1

    def previous_song(self):
        """
        Plays previous song
        :return:
        """
        self.actual_song = self.get_previous_song()
        self.play_music()

    def stop_song(self):
        """
        Plays previous song
        :return:
        """
        self.stopped = True
        pygame.mixer.music.stop()

    def select_song(self, event):
        """
        Play song selected from playlist.
        :param event:
        :return:
        """
        selection = event.widget.curselection()
        self.actual_song = selection[0]
        self.play_music()

    def resize(self):
        """
        Toggle window size.
        :return:
        """

        if self.max_size:
            window.geometry(MIN_SIZE)
            self.b7.config(text='max')
            self.max_size = False
        else:
            window.geometry(MAX_SIZE)
            self.b7.config(text='min')
            self.max_size = True


window = Tk()
window.geometry(MAX_SIZE)
window.config(padx=10,pady=10)
window.title("MP3 Music Player")

app = FrameApp(window)
try:
    icon_img = tk.PhotoImage(file="~/PycharmProjects/mp3/mp3.png")
    window.iconphoto(False, icon_img)
except tk.TclError:
    print("mp3.png not found. Using default icon.")

while app.app_running:
    # runs mainloop of program
    app.check_music()
    try:
        app.update()
    except TclError:
        # Someone closed the app using the Close 'X' instead of the Exit button
        pass
