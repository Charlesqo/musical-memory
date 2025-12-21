import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Tuple


@dataclass
class UserProfile:
    """A single player's stored progress and settings."""

    name: str
    high_score: int = 0
    history: List[int] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfileManager:
    """Manage multiple :class:`UserProfile` instances."""

    file_path: Path = field(
        default_factory=lambda: Path(__file__).with_name("profiles.json")
    )
    profiles: Dict[str, UserProfile] = field(default_factory=dict)

    # -- Basic persistence -------------------------------------------------
    def load(self) -> None:
        """Load profile data from :attr:`file_path`."""
        if self.file_path.exists():
            with self.file_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.profiles = {
                name: UserProfile(
                    name=name,
                    high_score=info.get("high_score", 0),
                    history=info.get("history", []),
                    settings=info.get("settings", {}),
                )
                for name, info in data.get("profiles", {}).items()
            }
        else:
            self.profiles = {}

    def save(self) -> None:
        """Persist current profiles to :attr:`file_path`."""
        data = {
            "profiles": {
                name: {
                    "high_score": p.high_score,
                    "history": p.history,
                    "settings": p.settings,
                }
                for name, p in self.profiles.items()
            }
        }
        with self.file_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    # -- Profile operations -----------------------------------------------
    def get_profile(self, name: str) -> UserProfile:
        """Return existing profile or create a new one."""
        profile = self.profiles.get(name)
        if profile is None:
            profile = UserProfile(name)
            self.profiles[name] = profile
        return profile

    def record_score(self, name: str, score: int) -> bool:
        """Record ``score`` for ``name`` and update high score.

        Returns ``True`` if ``score`` is a new high score for the player.
        """
        profile = self.get_profile(name)
        profile.history.append(score)
        new_high = False
        if score > profile.high_score:
            profile.high_score = score
            new_high = True
        self.save()
        return new_high

    def reset_profile(self, name: str) -> bool:
        """Reset ``name`` back to an empty profile.

        Returns ``True`` if a profile existed and was reset. Missing profiles
        are left untouched and return ``False`` so callers can differentiate
        between "reset" and "nothing to do" states.
        """
        if name not in self.profiles:
            return False
        self.profiles[name] = UserProfile(name)
        self.save()
        return True

    def leaderboard(self) -> List[Tuple[str, int]]:
        """Return leaderboard as list of ``(name, high_score)`` tuples."""
        return sorted(
            ((p.name, p.high_score) for p in self.profiles.values()),
            key=lambda item: item[1],
            reverse=True,
        )

    # -- Import / Export ---------------------------------------------------
    def export_data(self, path: Path) -> None:
        """Export all profile data to ``path``."""
        data = {
            "profiles": {
                name: {
                    "high_score": p.high_score,
                    "history": p.history,
                    "settings": p.settings,
                }
                for name, p in self.profiles.items()
            }
        }
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    def import_data(self, path: Path) -> None:
        """Import profile data from ``path`` and merge with existing data."""
        if not path.exists():
            return
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        for name, info in data.get("profiles", {}).items():
            profile = self.get_profile(name)
            profile.high_score = max(profile.high_score, info.get("high_score", 0))
            profile.history.extend(info.get("history", []))
            profile.settings.update(info.get("settings", {}))
        self.save()
