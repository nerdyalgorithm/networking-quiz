from flask import Flask, request, render_template
import sqlite3
import random
import os

app = Flask(__name__)

# All questions from Networking 101 note (50 total, covering everything)
QUESTIONS = [
    {"id": 0, "text": "Networking is the connection of multiple devices through a medium to communicate and share data.",
    "obj_q": "What does networking connect?", "options": ["Power sources", "Multiple devices", "Single devices", "Software"], "obj_answer": "Multiple devices",
    "theory_q": "Explain how networking connects devices to share data."},
    {"id": 1, "text": "The sender of data is the source, the receiver is the destination.",
    "obj_q": "What’s the source in networking?", "options": ["Receiver", "Sender", "Medium", "Server"], "obj_answer": "Sender",
    "theory_q": "Describe the roles of source and destination in networking."},
    {"id": 2, "text": "Purpose of networking includes data sharing (audio, video, text).",
    "obj_q": "What’s a purpose of networking?", "options": ["Data sharing", "Hardware repair", "Encryption", "Cooling"], "obj_answer": "Data sharing",
    "theory_q": "Why is data sharing a key purpose of networking?"},
    {"id": 3, "text": "Resource sharing includes hardware like printers and scanners.",
    "obj_q": "What’s a shared resource?", "options": ["Printers", "Passwords", "Electricity", "Code"], "obj_answer": "Printers",
    "theory_q": "How does resource sharing benefit a network?"},
    {"id": 4, "text": "Devices are hardware within the network.",
    "obj_q": "What are devices in networking?", "options": ["Software", "Hardware", "Protocols", "Bandwidth"], "obj_answer": "Hardware",
    "theory_q": "Explain the role of devices in a network."},
    {"id": 5, "text": "Media is the medium through which devices are connected.",
    "obj_q": "What connects devices?", "options": ["Server", "Media", "Client", "Adapter"], "obj_answer": "Media",
    "theory_q": "How does media enable device connections?"},
    {"id": 6, "text": "Wired media includes twisted pair cables (STP, UTP).",
    "obj_q": "Which is a wired medium?", "options": ["Bluetooth", "Twisted pair", "Radio waves", "Microwaves"], "obj_answer": "Twisted pair",
    "theory_q": "Why use twisted pair cables in wired media?"},
    {"id": 7, "text": "Fiber optic cables include single-mode for long distances.",
    "obj_q": "What’s single-mode fiber for?", "options": ["Short range", "Long distance", "Low speed", "Bluetooth"], "obj_answer": "Long distance",
    "theory_q": "Explain why single-mode fiber is used for long distances."},
    {"id": 8, "text": "Wireless media includes Bluetooth.",
    "obj_q": "What’s a wireless medium?", "options": ["UTP", "Bluetooth", "Coaxial", "Fiber"], "obj_answer": "Bluetooth",
    "theory_q": "How does Bluetooth function as a wireless medium?"},
    {"id": 9, "text": "Network adapter holds network information.",
    "obj_q": "What does a network adapter do?", "options": ["Manages software", "Holds network info", "Serves data", "Connects cables"], "obj_answer": "Holds network info",
    "theory_q": "Describe the role of a network adapter."},
    {"id": 10, "text": "PAN covers a small range, typically 10 meters.",
    "obj_q": "What’s the range of a PAN?", "options": ["10 meters", "100 meters", "1 km", "Global"], "obj_answer": "10 meters",
    "theory_q": "Why is a PAN limited to 10 meters?"},
    {"id": 11, "text": "LAN max range is 100 meters for ethernet cables.",
    "obj_q": "What’s the max LAN range with ethernet?", "options": ["10m", "100m", "500m", "1km"], "obj_answer": "100m",
    "theory_q": "Explain why LANs are limited to 100 meters with ethernet."},
    {"id": 12, "text": "WAN spans multiple regions or the globe.",
    "obj_q": "What does a WAN span?", "options": ["A building", "A city", "Multiple regions", "10 meters"], "obj_answer": "Multiple regions",
    "theory_q": "How does a WAN differ from a LAN in scope?"},
    {"id": 13, "text": "MAN covers a large area like a city.",
    "obj_q": "What does a MAN cover?", "options": ["10 meters", "A building", "A city", "The globe"], "obj_answer": "A city",
    "theory_q": "What’s the purpose of a MAN?"},
    {"id": 14, "text": "Attenuation weakens signals over 100 meters in LANs.",
    "obj_q": "What weakens LAN signals over 100m?", "options": ["Attenuation", "Encryption", "Bandwidth", "Crosstalk"], "obj_answer": "Attenuation",
    "theory_q": "How does attenuation affect LAN performance?"},
    {"id": 15, "text": "Peripherals are external devices like printers.",
    "obj_q": "What’s a peripheral?", "options": ["Server", "Printer", "NOS", "Adapter"], "obj_answer": "Printer",
    "theory_q": "Why are peripherals important in networks?"},
    {"id": 16, "text": "Bandwidth refers to network capacity.",
    "obj_q": "What measures network capacity?", "options": ["Bandwidth", "Latency", "Protocol", "Topology"], "obj_answer": "Bandwidth",
    "theory_q": "Explain the role of bandwidth in networking."},
    {"id": 17, "text": "Client-server uses a central server.",
    "obj_q": "What’s central in client-server?", "options": ["Peer", "Server", "Hybrid", "Bus"], "obj_answer": "Server",
    "theory_q": "How does a client-server architecture function?"},
    {"id": 18, "text": "P2P has no client-server distinction.",
    "obj_q": "What’s true of P2P?", "options": ["Has a server", "No client-server distinction", "Uses a bus", "Only clients"], "obj_answer": "No client-server distinction",
    "theory_q": "Why does P2P lack a client-server distinction?"},
    {"id": 19, "text": "Hybrid combines P2P and client-server.",
    "obj_q": "What’s a hybrid architecture?", "options": ["P2P only", "Client-server only", "P2P and client-server", "Bus only"], "obj_answer": "P2P and client-server",
    "theory_q": "What’s the advantage of a hybrid architecture?"},
    {"id": 20, "text": "Bus topology uses a single main cable.",
    "obj_q": "What connects devices in bus topology?", "options": ["Hub", "Single cable", "Switch", "Mesh"], "obj_answer": "Single cable",
    "theory_q": "How does a bus topology use a single cable?"},
    {"id": 21, "text": "Terminator stops data roaming in bus topology.",
    "obj_q": "What stops data roaming in bus?", "options": ["Terminator", "T-connector", "NIC", "Switch"], "obj_answer": "Terminator",
    "theory_q": "Why is a terminator needed in bus topology?"},
    {"id": 22, "text": "Bus topology is hard to troubleshoot.",
    "obj_q": "What’s a bus topology downside?", "options": ["Easy to troubleshoot", "Hard to troubleshoot", "High speed", "No collisions"], "obj_answer": "Hard to troubleshoot",
    "theory_q": "Why is troubleshooting difficult in bus topology?"},
    {"id": 23, "text": "Star topology uses a hub or switch.",
    "obj_q": "What’s central in star topology?", "options": ["Bus", "Hub or switch", "Terminator", "Router"], "obj_answer": "Hub or switch",
    "theory_q": "How does a hub or switch work in star topology?"},
    {"id": 24, "text": "Star topology fails if the central device breaks.",
    "obj_q": "What fails star topology if broken?", "options": ["Node", "Central device", "Cable", "NIC"], "obj_answer": "Central device",
    "theory_q": "What happens if the central device fails in star topology?"},
    {"id": 25, "text": "Ring topology has unidirectional data flow.",
    "obj_q": "How does data flow in ring topology?", "options": ["Bidirectional", "Unidirectional", "Random", "Via hub"], "obj_answer": "Unidirectional",
    "theory_q": "Why does ring topology use unidirectional flow?"},
    {"id": 26, "text": "Token passing prevents collisions in ring topology.",
    "obj_q": "What prevents collisions in ring?", "options": ["Token passing", "Hub", "Switch", "Bus"], "obj_answer": "Token passing",
    "theory_q": "How does token passing prevent collisions?"},
    {"id": 27, "text": "Mesh topology connects every node to every other.",
    "obj_q": "How are nodes connected in mesh?", "options": ["To a bus", "To a hub", "To every node", "In a circle"], "obj_answer": "To every node",
    "theory_q": "Why does mesh topology connect every node?"},
    {"id": 28, "text": "Mesh topology has no single failure point.",
    "obj_q": "What’s a mesh advantage?", "options": ["Cheap", "No single failure point", "Easy setup", "Slow"], "obj_answer": "No single failure point",
    "theory_q": "How does mesh topology avoid single failure points?"},
    {"id": 29, "text": "Tree topology has a root node.",
    "obj_q": "What’s the top node in tree topology?", "options": ["Leaf", "Root", "Switch", "Bus"], "obj_answer": "Root",
    "theory_q": "What’s the role of the root node in tree topology?"},
    {"id": 30, "text": "Hybrid topology combines star and bus.",
    "obj_q": "What’s a common hybrid topology?", "options": ["Star-bus", "Ring-mesh", "Bus-tree", "LAN-WAN"], "obj_answer": "Star-bus",
    "theory_q": "How does a star-bus hybrid topology work?"},
    {"id": 31, "text": "IP address is a 12-digit number separated by dots.",
    "obj_q": "What separates an IP address?", "options": ["Commas", "Dots", "Hyphens", "Spaces"], "obj_answer": "Dots",
    "theory_q": "Why are IP addresses separated by dots?"},
    {"id": 32, "text": "Class C IP range is 192-223.",
    "obj_q": "What’s the Class C IP range?", "options": ["1-127", "128-191", "192-223", "224-255"], "obj_answer": "192-223",
    "theory_q": "What’s the significance of Class C IP addresses?"},
    {"id": 33, "text": "DNS translates domain names to IP addresses.",
    "obj_q": "What does DNS translate?", "options": ["MAC to IP", "Domain to IP", "IP to MAC", "Protocols"], "obj_answer": "Domain to IP",
    "theory_q": "How does DNS simplify networking?"},
    {"id": 34, "text": "Subnet mask for Class A is 255.0.0.0.",
    "obj_q": "What’s the Class A subnet mask?", "options": ["255.0.0.0", "255.255.0.0", "255.255.255.0", "0.0.0.0"], "obj_answer": "255.0.0.0",
    "theory_q": "Why does Class A use a 255.0.0.0 subnet mask?"},
    {"id": 35, "text": "MAC address uses hyphens.",
    "obj_q": "What separates MAC address values?", "options": ["Dots", "Hyphens", "Colons", "Spaces"], "obj_answer": "Hyphens",
    "theory_q": "Why are MAC addresses formatted with hyphens?"},
    {"id": 36, "text": "MAC address is assigned by the manufacturer.",
    "obj_q": "Who assigns a MAC address?", "options": ["ISP", "User", "Manufacturer", "Router"], "obj_answer": "Manufacturer",
    "theory_q": "Why is the MAC address assigned by the manufacturer?"},
    {"id": 37, "text": "Hub broadcasts data to all devices.",
    "obj_q": "What does a hub do?", "options": ["Filters traffic", "Broadcasts data", "Routes packets", "Translates"], "obj_answer": "Broadcasts data",
    "theory_q": "How does a hub broadcast data in a network?"},
    {"id": 38, "text": "Switch is more efficient than a hub.",
    "obj_q": "What’s more efficient than a hub?", "options": ["Router", "Switch", "Bridge", "Modem"], "obj_answer": "Switch",
    "theory_q": "Why is a switch more efficient than a hub?"},
    {"id": 39, "text": "Switch uses store and forward method.",
    "obj_q": "What method does a switch use?", "options": ["Broadcast", "Store and forward", "Random", "Loop"], "obj_answer": "Store and forward",
    "theory_q": "How does the store and forward method work in a switch?"},
    {"id": 40, "text": "Router sorts data by IP address.",
    "obj_q": "What does a router use to sort data?", "options": ["MAC address", "IP address", "Bandwidth", "Topology"], "obj_answer": "IP address",
    "theory_q": "Why does a router use IP addresses to sort data?"},
    {"id": 41, "text": "Bridge filters traffic between segments.",
    "obj_q": "What filters traffic between segments?", "options": ["Bridge", "Gateway", "Modem", "Hub"], "obj_answer": "Bridge",
    "theory_q": "How does a bridge filter traffic?"},
    {"id": 42, "text": "Gateway connects different network types.",
    "obj_q": "What connects different networks?", "options": ["Router", "Gateway", "Switch", "Bridge"], "obj_answer": "Gateway",
    "theory_q": "Why is a gateway needed for different networks?"},
    {"id": 43, "text": "Modem converts analog to digital signals.",
    "obj_q": "What does a modem convert?", "options": ["IP to MAC", "Analog to digital", "Data to light", "Wired to wireless"], "obj_answer": "Analog to digital",
    "theory_q": "How does a modem convert signals?"},
    {"id": 44, "text": "STP resists EMI unlike UTP.",
    "obj_q": "Which cable resists EMI?", "options": ["UTP", "STP", "Coaxial", "Both B and C"], "obj_answer": "STP",
    "theory_q": "Why does STP resist EMI better than UTP?"},
    {"id": 45, "text": "Bluetooth has a 10-meter range.",
    "obj_q": "What’s Bluetooth’s range?", "options": ["10m", "100m", "1km", "Unlimited"], "obj_answer": "10m",
    "theory_q": "Why is Bluetooth limited to a 10-meter range?"},
    {"id": 46, "text": "Radio waves are cheaper than microwaves.",
    "obj_q": "Which is cheaper?", "options": ["Microwaves", "Bluetooth", "Radio waves", "Fiber"], "obj_answer": "Radio waves",
    "theory_q": "Why are radio waves cheaper than microwaves?"},
    {"id": 47, "text": "Malware is an intentional human threat.",
    "obj_q": "What’s an intentional threat?", "options": ["Flood", "Malware", "Earthquake", "Error"], "obj_answer": "Malware",
    "theory_q": "How does malware threaten a network?"},
    {"id": 48, "text": "Employee error is an unintentional threat.",
    "obj_q": "What’s an unintentional threat?", "options": ["Hacking", "Employee error", "Sniffing", "Spamming"], "obj_answer": "Employee error",
    "theory_q": "Why are employee errors a threat?"},
    {"id": 49, "text": "Sniffing intercepts network traffic.",
    "obj_q": "What does sniffing do?", "options": ["Encrypts data", "Intercepts traffic", "Boosts speed", "Filters"], "obj_answer": "Intercepts traffic",
    "theory_q": "How does sniffing attack a network?"}
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
    conn = sqlite3.connect('quiz.db')  # Disk-based SQLite
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attempts 
                (id INTEGER PRIMARY KEY, question TEXT, qtype TEXT, answer TEXT, user_answer TEXT, correct INTEGER)''')
    conn.commit()
    conn.close()

selected_questions = []

@app.route('/', methods=['GET', 'POST'])
def start():
    global selected_questions
    if request.method == 'POST':
        qtype = request.form['qtype']
        num_questions = int(request.form['num_questions'])
        selected_questions = random.sample(QUESTIONS, min(num_questions, len(QUESTIONS)))
        return render_template('quiz.html', questions=selected_questions, qtype=qtype, num_questions=num_questions)
    return render_template('start.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    global selected_questions
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    qtype = request.form['qtype']
    num_questions = int(request.form['num_questions'])
    score = 0
    total = num_questions
    failed = []

    for q in selected_questions:
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
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT env
    app.run(host="0.0.0.0", port=port, debug=True)