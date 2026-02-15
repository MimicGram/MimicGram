"""
MimicGram - Decision Engine
Stateful decision logic (No sending)
"""

import random
from storage.db import get_connection


class DecisionEngine:

    def decide(self, channel_id: int) -> str:
        state = self._get_state(channel_id)

        if state is None:
            decision = "SKIP" if random.random() < 0.7 else "ACT"
            self._save_state(channel_id, decision, 1 if decision == "SKIP" else 0)
            return decision

        last_action, skip_count = state

        if last_action == "ACT":
            decision = "SKIP"

        elif skip_count >= 2:
            decision = "ACT"

        else:
            decision = "ACT" if random.random() < 0.3 else "SKIP"

        new_skip_count = skip_count + 1 if decision == "SKIP" else 0
        self._save_state(channel_id, decision, new_skip_count)

        return decision

    def _get_state(self, channel_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT last_action, skip_count FROM channel_state WHERE channel_id=?",
            (channel_id,)
        )

        row = cursor.fetchone()
        conn.close()
        return row

    def _save_state(self, channel_id, decision, skip_count):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO channel_state (channel_id, last_action, skip_count)
            VALUES (?, ?, ?)
            ON CONFLICT(channel_id)
            DO UPDATE SET
                last_action=excluded.last_action,
                skip_count=excluded.skip_count,
                last_updated=CURRENT_TIMESTAMP
        """, (channel_id, decision, skip_count))

        conn.commit()
        conn.close()
