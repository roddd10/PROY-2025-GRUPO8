"""Allow to use command line arguments for the camera and board numbers."""
import argparse

def create_parser(task="broadcast"):
    if task == "broadcast":
        description = "Broadcast game from a camera to Lichess."
    elif task == "calibrate":
        description = "Calibrate camera using empty board."
    elif task == "main":
        description = "Run local chess move tracking from camera."
    else:
        raise ValueError(f"Unknown task: {task}")

    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument(
        "-c", "--camera-index",
        metavar="CI",
        type=int,
        nargs="?",
        default=0,
        help="Index of the camera to be used (starts at 0).",
    )
    parser.add_argument(
        "-g", "--game-index",
        metavar="GI",
        type=int,
        nargs="?",
        default=0,
        help="Index of the initial PGN game to load (starts at 0).",
    )
    parser.add_argument(
        "-s", "--stream",
        metavar="STREAM",
        type=int,
        nargs="?",
        default=2,
        help="Stream resolution: 1 for 720p, 2 for 360p.",
    )
    
    return parser
