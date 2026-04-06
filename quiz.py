import random

with open(r"c:\Vscode\Code1\Quiz reader\questions.txt", encoding="utf-8") as f:
    content = f.read()
blocks = content.split("\n\n")

quiz_questions = []
for block in blocks:
    line = block.split("\n")
    question_data = {
        "question": line[0],
        "options": line[1:5],
        "answer": line[5]
    }
    quiz_questions.append(question_data)

#score
score = 0
while True:
    #shuffle the questions    
    random.shuffle(quiz_questions)
    for i, q in enumerate(quiz_questions, 1):   
        print(f"Question {i}:", q["question"])
        print("Options:", "   ".join(q["options"]))
        
        valid_answer = ["A", "B", "C", "D"]
        while True:
            user_answer = input("Your answer (A/B/C/D): ").strip().upper()
            if user_answer in valid_answer:
                break
            else:
                print("Invalid input. Please enter A, B, C, or D.")
        
        if user_answer.strip().lower() == q["answer"].strip().lower():
                print("Correct!✅")
                score += 1
                
        else:
            print("Incorrect❌. The correct answer is:", q["answer"])
    print("Quiz completed! Your score:", (score, "/", len(quiz_questions)))
    print("Do you want to retake the quiz? (yes/no)")
    retry = input().strip().lower()
    if retry == "yes":
        score = 0
        continue
    elif retry == "no":
        print("Thank you for playing! Good Luck! Goodbye!")
        break
    else:
        print("Invalid input. Exiting the quiz.")
        break
