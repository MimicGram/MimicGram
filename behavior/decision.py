"""
MimicGram - Decision Engine
Stateful decision logic (No sending)
"""

import random
from collections import defaultdict


class DecisionEngine:
    def __init__(self):
        # channel_id -> state
        self.channel_state = defaultdict(lambda: {
            "last_action": None,  # "ACT" or "SKIP"
            "skip_count": 0
        })

    def decide(self, channel_id: int) -> str:
        state = self.channel_state[channel_id]

        # First time seeing this channel
        if state["last_action"] is None:
            decision = "SKIP" if random.random() < 0.7 else "ACT"
            self._update_state(channel_id, decision)
            return decision

        # If last was ACT -> force SKIP
        if state["last_action"] == "ACT":
            decision = "SKIP"
            self._update_state(channel_id, decision)
            return decision

        # If skipped twice -> force ACT
        if state["skip_count"] >= 2:
            decision = "ACT"
            self._update_state(channel_id, decision)
            return decision

        # Otherwise random small chance to ACT
        decision = "ACT" if random.random() < 0.3 else "SKIP"
        self._update_state(channel_id, decision)
        return decision

    def _update_state(self, channel_id, decision):
        state = self.channel_state[channel_id]

        state["last_action"] = decision

        if decision == "SKIP":
            state["skip_count"] += 1
        else:
            state["skip_count"] = 0
