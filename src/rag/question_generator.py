import random
import re

class QuestionGenerator:

    def generate_questions(self, context):

        sentences = re.split(r'(?<=[.!?]) +', context)

        topics = []

        for sentence in sentences:

            sentence = sentence.strip()

            # Skip short or too long sentences
            if len(sentence.split()) < 8 or len(sentence.split()) > 25:
                continue

            # Skip headers / junk
            if any(x in sentence for x in ["Professor", "University", "Page"]):
                continue

            # Remove garbage words
            if any(word in sentence.lower() for word in [
                "example", "reference", "summary", "http", "www", "fig"
            ]):
                continue

            # ❌ REMOVE COMMAND-LIKE / CHEAT SHEET TEXT
            if any(cmd in sentence.lower() for cmd in [
                "git", "http", "www", "command", "file", "commit"
            ]):
                continue

            # Keep only meaningful sentences
            if not any(word in sentence.lower() for word in [
                " is ", " are ", " refers ", " means ", " defined "
            ]):
                continue

            # Clean sentence
            sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)

            words = sentence.split()

            # Better topic (not just first 10 random words)
            topic = " ".join(words[:6]).capitalize()

            # Avoid weird topics
            if len(topic) < 15:
                continue

            topics.append(topic)

        # Remove duplicates + ensure enough variety
        topics = list(set(topics))

        if len(topics) < 4:
            return [], [], []

        topics = topics[:10]

        mcq = []
        short_answer = []
        viva = []

        for topic in topics:

            # Better distractors (avoid very similar ones)
            other_topics = [t for t in topics if t != topic and t[:10] != topic[:10]]

            if len(other_topics) >= 3:
                distractors = random.sample(other_topics, 3)
            else:
                continue  # skip bad question

            options = distractors + [topic]
            random.shuffle(options)

            mcq.append({
                "question": f"Which concept best matches: {topic}?",
                "options": options,
                "answer": topic
            })

            short_answer.append(f"Explain: {topic}.")
            viva.append(f"What do you understand by: {topic}?")

        return mcq, short_answer, viva