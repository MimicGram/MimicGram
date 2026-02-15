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

    async def execute(self, client, channel, message, discussion_group_id):
        delay = random.randint(self.MIN_DELAY, self.MAX_DELAY)

        logging.info(f"Delaying action for {delay} seconds...")

        await asyncio.sleep(delay)

        # Generate comment once
        comment = engine.generate()

        # Duplicate protection
        if memory.exists_recent(comment):
            logging.info("Duplicate comment detected. Skipping.")
            return

        try:
            await client.send_message(
                entity=discussion_group_id,
                message=comment,
                reply_to=message.id
            )
            logging.info("Comment sent successfully.")

        except Exception as e:
            logging.error(f"Failed to send comment: {e}")
            return

        # Save to memory AFTER successful send
        memory.save(comment)

        logging.info(
            f"[SAFE PIPELINE] Generated comment for message {message.id}: "
            f"{comment} in channel {channel.title}"
        )
