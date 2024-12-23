from flask import Flask, render_template, url_for, render_template_string
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
import webbrowser
import time

# Initialize Flask app
app = Flask(__name__)
global depressed_percentage, not_depressed_percentage
depressed_percentage = 0
not_depressed_percentage = 0
global counselorType
counselorType=""
# Route to render landing.html
@app.route("/")
def landing():
    return render_template("index.html")







@app.route("/quiz1")
def quiz1():
    quiz_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Result</title>
        <style>
            .start-btn-container {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: "Roboto", sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                background: #f0f8ff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .start-btn-container h2 {
                font-size: 36px;
                margin: 0 0 16px 0;
                color: #003366;
            }
            .start-btn-container p {
                font-size: 18px;
                color: #001f3f;
                margin: 0 0 24px 0;
            }
            .start-btn-container .start-btn {
                background: #003366;
                color: #f0f8ff;
                padding: 12px 32px;
                border-radius: 8px;
                border: none;
                font-size: 20px;
                cursor: pointer;
                text-transform: uppercase;
                font-weight: bold;
                transition: background 0.3s, box-shadow 0.3s;
            }
            .start-btn-container .start-btn:hover {
                background: #002244;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            .start-btn-container .start-btn a {
                color: #f0f8ff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="start-btn-container">
            <h2>QUIZ</h2>
            <p>Take this quiz before the final step of your screening process.</p>
            <button class="start-btn">
                <a href="{{ url_for('quiz2') }}">Start Quiz</a>
            </button>
        </div>
    </body>
    </html>
    '''
    return render_template_string(quiz_html)

@app.route('/quiz2')
def quiz2():
    quiz2_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Mental Health Quiz</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f0f0f0;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .quiz-container {
                background-color: navy;
                padding: 30px;
                border-radius: 15px;
                width: 100%;
                max-width: 600px;
                box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
                color: #fff;
            }
            .question {
                font-size: 22px;
                margin-bottom: 25px;
            }
            .options {
                margin-bottom: 25px;
            }
            .option {
                padding: 12px;
                margin-bottom: 15px;
                background-color: #ffffff;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                color: #333;
            }
            .option:hover {
                background-color: #f5f5f5;
            }
            .option.selected {
                background-color: #304ffe;
                color: #ffffff;
            }
            .next-btn {
                padding: 12px 24px;
                background-color: #304ffe;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                color: #ffffff;
                font-size: 18px;
                transition: background-color 0.3s ease;
            }
            .next-btn:hover {
                background-color: #1a237e;
            }
            .next-btn:disabled {
                background-color: #ccc;
                cursor: not-allowed;
                color: #777;
            }
            .quiz-result {
                display: none;
                flex-direction: column;
                align-items: center;
                text-align: center;
                color: #1a237e;
                padding: 30px;
                background-color: #fff;
                border-radius: 15px;
                box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
                max-width: 600px;
            }
            .quiz-result h2 {
                margin-bottom: 20px;
                font-size: 24px;
                color: #2f268d;
            }
            .quiz-result p {
                font-size: 18px;
                margin-bottom: 10px;
            }
            .quiz-result a {
                color: #304ffe;
                text-decoration: none;
                font-weight: bold;
            }
            .quiz-result a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="quiz-container">
            <div class="question"></div>
            <div class="options"></div>
            <button class="next-btn" disabled>Next</button>
        </div>
        <div class="quiz-result"></div>

        <script>
            const quizData = [
                {
                    question: "How long have you been experiencing feelings of sadness, hopelessness, or a lack of interest in activities you once enjoyed?",
                    options: ["Less than 6 months", "6 months to 1 year", "1-3 years", "Over 3 years"],
                },
                {
                    question: "Have you ever been diagnosed with depression or any other mental health condition?",
                    options: ["Yes", "No"],
                },
                {
                    question: "What types of treatment or support have you tried or are currently using to manage your mental health?",
                    options: ["Therapy", "Medication", "Support Groups", "Other"],
                },
                {
                    question: "Which of the following symptoms have you experienced over the last two weeks? (Select all that apply)",
                    options: ["Persistent sadness or low mood", "Loss of interest in activities", "Changes in appetite or weight", "Sleep disturbances", "Fatigue or lack of energy", "Difficulty concentrating", "Feelings of worthlessness or guilt", "Thoughts of self-harm or suicide"],
                },
                {
                    question: "Over the last two weeks, how much have these symptoms affected your daily life and activities?",
                    options: ["Not at all", "Slightly", "Moderately", "Severely"],
                },
                {
                    question: "Which of the following triggers or stressors do you feel contribute most to your mental health? (Select all that apply)",
                    options: ["Work related issues", "Relationship issues", "Financial Problems", "Health issues", "Past trauma"],
                },
                {
                    question: "Which of the following methods do you find most effective in managing your mental well-being? (Select all that apply)",
                    options: ["Self-care (e.g. exercise, hobbies)", "Talking to friends or family", "Professional therapy", "Medication", "Mindfulness or meditation"],
                },
                {
                    question: "How effective do you find the following strategies in managing your mental well-being? (Select all that apply)",
                    options: ["Very effective", "Somewhat effective", "Not effective", "I don't use any strategies"],
                },
                {
                    question: "How effective do you find talking to friends or family in improving your mood?",
                    options: ["Very effective", "Somewhat effective", "Not effective", "I don't use any strategies"],
                },
                {
                    question: "How often have you experienced trouble falling asleep, staying asleep, or sleeping too much?",
                    options: ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                },
                {
                    question: "Over the last two weeks, how often have you felt tired or had little energy?",
                    options: ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                },
                {
                    question: "Over the last two weeks, how often have you felt bad about yourself or that you are a failure?",
                    options: ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                },
            ];

            const counselors = [
                "Cognitive Behavioral Therapist (CBT)",
                "Psychodynamic Counselor",
                "Humanistic Therapist",
                "Mindfulness-Based Counselor",
                "Family Therapist",
                "Art Therapist",
                "Trauma-Informed Counselor"
            ];

            const questionElement = document.querySelector('.question');
            const optionsElement = document.querySelector('.options');
            const nextButton = document.querySelector('.next-btn');
            const resultElement = document.querySelector('.quiz-result');
            let currentQuestionIndex = 0;
            let selectedOptions = [];

            function displayQuestion() {
                const currentQuestion = quizData[currentQuestionIndex];
                questionElement.textContent = currentQuestion.question;
                optionsElement.innerHTML = '';
                currentQuestion.options.forEach((option, index) => {
                    const optionElement = document.createElement('div');
                    optionElement.textContent = option;
                    optionElement.className = 'option';
                    optionElement.addEventListener('click', () => selectOption(optionElement, option));
                    optionsElement.appendChild(optionElement);
                });
                nextButton.disabled = true;
            }

            function selectOption(optionElement, option) {
                const previouslySelected = optionsElement.querySelector('.option.selected');
                if (previouslySelected) {
                    previouslySelected.classList.remove('selected');
                }
                optionElement.classList.add('selected');
                nextButton.disabled = false;
                selectedOptions = [option];
            }

            function handleNext() {
                if (currentQuestionIndex < quizData.length - 1) {
                    currentQuestionIndex++;
                    displayQuestion();
                } else {
                    showResult();
                }
            }

            function showResult() {
                document.querySelector('.quiz-container').style.display = 'none';
                resultElement.style.display = 'flex';

                const randomCounselor = counselors[Math.floor(Math.random() * counselors.length)];

                resultElement.innerHTML = `
                    <h2>Quiz Completed!</h2>
                    <p>Thank you for completing the quiz. Based on your responses, we recommend seeing a <strong>${randomCounselor}</strong>.</p>
                    <a href="{{ url_for('index') }}">Start Screening</a>
                `;
            }

            nextButton.addEventListener('click', handleNext);

            displayQuestion();
        </script>
    </body>
    </html>
    '''
    return render_template_string(quiz2_html)



@app.route("/index")
def index():
    return render_template("index.html")

# Route for start_detection
@app.route("/start_detection")
def start_detection():
    face_classifier = cv2.CascadeClassifier(r"C:\Users\Sankrishna Goyal\PycharmProjects\Mano-Mitr\Emotion_Detection_CNN-main\haarcascade_frontalface_default.xml")
    classifier = load_model(r"C:\Users\Sankrishna Goyal\PycharmProjects\Mano-Mitr\Emotion_Detection_CNN-main\model.h5")
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    cap = cv2.VideoCapture(0)

    depression_count = 0
    frame_count = 0

    start_time = time.time()
    while time.time() - start_time < 30:  # Capture frames for 30 seconds
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                if prediction.argmax() in [3, 4, 6]:  # Happy, Neutral, Surprise
                    label = "Not Depressed"
                else:
                    label = "Depressed"
                    depression_count += 1

                label_position = (x, y)

        cv2.imshow('Emotion Detector', frame)

        # Check for 'q' key press to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Calculate percentages
    if frame_count > 0:  # Avoid division by zero
        depressed_percentage = (depression_count / frame_count) * 100
    else:
        depressed_percentage = 0
    not_depressed_percentage = 100 - depressed_percentage

    if depression_count > 10:  # Arbitrary threshold for depression count
        result = "You may be depressed."
        result_color = "red"
    else:
        result = "You may not depressed."
        result_color = "green"

    # Render result HTML directly without writing to a file
    result_html_content = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Embrace Well</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='result.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Audiowide:wght@400&amp;display=swap" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

        body {{
            font-family: 'Poppins', sans-serif;
            background-color: rgba(20, 22, 46, 1);
            margin: 0;
            padding: 0;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            background-color: rgba(243, 243, 252, 1);
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            position: relative;
        }}

        h1 {{
    color: rgba(22, 120, 242, 1);
    font-weight: 600;
    font-size: 4rem;
    margin-bottom: 30px;
    text-align: left;
    position: relative;
    padding-left: 120px; /* Adjust the value as needed */
}}


    .embrace-image1{{
        position: absolute;
    top: 280px; /* Adjust top positioning as needed */
    right: 40px;
    ali
    transform: translate(-50%, -50%);
    width: 50%; /* Adjust size relative to h1 */
    height: auto;
        
    }}
        .embrace-image {{
    position: absolute;
    top: 45px; /* Adjust top positioning as needed */
    left: 40px;
    transform: translate(-50%, -50%);
    width: 5%; /* Adjust size relative to h1 */
    height: auto;

        }}

        .result {{
            margin-top: 30px;
            color: {result_color};
            font-weight: 500;
            font-size: 1.6rem;
            text-align: center;
        }}

        .progress-container {{
            width: 70%;
            margin: 30px auto;
            background-color: #ddd;
            border-radius: 20px;
            overflow: hidden;
        }}

       .progress-bar {{
    width: {depressed_percentage}%;
    height: 30px;
    background-color: red; /* Set the progress bar fill color to red */
    text-align: center;
    color: white;
    line-height: 30px;
    transition: width 0.5s;
    border-radius: 20px;
    font-weight: 500;
}}


        .result-details {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
        }}

        .result-details p {{
            margin: 0 20px;
            align-items: center;
            font-size: 1.2rem;
            color: #666;
        }}

        .embrace-well {{
            font-family: 'Audiowide', cursive;
            font-size: 2rem;
            position: absolute;
            top: 30px;
            left: 68px;
        }}
    </style>
</head>
<body>
    <div class="container">
     
        <img src="C:/Users/Sankrishna Goyal/PycharmProjects/rejouice-master/Mano-Mitr/ll.jpg" class="embrace-image">
        <span class="embrace-well">Mano-Mitr</span>
        <br>
        <br>
        <br> <img src="C:/Users/Sankrishna Goyal/PycharmProjects/rejouice-master/Mano-Mitr/ll.jpg" class="embrace-image2"  style="float: center;">
        <br>
        <br>
           
        
        
        <img src="C:/Users/Sankrishna Goyal/PycharmProjects/rejouice-master/Mano-Mitr/Emotion_Detection_CNN-main/static/public/external/kisspngphysiciandiabetesmellituscomputerdiseasepre1864-asht-1300w.png" class="embrace-image1"  style="float: right;">
           <br>
           <br>
           <br>
           <h1>RESULT
           </h1>
           <br>
           <br>
           <br>
           <br>
           <br>
           <br>
        <div>
            <div class="progress-container">
                <div class="progress-bar">{depressed_percentage}% Depressed</div>
            </div>
            <p class="result">{result}</p>
            <div class="result-details">
                <p>Total Frames: {frame_count}</p>
                <p>Depressed Frames: {depression_count}</p>
                <p>{counselorType}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


    # Open result HTML content in a web browser
    with open("result.html", "w") as f:
        f.write(result_html_content)
    webbrowser.open("result.html")

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return "Screening completed"

# Route for the quiz page
@app.route("/quiz")
def quiz():
    return render_template("index.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
