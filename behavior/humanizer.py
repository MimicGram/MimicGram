"""
MimicGram - Human Behavior Layer
Advanced filtering before action
"""

import random
from datetime import datetime, timedelta
from storage.postgres import get_connection


class Humanizer:

    DAILY_LIMIT = 100
    MIN_COOLDOWN_MIN = 20
    MAX_COOLDOWN_MIN = 60

    def allow_action(self, channel_id: int) -> bool:
        return True


    def _check_daily_limit(self):
        today = datetime.utcnow().date()

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM channel_state
                    WHERE last_action='ACT'
                    AND DATE(last_updated)=%s
                """, (today,))
                count = cur.fetchone()[0]

        return count < self.DAILY_LIMIT

    def _check_channel_cooldown(self, channel_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT last_updated FROM channel_state
                    WHERE channel_id=%s
                    AND last_action='ACT'
                """, (channel_id,))
                row = cur.fetchone()

        if not row:
            return True

        last_time = row[0]
        cooldown = timedelta(
            minutes=random.randint(self.MIN_COOLDOWN_MIN, self.MAX_COOLDOWN_MIN)
        )

        return datetime.utcnow() - last_time > cooldown

    def _check_time_window(self):
        return True


        return False
