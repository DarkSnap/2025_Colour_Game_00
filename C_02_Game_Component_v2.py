import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from numpy.random import normal


# Helper functions go here


def get_colours():
    """
    Retrieves colours from csv file
    :return: list of colours which were each list item has the
    colour name, associated score and foreground colour for the text
    """

    file = open("00_colour_list_hex_v3.csv", "r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row
    all_colours.pop(0)

    return all_colours


def get_round_colours():
    """
    Choose four colours from larger list ensuring that the scores are all different.
    :return: List of colours and score to beat (median of scores)
    """
    all_colour_list = get_colours()

    round_colours = []
    colour_scores = []

    # Loop until we have four colours with different scores...
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colour_list)

        # Get the score and check it's not a duplicate
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)

            colour_scores.append(potential_colour[1])

    # Chance scores to integers
    int_scores = [int(x) for x in colour_scores]

    int_scores.sort()
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colours, median


def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
    :return: Rounded number (an integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = f"{var_rounded:.0f}"
    return int(raw_rounded)


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

        # Create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        Play(5)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:
    """
    Interface for playing the Colout Quest Game
    """

    def __init__(self, how_many):

        #Integers / String Variables
        self.target_score = IntVar()

        # Rounds played | start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels...
        body_font = ("Arial", "12")

        # Lists for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good luck.", body_font, "#D5E8D4", 2],
            ["You choose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # Set up colour buttons...
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.colour_button_ref = []
        self.button_colours_list = []

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.colour_button  = Button(self.colour_frame, font=body_font,
                                         text="Colour Name", width=15,
                                         command=partial(self.rounds_results, item))
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

            self.colour_button_ref.append(self.colour_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 30, 7, None]
        ]

        # Create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured.
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface has been created, invoke new
        # Round function for first round.
        self.new_round()

    def new_round(self):
        """
        Choose four colours, works out median for score to beat,
        Configures buttons with chosen colours
        """

        # Retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # Get round colours and median score...
        self.round_colour_list, median = get_round_colours()

        # Set target score as median (For later comparison)
        self.target_score.set(median)

        # Update heading, and score to beat labels. "Hide" results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target Score: {median}", font="Arial" "14" "bold")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # Configure buttons using foreground and background colours from list
        #enable colour buttons (disable at the end of the last round)
        for count, item in enumerate(self.colour_button_ref):
            item.config(fg=self.round_colour_list[count][2],
                        bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def rounds_results(self, user_choice):
        """
        Retrieves which button has pushed (index 0 - 3),
        retrieves score and then compares it with median,
        updates results and adds results to stats list.
        """
        # Get user score and colour based on button press...
        score = int(self.round_colour_list[user_choice][1])

        # Alternate way to get button name. Good for if buttons have been scrambled!
        colour_name = self.colour_button_ref[user_choice].cget('text')

        # Retrieve target score and compare with user score to find round results
        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success!! {colour_name} earned you {score} points"
            result_bg = "#82B366"
            self.all_scores_list.append(score)

        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # Enable stats & next buttons, disable color buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.colour_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
