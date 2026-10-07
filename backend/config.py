"""Shared backend configuration and semantic state labels."""

from pathlib import Path

STATE_LABELS = ("Low Traffic", "Medium Traffic", "High Traffic")
NUM_STATES = len(STATE_LABELS)
MIN_OBSERVATIONS = 6
DEFAULT_WINDOW_SIZE = 24
FUTURE_STEPS = 3
MAX_TRAINING_ITERATIONS = 100
TRAINING_TOLERANCE = 1e-4
VARIANCE_FLOOR = 1e-3
DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "pems08.npz"