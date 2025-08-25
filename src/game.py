import random
import time

try:
    import numpy as np
    import simpleaudio as sa
except Exception:  # simpleaudio optional
    sa = None
    np = None

# Mapping for difficulty to available notes
DIFFICULTY_NOTES = {
    "easy": [1, 2, 3, 4],
    "medium": [1, 2, 3, 4, 5, 6],
    "hard": list(range(1, 9)),
}

# Basic frequency mapping for notes, using C major scale
NOTE_FREQUENCIES = {
    1: 261.63,
    2: 293.66,
    3: 329.63,
    4: 349.23,
    5: 392.00,
    6: 440.00,
    7: 493.88,
    8: 523.25,
}

def generate_next_note(difficulty: str) -> int:
    """Return a random note based on difficulty."""
    notes = DIFFICULTY_NOTES.get(difficulty, DIFFICULTY_NOTES["easy"])
    return random.choice(notes)

def check_sequence(expected, actual) -> bool:
    """Compare two sequences."""
    return expected == actual

def _play_tone(frequency: float, duration: float = 0.4) -> None:
    """Play a tone using simpleaudio if available."""
    if not sa or not np:
        time.sleep(duration)
        return
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    audio = (tone * (2 ** 15 - 1) / np.max(np.abs(tone))).astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()

def play_sequence(sequence, use_audio: bool = False, delay: float = 0.5) -> None:
    """Print and optionally play sequence."""
    for note in sequence:
        print(note)
        if use_audio:
            freq = NOTE_FREQUENCIES.get(note, 440)
            _play_tone(freq)
        else:
            time.sleep(delay)
