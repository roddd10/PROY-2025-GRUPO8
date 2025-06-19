"""Upload the pairing info to Lichess before the round starts."""

import os

from broadcast_info import BroadcastInfo
broadcast_info = BroadcastInfo()
broadcast_id = broadcast_info.broadcast_id

# Load the games metadata from a single PGN file.
with open("initial_games.pgn") as f:
    pgn_games = f.read().split("\n\n\n")
