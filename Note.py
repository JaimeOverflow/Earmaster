
class Note:

    def __init__(self, note, string, flet):
        # Format "note-sharp-level" without hyphen
        # Example: A#4
        self.note = str(note[0])
        self.is_sharp = True if "#" in note else False
        self.level = int(note[-1])
        self.string = string
        self.flet = flet

    def getNote(self):
        note = "{note}{sharp}{level}".format(
            note=self.note,
            sharp="#" if self.is_sharp else "",
            level=str(self.level)
        )
        return note


    def getFullNote(self):
        note = self.getNote()

        result = "String {string} - Flet {flet} - Note {note}".format(
            string=self.string,
            flet=self.flet,
            note=note
        )
        return result

    def __str__(self):
        return self.getFullNote()
