class QuizEngine:
    def start_quiz(self, mcq_questions):

        score = 0
        total = len(mcq_questions)

        for i, q in enumerate(mcq_questions):

            print(f"\nQuestion {i+1}: {q['question']}")

            print("A)", q["options"][0])
            print("B)", q["options"][1])
            print("C)", q["options"][2])
            print("D)", q["options"][3])

            answer = input("Your answer (A/B/C/D): ").strip().upper()

            correct_option = q["options"].index(q["answer"])
            correct_letter = ["A", "B", "C", "D"][correct_option]

            if answer == correct_letter:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! Correct answer: {correct_letter}")

        print("\nQuiz Completed!")
        print(f"Your Score: {score}/{total}")