from flask import Flask, request, render_template
import sqlite3
import random
import os

app = Flask(__name__)

# All questions from Networking 101 note (50 total)
QUESTIONS = [
    {"id": 0, "text": "Networking is the connection of multiple devices through a medium to communicate and share data.",
     "obj_q": "What does networking connect?", "options": ["Power sources", "Multiple devices", "Single devices", "Software"], "obj_answer": "Multiple devices",
     "theory_q": "What does networking connect to share data?"},
    {"id": 1, "text": "The sender of data is the source, the receiver is the destination.",
     "obj_q": "What’s the source in networking?", "options": ["Receiver", "Sender", "Medium", "Server"], "obj_answer": "Sender",
     "theory_q": "What’s the source in networking?"},
    # Add remaining 48 questions here (shortened for brevity)
    {"id": 49, "text": "Sniffing intercepts network traffic.",
     "obj_q": "What does sniffing do?", "options": ["Encrypts data", "Intercepts traffic", "Boosts speed", "Filters"], "obj_answer": "Intercepts traffic",
     "theory_q": "What does sniffing do to a network?"}
]

INSULTS = [
    "As far as intellectual luggage is concerned, you’re traveling lightly",
    "Job seekers would be so happy to fill the vacancy in your head",
    "If they put your brain in a dog it would moo",
    "It whistles, doesn’t it? Your head when it’s windy",
    "Seems like you had a big ass umbrella when it was raining brains",
    "Your brain is like a software demo—limited function and expires quickly",
    "If your thoughts were currency, you’d still be in poverty",
    "I just know water freezes at your IQ level",
    "You have the same cognitive output as a potato, but at least the potato can be useful",
    "Your intelligence is like a parachute with holes—technically there, but completely useless when needed",
    "I’d compare you to a book, but even blank pages hold more information",
    "Your comprehension speed makes a snail look like a race car",
    "If logic were a language, you’d be permanently mute",
    "I fit bench your IQ too, but that’s basically a warm-up 🙂",
    "We need to evaluate the quality of thoughts we have because this is not an acceptable use of a head ✍🏾",
    "Your brain really folds its arms and watches the air in your brain do the reasoning",
    "Sugar dissolves in water, so please don't walk in the rain",
    "Please stick to pictures, you haven’t had a good run with your thoughts"
]

PRAISES = [
    "You’re a networking genius—perfect score vibes!",
    "Brains and beauty, Heaven would be proud!",
    "You aced it like a pro—top-tier intellect!",
    "Your mind’s sharper than a router’s ping!",
    "Networking 101? More like Networking 1000 for you!",
    "You’re basically the LAN lord now!",
    "Perfect score—your brain’s bandwidth is unlimited!",
    "You’re wired for success, no attenuation here!"
]

def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attempts 
                 (id INTEGER PRIMARY KEY, question TEXT, qtype TEXT, answer TEXT, user_answer TEXT, correct INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        qtype = request.form['qtype']
        num_questions = int(request.form['num_questions'])
        selected_questions = random.sample(QUESTIONS, min(num_questions, len(QUESTIONS)))
        return render_template('quiz.html', questions=selected_questions, qtype=qtype, num_questions=num_questions)
    return render_template('start.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    qtype = request.form['qtype']
    num_questions = int(request.form['num_questions'])
    score = 0
    total = num_questions
    failed = []

    for q in QUESTIONS[:num_questions]:
        i = q['id']
        if qtype == 'objective':
            user_answer = request.form.get(f'answer_{i}')
            correct_answer = q['obj_answer']
            is_correct = 1 if user_answer == correct_answer else 0
            if not is_correct and user_answer:
                failed.append(q)
            score += is_correct
            c.execute("INSERT INTO attempts (question, qtype, answer, user_answer, correct) VALUES (?, ?, ?, ?, ?)",
                      (q['obj_q'], qtype, correct_answer, user_answer, is_correct))
        else:
            user_answer = request.form.get(f'answer_{i}')
            is_correct = 1 if user_answer == 'got_it' else 0
            if not is_correct and user_answer:
                failed.append(q)
            score += is_correct
            c.execute("INSERT INTO attempts (question, qtype, answer, user_answer, correct) VALUES (?, ?, ?, ?, ?)",
                      (q['theory_q'], qtype, 'N/A', user_answer, is_correct))
    
    feedback = random.choice(INSULTS) if score < 40 else random.choice(PRAISES)
    conn.commit()
    conn.close()
    return render_template('results.html', score=score, total=total, failed=failed, qtype=qtype, feedback=feedback)

@app.route('/retry', methods=['POST'])
def retry():
    qtype = request.form['qtype']
    num_questions = int(request.form['num_questions'])
    failed_questions = []
    for i in range(num_questions):
        q_text = request.form.get(f'failed_q_{i}')
        if q_text:
            q = next(q for q in QUESTIONS if (q['obj_q'] if qtype == 'objective' else q['theory_q']) == q_text)
            failed_questions.append(q)
    return render_template('quiz.html', questions=failed_questions, qtype=qtype, num_questions=len(failed_questions))

if __name__ == '__main__':
    if not os.path.exists('quiz.db'):
        init_db()
    app.run(debug=True)