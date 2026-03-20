import random
import re

class QuestionGenerator:

    def generate_questions(self, context):

        sentences = re.split(r'(?<=[.!?]) +', context)

        topics = []

        for sentence in sentences:

            sentence = sentence.strip()

            # Skip short sentences
            if len(sentence.split()) < 8:
                continue

            # Skip headers
            if "Professor" in sentence or "University" in sentence:
                continue

            if "Page" in sentence:
                continue

            # Remove garbage words
            if any(word in sentence.lower() for word in [
                "example", "reference", "summary", "kute", "http", "www"
            ]):
                continue

            # Keep only meaningful sentences
            if not any(word in sentence.lower() for word in [
                "is", "are", "refers", "means", "defined"
            ]):
                continue

            # Clean sentence
            sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)

            # Fix broken words
            sentence = sentence.replace("featurespredictors", "features predictors")

            # Shorten sentence
            words = sentence.split()
            topic = " ".join(words[:10]).capitalize()

            topics.append(topic)

        # Remove duplicates + limit
        topics = list(set(topics))[:10]

        mcq = []
        short_answer = []
        viva = []

        for topic in topics:

            other_topics = [t for t in topics if t != topic]

            if len(other_topics) >= 3:
                distractors = random.sample(other_topics, 3)
            else:
                distractors = other_topics

            options = distractors + [topic]
            random.shuffle(options)

            mcq.append({
                "question": f"Which of the following best explains: {topic}?",
                "options": options,
                "answer": topic
            })

            short_answer.append(f"Explain: {topic}.")
            viva.append(f"What do you understand by: {topic}?")

        return mcq, short_answer, viva