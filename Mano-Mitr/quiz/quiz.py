from flask import Flask, render_template, request

app = Flask(__name__)

# Define the quiz questions, options, and scores for each type of counselor
quiz_data = [
    {
        "question": "How often do you feel overwhelmed by your responsibilities?",
        "options": [
            {"text": "Rarely", "scores": {"Family Counselor": 1, "Academic Counselor": 2}},
            {"text": "Sometimes", "scores": {"Family Counselor": 2, "Academic Counselor": 3, "Financial Counselor": 2}},
            {"text": "Often", "scores": {"Family Counselor": 3, "Academic Counselor": 4, "Financial Counselor": 3}},
            {"text": "Always", "scores": {"Family Counselor": 4, "Academic Counselor": 5, "Financial Counselor": 4}},
        ]
    },
    {
        "question": "Have you experienced any recent conflicts with your family?",
        "options": [
            {"text": "No", "scores": {"Family Counselor": 1}},
            {"text": "Minor conflicts", "scores": {"Family Counselor": 2}},
            {"text": "Major conflicts", "scores": {"Family Counselor": 4}},
        ]
    },
    {
        "question": "Do you feel anxious or stressed due to financial issues?",
        "options": [
            {"text": "No", "scores": {"Financial Counselor": 1}},
            {"text": "Sometimes", "scores": {"Financial Counselor": 2}},
            {"text": "Frequently", "scores": {"Financial Counselor": 3}},
            {"text": "Always", "scores": {"Financial Counselor": 4}},
        ]
    },
    {
        "question": "Have you been bullied or harassed recently?",
        "options": [
            {"text": "No", "scores": {"Bullying Counselor": 1}},
            {"text": "Yes", "scores": {"Bullying Counselor": 4}},
        ]
    },
    {
        "question": "Do you struggle with academic pressure or challenges?",
        "options": [
            {"text": "No", "scores": {"Academic Counselor": 1}},
            {"text": "Sometimes", "scores": {"Academic Counselor": 2}},
            {"text": "Often", "scores": {"Academic Counselor": 3}},
            {"text": "Always", "scores": {"Academic Counselor": 4}},
        ]
    },
    {
        "question": "Have you been a victim of sexual abuse?",
        "options": [
            {"text": "No", "scores": {"Sexual Abuse Counselor": 1}},
            {"text": "Yes", "scores": {"Sexual Abuse Counselor": 5}},
        ]
    },
    {
        "question": "Do you face challenges in your current relationship?",
        "options": [
            {"text": "No", "scores": {"Relationship Counselor": 1}},
            {"text": "Yes", "scores": {"Relationship Counselor": 4}},
        ]
    },
    {
        "question": "Do you struggle with parenting challenges?",
        "options": [
            {"text": "No", "scores": {"Parenting Counselor": 1}},
            {"text": "Yes", "scores": {"Parenting Counselor": 4}},
        ]
    }
]

# Complex backend logic to recommend a counselor
def recommend_counselor(answers):
    counselor_scores = {
        "Bullying Counselor": 0,
        "Family Counselor": 0,
        "Academic Counselor": 0,
        "Sexual Abuse Counselor": 0,
        "Relationship Counselor": 0,
        "Financial Counselor": 0,
        "Parenting Counselor": 0
    }

    for answer in answers:
        for counselor, score in answer.items():
            counselor_scores[counselor] += score

    # Recommend the counselor with the highest score
    recommended_counselor = max(counselor_scores, key=counselor_scores.get)
    return recommended_counselor

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        answers = []
        for i, question_data in enumerate(quiz_data):
            selected_option = request.form.get(f'question_{i}')
            for option in question_data['options']:
                if option['text'] == selected_option:
                    answers.append(option['scores'])

        recommended_counselor = recommend_counselor(answers)
        return render_template('result.html', recommended_counselor=recommended_counselor)

    # Passing enumerate to the template
    return render_template('quiz.html', quiz_data=quiz_data, enumerate=enumerate)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
