import time
import os
import sys
import random
from threading import Thread

class NonInfingingBirdPipeGame():
    def __init__(self):
        self.pipe_segment = '#'
        self.sky = ' '
        self.bird = '*'
        self.is_flap = False
        self.flap_count = 1
        self.max_flaps = 2
        self.is_dead = False
        self.score = 0
        
        s = self.sky
        b = self.bird
        p = self.pipe_segment
        self.game_state = {
            "r1": {
                "c1": s,
                "c2": s,
                "c3": s,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": p,
                "c10": s,
                "c11": s,
                "c12": s
            },
            "r2": {
                "c1": s,
                "c2": s,
                "c3": s,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": p,
                "c10": s,
                "c11": s,
                "c12": s
            },
            "r3": {
                "c1": s,
                "c2": s,
                "c3": s,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": s,
                "c10": s,
                "c11": s,
                "c12": s
            },
            "r4": {
                "c1": s,
                "c2": s,
                "c3": b,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": s,
                "c10": s,
                "c11": s,
                "c12": s
            },
            "r5": {
                "c1": s,
                "c2": s,
                "c3": s,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": p,
                "c10": s,
                "c11": s,
                "c12": s
            },
            "r6": {
                "c1": s,
                "c2": s,
                "c3": s,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": p,
                "c10": s,
                "c11": s,
                "c12": s
            },
            "r7": {
                "c1": s,
                "c2": s,
                "c3": s,
                "c4": s,
                "c5": s,
                "c6": s,
                "c7": s,
                "c8": s,
                "c9": p,
                "c10": s,
                "c11": s,
                "c12": s
            },
        }

        # Start thread to handle user input
        Thread(target = self.handle_input, daemon = True).start()

    def print_state(self):
        for row in self.game_state.keys():
            for col in self.game_state[row].keys():
                print(self.game_state[row][col], flush=True, end="")
            print("")
        print("")

    def handle_input(self):
        import platform
        while (True):
            if "linux" in platform.platform().lower():
                import getch
                user_input = getch.getch()
            elif "windows" in platform.platform().lower():
                import msvcrt
                user_input = msvcrt.getch()
            else:
                print("OS NOT SUPPORTED LMAO XD")
                exit(1)
            if " " in str(user_input): 
                self.is_flap = True
            #else: 
            #    self.is_flap = False

    def next_frame(self):
        def make_pipes(current_game_state):
            type_1 = {
                "r1": self.pipe_segment,
                "r2": self.pipe_segment,
                "r3": self.sky,
                "r4": self.sky,
                "r5": self.pipe_segment,
                "r6": self.pipe_segment,
                "r7": self.pipe_segment
            }
            type_2 = {
                "r1": self.pipe_segment,
                "r2": self.sky,
                "r3": self.sky,
                "r4": self.pipe_segment,
                "r5": self.pipe_segment,
                "r6": self.pipe_segment,
                "r7": self.pipe_segment
            }
            type_3 = {
                "r1": self.pipe_segment,
                "r2": self.pipe_segment,
                "r3": self.pipe_segment,
                "r4": self.sky,
                "r5": self.sky,
                "r6": self.pipe_segment,
                "r7": self.pipe_segment
            }
            type_4 = {
                "r1": self.pipe_segment,
                "r2": self.pipe_segment,
                "r3": self.pipe_segment,
                "r4": self.pipe_segment,
                "r5": self.sky,
                "r6": self.sky,
                "r7": self.pipe_segment
            }
            types = [type_1, type_2, type_3, type_4]
            new_pipes = types[random.randrange(0,4,1)]
            for row in current_game_state.keys():
                current_game_state[row]['c12'] = new_pipes[row]

        has_bird_moved = False
        is_make_pipe = False
        for row in self.game_state.keys():
            for col in self.game_state[row].keys():
                current_row = int(row.split('r')[1])
                current_col = int(col.split('c')[1])
                # Make new pipes
                if current_col == 3: 
                    if self.game_state['r1'][f'c{current_col - 1}'] == self.sky and self.game_state['r1'][f'c{current_col}'] == self.pipe_segment and self.game_state['r1'][f'c{current_col+1}'] == self.sky:
                        if self.game_state['r7'][f'c{current_col - 1}'] == self.sky and self.game_state['r7'][f'c{current_col}'] == self.pipe_segment and self.game_state['r7'][f'c{current_col+1}'] == self.sky:
                            if is_make_pipe == False:
                                is_make_pipe = True
                # Move old pipes
                if self.pipe_segment in self.game_state[row][col]:
                    if current_col != 1:
                        self.game_state[row][f'c{current_col - 1}'] = self.pipe_segment
                        self.game_state[row][col] = self.sky
                    else:
                        self.game_state[row][col] = self.sky
                # Move bird
                if self.bird in self.game_state[row][col] and has_bird_moved == False:
                    # Move bird up
                    if self.is_flap == True:
                        if current_row != 1:
                            # Collision detection
                            if self.game_state[f'r{current_row - 1}'][col] == self.pipe_segment:
                                self.is_dead = True
                            self.game_state[f'r{current_row - 1}'][col] = self.bird
                            self.game_state[row][col] = self.sky
                    # Move bird down
                    elif self.is_flap == False:
                        if current_row != 7:
                            # Collision detection 
                            if self.game_state[f'r{current_row + 1}'][col] == self.pipe_segment:
                                self.is_dead = True
                            self.game_state[f'r{current_row + 1}'][col] = self.bird
                            self.game_state[row][col] = self.sky
                        else:
                            self.is_dead = True
                    # Prevent multiple moves in a single frame
                    has_bird_moved = True
                    
        # Create new pipes after moving bird and old pipes
        if is_make_pipe:
            make_pipes(self.game_state)

        # Gives the bird some flap power
        if self.flap_count < self.max_flaps:
            self.flap_count += 1
        else:
            self.is_flap = False
            self.flap_count = 1

        # Check if player is dead
        is_found = False
        for row in self.game_state.keys():
            if self.bird in self.game_state[row]['c3']:
                is_found = True
        if not is_found or self.is_dead:
            self.is_dead = True
            print(f"You died.\nScore: {self.score}")
            exit()
        
        self.score += 1

    def play(self):
        os.system('cls||clear')
        self.print_state()
        time.sleep(0.5)
        self.next_frame()

if __name__ == "__main__":
    game = NonInfingingBirdPipeGame()
    while (not game.is_dead):
        game.play()
