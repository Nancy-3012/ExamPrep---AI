import os
import json
import re

class QuestionGenerator:

    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set. Get a free key at https://console.groq.com")
        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def _call_llm(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content.strip()

    def _parse_json(self, raw: str):
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("```").strip()
        return json.loads(raw)

    def generate_mcq(self, context: str, num: int = 5) -> list:
        prompt = f"""You are an expert exam question generator.

Based ONLY on the context below, generate exactly {num} multiple choice questions.

Context:
\"\"\"
{context}
\"\"\"

Rules:
- Questions must be directly based on the context above.
- Each question must have exactly 4 options (A, B, C, D).
- Only one option must be correct.
- Distractors must be plausible but wrong.
- Do NOT add any explanation outside the JSON.

Return ONLY a valid JSON array in this exact format:
[
  {{
    "question": "What is ...?",
    "options": ["Correct answer", "Wrong option 1", "Wrong option 2", "Wrong option 3"],
    "answer": "Correct answer"
  }}
]
"""
        raw = self._call_llm(prompt)
        return self._parse_json(raw)

    def generate_short(self, context: str, num: int = 5) -> list:
        prompt = f"""You are an expert exam question generator.

Based ONLY on the context below, generate exactly {num} short answer questions (2-3 sentence answers expected).

Context:
\"\"\"
{context}
\"\"\"

Rules:
- Questions must be directly from the context.
- They should test understanding, not just recall.
- Do NOT add any explanation outside the JSON.

Return ONLY a valid JSON array of question strings like:
["Question 1?", "Question 2?", ...]
"""
        raw = self._call_llm(prompt)
        return self._parse_json(raw)

    def generate_viva(self, context: str, num: int = 5) -> list:
        prompt = f"""You are an expert exam question generator.

Based ONLY on the context below, generate exactly {num} deep conceptual viva questions (detailed answers expected).

Context:
\"\"\"
{context}
\"\"\"

Rules:
- Questions should require explanation, analysis, or comparison.
- Avoid simple yes/no or one-word answers.
- Do NOT add any explanation outside the JSON.

Return ONLY a valid JSON array of question strings like:
["Question 1?", "Question 2?", ...]
"""
        raw = self._call_llm(prompt)
        return self._parse_json(raw)

    def generate_questions(self, context: str, num: int = 5):
        mcq   = self.generate_mcq(context, num)
        short = self.generate_short(context, num)
        viva  = self.generate_viva(context, num)
        return mcq, short, viva

    def chat_with_pdf(self, question: str, context: str) -> str:
        prompt = f"""You are a helpful study assistant.
Answer the student's question based ONLY on the context provided below.
If the answer is not in the context, say "I couldn't find this in your document."

Context:
\"\"\"
{context}
\"\"\"

Student's Question: {question}

Give a clear, concise answer in 3-5 sentences.
"""
        return self._call_llm(prompt)

    def evaluate_answer(self, question: str, student_answer: str, context: str) -> dict:
        prompt = f"""You are a strict but fair exam evaluator.

A student has answered the following question. Evaluate their answer based on the context provided.

Context from document:
\"\"\"
{context}
\"\"\"

Question: {question}

Student's Answer: {student_answer}

Evaluate and return ONLY a valid JSON object like this:
{{
    "score": 7,
    "out_of": 10,
    "feedback": "Your answer is correct but missing details about...",
    "correct_answer": "The ideal answer would be..."
}}
"""
        raw = self._call_llm(prompt)
        return self._parse_json(raw)

    def generate_flashcards(self, context: str, num: int = 10) -> list:
        prompt = f"""You are an expert study material creator.

Based ONLY on the context below, generate exactly {num} flashcards.

Context:
\"\"\"
{context}
\"\"\"

Rules:
- Front of card: A key term, concept, or question
- Back of card: A clear, concise explanation or answer (2-3 sentences max)
- Cards must be directly based on the context
- Do NOT add any explanation outside the JSON

Return ONLY a valid JSON array like this:
[
  {{
    "front": "What is Bagging?",
    "back": "Bagging (Bootstrap Aggregating) is an ensemble technique that trains multiple models on random subsets of training data and combines their predictions to reduce variance."
  }}
]
"""
        raw = self._call_llm(prompt)
        return self._parse_json(raw)