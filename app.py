from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Job Sequencing Algorithm
def job_sequencing(jobs):
    jobs = sorted(jobs, key=lambda x: x['profit'], reverse=True)

    max_deadline = max(job['deadline'] for job in jobs)
    slots = [None] * (max_deadline + 1)

    total_profit = 0
    scheduled = []
    rejected = []

    for job in jobs:
        placed = False
        for t in range(job['deadline'], 0, -1):
            if slots[t] is None:
                slots[t] = job['id']
                scheduled.append(job)
                total_profit += job['profit']
                placed = True
                break
        if not placed:
            rejected.append(job)

    return {
        "scheduled": scheduled,
        "timeline": slots[1:],
        "profit": total_profit,
        "rejected": rejected,
        "total_jobs": len(jobs)
    }


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    jobs = data.get("jobs", [])
    return jsonify(job_sequencing(jobs))
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get("message", "")

    # Simple AI logic (you can improve later)
    if "greedy" in question.lower():
        answer = "Greedy choice property means selecting the job with highest profit first."
    elif "deadline" in question.lower():
        answer = "Jobs are scheduled before their deadline to maximize profit."
    else:
        answer = "This is a DAA Job Sequencing problem using Greedy Algorithm."

    return jsonify({"reply": answer})


if __name__ == '__main__':
    app.run(debug=True)