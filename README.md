# Musical Memory

Musical Memory 是一个简单的记忆游戏：玩家需要记住并重复播放的音符序列。

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

运行入口位于 `src.main`，建议使用模块方式启动：

```bash
python -m src.main --levels 5 --difficulty easy
```

常用参数：

- `--levels`：关卡数量（默认 `5`）
- `--difficulty`：难度 `easy|medium|hard`
- `--audio`：若系统支持，将播放真实音调
- `--mode`：交互模式 `cli|gui|web`
- `--config`：可选的 JSON 配置文件

## Extending

- 在 `src/game.py` 中修改 `DIFFICULTY_NOTES` 或 `NOTES` 以定制音符池。
- 在 `src/cli.py` 中完善 `_run_gui` 或 `_run_web`，或添加新的模式以扩展交互方式。
- 通过扩展 `src/score.py` 中的 `ScoreManager`，可替换或接入不同的分数存储方案。

更多开发信息请参阅 [`docs/developer-guide.md`](docs/developer-guide.md)。

