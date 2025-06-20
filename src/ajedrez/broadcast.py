import datetime
import time


class Broadcast:
    def __init__(self, board_basics, token_unused, broadcast_id_unused, pgn_games, roi_mask, game_id, time_control="90+30"):
        self.board = board_basics
        self.roi_mask = roi_mask
        self.all_games = pgn_games
        self.game_id = game_id
        self.pgn_game = pgn_games[game_id] + "\n\n"

        init_minutes = int(time_control.split("+")[0])
        self.clock_times = [init_minutes * 60, init_minutes * 60]
        self.increment = int(time_control.split("+")[1])
        self.num_half_moves = 0
        self.last_move_time = time.time()
        self.cur_move_time = None

        self.executed_moves = []

    @property
    def pgn_list(self):
        pgn_list = [str(game) for game in self.all_games]
        pgn_list[self.game_id] = self.pgn_game + "*"
        return pgn_list

    def move(self, move):
        self.num_half_moves += 1
        if self.num_half_moves % 2 == 1:
            self.pgn_game += f"\n{(self.num_half_moves + 1) // 2}. "
        self.pgn_game += move + self.get_clock_update() + " "

        with open(f"./ongoing_games/game{self.game_id}.pgn", "w") as f:
            f.write(self.pgn_game)

        self.executed_moves.append(move)
        print(f"Move played: {move}")

    def get_clock_update(self):
        self.cur_move_time = time.time()
        elapsed_time = self.cur_move_time - self.last_move_time
        self.last_move_time = self.cur_move_time

        which_clock = (self.num_half_moves - 1) % 2
        self.clock_times[which_clock] -= elapsed_time
        self.clock_times[which_clock] += self.increment

        clock_str = str(datetime.timedelta(seconds=int(self.clock_times[which_clock]))).split(".")[0]
        return f" {{[%clk {clock_str}]}}"

    def correct_moves(self):
        """Allow external tool to edit PGN. Reloads it from file."""
        try:
            with open(f"./ongoing_games/game{self.game_id}.pgn", "r") as f:
                self.pgn_game = f.read()
            print("PGN corrected.")
        except FileNotFoundError:
            print("PGN file not found for correction.")

    def correct_clocks(self, response):
        try:
            white_time, black_time = response.split(",")
            white_time = self._parse_time(white_time.strip())
            black_time = self._parse_time(black_time.strip())
            self.clock_times = [white_time, black_time]
            print("Clock times updated.")
        except Exception as e:
            print("Error updating clock times:", e)

    def _parse_time(self, time_str):
        parts = list(map(int, time_str.split(":")))
        if len(parts) == 3:
            h, m, s = parts
        elif len(parts) == 2:
            h = 0
            m, s = parts
        elif len(parts) == 1:
            h = 0
            m = 0
            s = parts[0]
        else:
            raise ValueError("Invalid time format.")
        return h * 3600 + m * 60 + s

    def is_light_change(self, frame):
        # Placeholder: implement your light change detection logic here
        return False

    def initialize_hog(self, frame):
        # Placeholder: set up for piece detection via HOG
        pass

    def register_move(self, fgmask, previous_frame, last_frame):
        # Placeholder: implement move detection logic here
        return False

    def is_game_over(self):
        # Placeholder: integrate actual game-over detection if needed
        return False
