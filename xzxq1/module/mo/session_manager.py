import random
import json
from module.games.glass.GlassGame import GlassGame
from module.games.roulette.RouletteGame import RussianRoulette
from module.games.rps.RPSGame import RockPaperScissorsGame
from module.games.video.video import VideoPlayer
from module.games.rg.rg import SquidGame


class SessionManager:
    def __init__(self):
        self.games = [GlassGame, RussianRoulette, RockPaperScissorsGame, VideoPlayer, SquidGame]
        self.current_game = None
        self.game_states = []

    def run_session(self):
        """Run the gaming session sequentially."""
        for _ in range(len(self.games)):
            self.select_random_game()
            result = self.run_current_game()
            print(f"Game result: {result}")
            if result == "lose":
                break  # End session if the player loses

    def select_random_game(self):
        """Select a random game from the available games."""
        self.current_game = random.choice(self.games)()

    def run_current_game(self):
        """Run the currently selected game."""
        if self.current_game:
            result = self.current_game.run()
            self.save_game_state()
            return result  # Return the result of the game

    def save_game_state(self):
        """Save the current game state."""
        game_state = {
            "game": self.current_game.__class__.__name__,
            "state": self.current_game.__dict__  # Save the current state of the game
        }
        self.game_states.append(game_state)
        with open('session_state.json', 'w') as f:
            json.dump(self.game_states, f)

    def load_game_state(self):
        """Load the game state from a file."""
        try:
            with open('session_state.json', 'r') as f:
                self.game_states = json.load(f)
        except FileNotFoundError:
            print("No saved session found.")

    def reset_session(self):
        """Reset the session for a new game."""
        self.game_states = []
        self.current_game = None
