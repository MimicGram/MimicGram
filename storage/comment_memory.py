"""
MimicGram - Comment Memory Storage
Prevent duplicate comments
"""

from storage.postgres import get_connection
from datetime import datetime, timedelta


class CommentMemory:

    LIMIT = 50

    def save(self, content: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO comment_memory (content) VALUES (%s)",
                    (content,)
                )

                # Keep only latest LIMIT entries
                cur.execute(f"""
                    DELETE FROM comment_memory
                    WHERE id NOT IN (
                        SELECT id FROM comment_memory
                        ORDER BY created_at DESC
                        LIMIT {self.LIMIT}
                    )
                """)

    def exists_recent(self, content: str, hours: int = 24) -> bool:
        time_threshold = datetime.utcnow() - timedelta(hours=hours)

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 1 FROM comment_memory
                    WHERE content=%s
                    AND created_at >= %s
                    LIMIT 1
                """, (content, time_threshold))

                return cur.fetchone() is not None
