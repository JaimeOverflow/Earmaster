import tkinter as tk
import random
from subprocess import Popen, DEVNULL, STDOUT

from NoteGenerator import NoteGenerator
from Settings import COLOR_BLUE_DARK, COLOR_BLUE_SKY, \
    COLOR_ENABLED, COLOR_DISABLED, \
    MODE, MODE_FREE, MODE_GUESS_NOTE

class MainGUI():


    def __init__(self):
        self.noteGenerator = NoteGenerator()
        self.btns_notes = []
        self.mode = MODE
        self.random_note = None
        self.random_notes = []

        self.initWindow()
        self.initSettings()
        self.initNotesGrid()

        self.window.mainloop()


    def initWindow(self):
        self.window = tk.Tk()
        self.window.title("Earmaster")

    def initSettings(self):
        frame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=0, column=0)
        self.btn_repeat = tk.Button(
            master=frame,
            text="Repeat",
            command=lambda :self.repeat_note(),
            width=10,
            height=5)
        self.btn_repeat.pack()

        frame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=0, column=1)
        self.btn_another = tk.Button(
            master=frame,
            text="Another",
            command=lambda :self.another_note(),
            width=10,
            height=5)
        self.btn_another.pack()

        frame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=0, column=2)
        self.btn_mode = tk.Button(
            master=frame,
            text="Mode free",
            command=lambda : self.change_mode(),
            width=10,
            height=5)
        self.btn_mode.pack()

    def initNotesGrid(self):
        for i in range(1, self.noteGenerator.get_num_strings()):
            buttons_row = []
            for j in range(self.noteGenerator.get_num_flets()):

                bg = COLOR_BLUE_DARK
                if j % 2 != 0:
                    bg = COLOR_BLUE_SKY

                frame = tk.Frame(
                    master=self.window,
                    relief=tk.RAISED,
                    borderwidth=1
                )

                frame.grid(row=i, column=j)
                button = tk.Button(
                    master=frame,
                    fg=COLOR_DISABLED,
                    bg=bg,
                    text=self.noteGenerator.get_note(i - 1, j),
                    command=lambda string=i - 1, flet=j: self.play_note(string, flet),
                    width=10,
                    height=5
                )

                button.bind("<Button-3>", lambda handler, string=i-1, flet=j: self.change_state_button(handler, string, flet))
                button.pack()
                buttons_row.append(button)

            self.btns_notes.append(buttons_row)

    def change_state_button(self, event, string, flet):
        if self.btns_notes[string][flet].cget("fg") == COLOR_DISABLED:
            self.btns_notes[string][flet].config(fg=COLOR_ENABLED)

            self.random_notes.append((string, flet))
            self.random_note = random.choice(self.random_notes)
            note = self.noteGenerator.get_note(self.random_note[0], self.random_note[1])

            filepath_note = "Notes/{note}.m4a".format(note=note)
            Popen(["mplayer", filepath_note], stdout=DEVNULL, stderr=STDOUT)

        else:
            self.btns_notes[string][flet].config(fg=COLOR_DISABLED)
            note_to_disable = (string, flet)

            self.random_notes.remove(note_to_disable)

            if self.random_note == note_to_disable:
                self.random_note = random.choice(self.random_notes)
                note = self.noteGenerator.get_note(self.random_note[0], self.random_note[1])

                filepath_note = "Notes/{note}.m4a".format(note=note)
                Popen(["mplayer", filepath_note], stdout=DEVNULL, stderr=STDOUT)


    def play_note(self, string, flet):
        if self.mode == MODE_FREE:
            note = self.noteGenerator.get_note(string, flet)
            filepath_note = "Notes/{note}.m4a".format(note=note)
            Popen(["mplayer", filepath_note], stdout=DEVNULL, stderr=STDOUT)

        elif self.mode == MODE_GUESS_NOTE:
            note_pressed = (string, flet)
            if self.random_note == note_pressed:
                self.random_note = random.choice(self.random_notes)
                note = self.noteGenerator.get_note(self.random_note[0], self.random_note[1])

                filepath_note = "Notes/{note}.m4a".format(note=note)
                Popen(["mplayer", filepath_note], stdout=DEVNULL, stderr=STDOUT)

    def change_mode(self):

        if self.mode == MODE_FREE:
            self.mode = MODE_GUESS_NOTE
            self.btn_mode.config(text="mode free")
        else:
            self.mode = MODE_FREE
            self.btn_mode.config(text="mode guess")

    def repeat_note(self):
        if self.random_note:
            note = self.noteGenerator.get_note(self.random_note[0], self.random_note[1])

            filepath_note = "Notes/{note}.m4a".format(note=note)
            Popen(["mplayer", filepath_note], stdout=DEVNULL, stderr=STDOUT)

    def another_note(self):
        if self.random_note:
            self.random_note = random.choice(self.random_notes)
            note = self.noteGenerator.get_note(self.random_note[0], self.random_note[1])

            filepath_note = "Notes/{note}.m4a".format(note=note)
            Popen(["mplayer", filepath_note], stdout=DEVNULL, stderr=STDOUT)