from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Iterable, Sequence, List, Union, Optional

# ==== 可选的声音播放依赖（没有就静默睡眠模拟时长）====
try:
    import numpy as np
    import simpleaudio as sa
except Exception:
    np = None
    sa = None

# ---- 类型别名：既可用数字音阶，也可用字母音名 ----
Note = Union[int, str]

# ---- 难度 -> 可用“数字音阶”池 ----
DIFFICULTY_NOTES = {
    "easy": [1, 2, 3, 4],
    "medium": [1, 2, 3, 4, 5, 6],
    "hard": list(range(1, 9)),
}

# ---- 默认“字母音名”池（如需字母序列玩法）----
NOTES: Sequence[str] = ("C", "D", "E", "F", "G", "A", "B")

# ---- 频率表：数字音阶 1~8 对应 C 大调（C4..C5）----
NOTE_FREQUENCIES_NUM = {
    1: 261.63, 2: 293.66, 3: 329.63, 4: 349.23,
    5: 392.00, 6: 440.00, 7: 493.88, 8: 523.25,
}

# ---- 频率表：字母音名（C4..B4）----
NOTE_FREQUENCIES_LETTER = {
    "C": 261.63, "D": 293.66, "E": 329.63, "F": 349.23,
    "G": 392.00, "A": 440.00, "B": 493.88,
}

# ================== 核心工具函数 ==================

def _freq_of(note: Note) -> float:
    """把任意 Note（int/str）映射到频率，未知则回退 440Hz。"""
    if isinstance(note, int):
        return NOTE_FREQUENCIES_NUM.get(note, 440.0)
    if isinstance(note, str):
        return NOTE_FREQUENCIES_LETTER.get(note.upper(), 440.0)
    return 440.0

def _play_tone(frequency: float, duration: float = 0.4) -> None:
    """用 simpleaudio 播放；若不可用，睡一会儿模拟时长。"""
    if not sa or not np:
        time.sleep(duration)
        return
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * frequency * t)
    audio = (tone * (2**15 - 1) / np.max(np.abs(tone))).astype(np.int16)
    sa.play_buffer(audio, 1, 2, sample_rate).wait_done()

def play_sequence(sequence: Sequence[Note], use_audio: bool = False, delay: float = 0.5) -> None:
    """依次打印并（可选）播放序列。"""
    for note in sequence:
        print(note)
        if use_audio:
            _play_tone(_freq_of(note))
        else:
            time.sleep(delay)

def generate_next_note(difficulty: str = "easy", notes: Optional[Sequence[Note]] = None) -> Note:
    """随机生成下一个音符。优先使用自定义 notes；否则按难度用数字音阶池。"""
    pool: Sequence[Note] = notes if notes is not None else DIFFICULTY_NOTES.get(difficulty, DIFFICULTY_NOTES["easy"])
    return random.choice(list(pool))

def generate_sequence(length: int, notes: Sequence[Note] = NOTES) -> List[Note]:
    """生成固定长度的随机序列（默认字母音名池）。"""
    if length < 0:
        raise ValueError("length must be non-negative")
    pool = list(notes)
    return [random.choice(pool) for _ in range(length)]

def sequence_length(level: int, base_length: int = 3, step: int = 1) -> int:
    """关卡长度增长规则：base + (level-1)*step。"""
    if level < 1:
        raise ValueError("level must be at least 1")
    return base_length + (level - 1) * step

def generate_level_sequence(level: int, base_length: int = 3, step: int = 1, notes: Sequence[Note] = NOTES) -> List[Note]:
    """按关卡生成随机序列（默认字母音名池，可换成数字池）。"""
    return generate_sequence(sequence_length(level, base_length, step), notes)

def check_sequence(expected: Iterable[Note], actual: Iterable[Note]) -> bool:
    """比较两个序列是否完全一致。"""
    return list(expected) == list(actual)

# ================== 分数保存（可选自动降级） ==================

def end_game(score: int, file_path: Optional[Path] = None) -> str:
    """
    更新最高分并返回提示：
    - 若存在外部 ScoreManager（score_manager.ScoreManager 或 .score.ScoreManager），优先使用；
    - 否则自动降级为本地文本文件 high_score.txt。
    """
    manager = None
    try:
        from score_manager import ScoreManager as _SM  # type: ignore
        manager = _SM(file_path) if file_path else _SM()
    except Exception:
        try:
            from .score import ScoreManager as _SM  # type: ignore
            manager = _SM(file_path) if file_path else _SM()
        except Exception:
            manager = None

    if manager is not None:
        try:
            manager.load()
            is_new = manager.record(score)
            msg = (
                f"New high score: {manager.high_score}!" if is_new
                else f"Your score: {score}. High score: {manager.high_score}."
            )
            print(msg)
            return msg
        except Exception:
            # 外部管理器失败则退回简易文件法
            pass

    path = file_path or Path("high_score.txt")
    prev = 0
    if path.exists():
        try:
            prev = int(path.read_text().strip() or "0")
        except Exception:
            prev = 0
    new_high = max(prev, score)
    path.write_text(str(new_high))
    msg = ("New high score: " + str(new_high) + "!" if score > prev
           else f"Your score: {score}. High score: {new_high}.")
    print(msg)
    return msg

if __name__ == "__main__":
    # 迷你自检
    seq = generate_level_sequence(1)          # 默认字母音名池
    play_sequence(seq, use_audio=False, delay=0.2)
    print("check:", check_sequence(seq, seq))
    end_game(random.randint(0, 10))
