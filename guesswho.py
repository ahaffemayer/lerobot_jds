import random
import time

import keyboard
import numpy as np
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot

from animals import animals_dict


class GuessWho:
    def __init__(self, ai_player=True) -> None:
        # Initialize the robot
        self.robot = ManipulatorRobot(config)
        self.ai_player = ai_player
        self.mode = None
        self.chosen_animal = None
        self.home_position = [0, 120, 135, -5, -5, -85, 0]
        self.playing = True

    def get_board_img(self):
        # Move to observation image
        self.robot.send_action(self.home_position)

        # Capture image
        board_img = self.robot.capture_observation()
        return board_img

    def launch(self):
        # Get the board image

        # Choose a random animal
        if self.ai_player:
            self.chosen_animal = self.choose_animal()


        # Deciding who start with "coin flip"
        coing_flip = np.random.random(1)
        if coing_flip > 0.5:
            self.your_turn = False
        else:
            self.your_turn = True

        # Announce who is starting


        # Play
        while self.playing:
            if self.your_turn:
                if self.ai_player:
                    remaining_animals = self.ask()
                    animals_to_be_removed = [animal for animal in animals_dict.keys() if animal not in remaining_animals]
                else:
                    animals_to_be_removed = self.listen()
                    remaining_animals = [animal in remaining_animals if animal is not in animals_to_be_removed]

                self.update_board(animals_to_be_removed)

                # Condition for winning
                if len(remaining_animals)==1:
                    print("You have won")

            else:
                if self.ai_player:
                    self.listen_and_answer()
                    keyboard.wait("space")

            self.your_turn  = not self.your_turn

    def choose_animal(self):
        """Choose the animal that the other player will have to guess"""
        animals = list(animals_dict.keys())
        animal = random.choice(animals)
        return animal

    def listen_and_answer(self):
        """
        Answer the question from the other player on the characteristics on the chosen image
        """

    def ask(self):
        """
        Find the optimal question for winning depending on images left and ask it
        """

    def update_board(self, animals):
        """Given the list of animals to conceal, performs the actions with lerobot"""

        
    def listen(self):
        """Listens to the commands from the human user to remove which animals"""
        return animals_to_be_removed
