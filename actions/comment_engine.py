"""
MimicGram - Smart Comment Generator
Anti-pattern comment generation
"""

import random

class CommentEngine:

    BASE_REACTIONS = [
        "🔥",
        "👏",
        "😍",
        "💪",
        "⚡️"
    ]

    SHORT_TEXTS = [
        "Amazing performance",
        "Well played",
        "Respect",
        "Top level",
        "Incredible"
    ]

    def generate(self):

        structure_type = random.choice(["emoji", "short", "mixed"])

        if structure_type == "emoji":
            return random.choice(self.BASE_REACTIONS)

        if structure_type == "short":
            return random.choice(self.SHORT_TEXTS)

        if structure_type == "mixed":
            return f"{random.choice(self.BASE_REACTIONS)} {random.choice(self.SHORT_TEXTS)}"
