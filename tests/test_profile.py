from pathlib import Path
from pathlib import Path
from src.profile import ProfileManager


def test_profile_record_and_leaderboard(tmp_path: Path) -> None:
    path = tmp_path / "profiles.json"
    manager = ProfileManager(path)
    manager.load()
    manager.record_score("alice", 5)
    manager.record_score("bob", 7)
    lb = manager.leaderboard()
    assert lb[0] == ("bob", 7)
    assert lb[1] == ("alice", 5)


def test_profile_export_import(tmp_path: Path) -> None:
    path = tmp_path / "profiles.json"
    manager = ProfileManager(path)
    manager.load()
    manager.record_score("alice", 10)
    export_path = tmp_path / "export.json"
    manager.export_data(export_path)

    manager2 = ProfileManager(tmp_path / "other.json")
    manager2.load()
    manager2.import_data(export_path)
    assert manager2.leaderboard() == [("alice", 10)]
