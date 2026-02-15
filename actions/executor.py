"""
MimicGram - Safe Action Executor
Controlled delayed execution
"""

import asyncio
import random
import logging
from actions.comment_engine import CommentEngine
from storage.comment_memory import CommentMemory

engine = CommentEngine()
memory = CommentMemory()


class ActionExecutor:

    MIN_DELAY = 45
    MAX_DELAY = 180

    async def execute(self, client, channel, message):
        delay = random.randint(self.MIN_DELAY, self.MAX_DELAY)

        logging.info(f"Delaying action for {delay} seconds...")

        await asyncio.sleep(delay)

        # Generate comment ONCE
        comment = engine.generate()

        # Duplicate protection
        if memory.exists_recent(comment):
            logging.info("Duplicate comment detected. Skipping.")
            return

        # Save to memory
        memory.save(comment)

        logging.info(
            f"[SAFE PIPELINE] Generated comment for message {message.id}: {comment} "
            f"in channel {channel.title}"
        )

        # (فعلاً فقط لاگ میزنیم — اگر بعداً خواستی ارسال واقعی اضافه می‌کنیم)
