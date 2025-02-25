
from tkinter import *
from functools import partial  # To prevent unwanted windows



# Class start here
class StartGame:
    """
    Initial Game interface (Asks users how many rounds they
    would like to play
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button...

        self.hints_button = Button(self.start_frame, font=("Arial", "14", "bold"),
                                  fg="#FFFFFF", bg="#FF8000", padx=10, pady=10, text="Hints", width=10,
                                  command=self.to_hints)
        self.hints_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints for playing game
        """
        DisplayHints(self)



class DisplayHints:
    """
    Interface for playing the Colout Quest Game
    """
    """
    Displays hints dialogue box
    """

    def __init__(self, partner):
        # Setup dialogue box and background colour
        background = "#ffe6cc"
        self.hints_box = Toplevel()

        # Disable hints box
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes hints and
        # 'releases' hints button
        self.hints_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hints, partner))

        self.hints_frame = Frame(self.hints_box, width=300,
                                height=200)
        self.hints_frame.grid()

        self.hints_heading_label = Label(self.hints_frame,
                                        text="Hints",
                                        font=("Arial", "14", "bold"))
        self.hints_heading_label.grid(row=0)

        hints_text = ("The score for each colour relates to it's hexadecimal code.\n\n"
                      "Remember, the hex code for white is #FFFFFF - which is the best score.\n\n"
                      "The hex code for black is #000000 which is the worst possible score.\n\n"
                      "The first colour in the code is red, so if you had to choose between red (#FF0000), green (#00FF00) and blue (#0000FF), then red would be the best choice.\n\n"
                      "Good luck!")

        self.hints_text_label = Label(self.hints_frame,
                                     text=hints_text,
                                     wraplength=350, justify="left")
        self.hints_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hints_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.hints_frame, self.hints_heading_label,
                         self.hints_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_hints(self, partner):
        """
        Closes Hints dialogue box (and enables hints button
        """

        # Put hints button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.hints_box.destroy()



# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
