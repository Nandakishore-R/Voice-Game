import json
from flask import Flask, render_template, Response
from flask import Flask, render_template, Response, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

app = Flask(__name__)

# Sample JSON data
data = {
    "lemon": {
        "attempts": [
            {"Slno": 1, "level": 1, "TimeTaken": "N/A", "Status": "Correct"},
            {"Slno": 2, "level": 1, "TimeTaken": "N/A", "Status": "Skipped"},
            {"Slno": 3, "level": 1, "TimeTaken": "1", "Status": "Skipped"}
        ],
        "chancesUsed": 3
    },
     "leg": {
        "attempts": [
            {"Slno": 1,"level": 1,"TimeTaken": "3","Status": "Skipped"}
    ],
    "chancesUsed": 1
  },
  "long": {
    "attempts": [
      {"Slno": 1,"level": 1,"TimeTaken": "2",
        "Status": "Skipped"
      }
    ],
    "chancesUsed": 1
  },
  "lunch": {
    "attempts": [
      {
        "Slno": 1,
        "level": 1,
        "TimeTaken": "5",
        "Status": "Skipped"
      }
    ],
    "chancesUsed": 1
  },
  "lamb": {
    "attempts": [
      {
        "Slno": 1,
        "level": 1,
        "TimeTaken": "1",
        "Status": "Skipped"
      }
    ],
    "chancesUsed": 1
  },
  "light": {
    "attempts": [
      {
        "Slno": 1,
        "level": 1,
        "TimeTaken": "3",
        "Status": "Correct"
      }
    ],
    "chancesUsed": 1
  },
  "lazy": {
    "attempts": [
      {
        "Slno": 1,
        "level": 1,
        "TimeTaken": "6",
        "Status": "Correct"
      }
    ],
    "chancesUsed": 4
  }

    # Add other words here...
}
@app.route('/charts')
def charts():
    word_stats = process_data(data)
    return render_template('charts2.html', word_stats=word_stats)



def process_data(data):
    word_stats = []
    for word, word_data in data.items():
        attempts = word_data["attempts"]
        total_attempts = len(attempts)
        total_time = 0
        correct_attempts = 0
        for attempt in attempts:
            level=attempt["level"]
            if attempt["Status"] == "Correct":
                correct_attempts += 1
                if attempt["TimeTaken"] != "N/A":
                    total_time += float(attempt["TimeTaken"])

        average_time_per_attempt = total_time / correct_attempts if correct_attempts > 0 else 0
        accuracy = (correct_attempts / total_attempts) * 100 if total_attempts > 0 else 0

        word_stat = {
            "Word": word,
            "Level":level,
            "TotalAttempts": total_attempts,
            "CorrectAttempts": correct_attempts,
            "Accuracy": accuracy,
            "AverageTimePerAttempt": average_time_per_attempt
        }

        word_stats.append(word_stat)

    return word_stats

@app.route('/')
def index():
    word_stats = process_data(data)
    return render_template('index2.html', word_stats=word_stats)

@app.route('/report')
def report():
    word_stats = process_data(data)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.drawString(30, height - 30, "Word Game Statistics Report")

    y_position = height - 50
    for word_stat in word_stats:
        text = f"Word: {word_stat['Word']}, Total Attempts: {word_stat['TotalAttempts']}, Correct Attempts: {word_stat['CorrectAttempts']}, Accuracy: {word_stat['Accuracy']:.2f}%, Average Time: {word_stat['AverageTimePerAttempt']:.2f} seconds"
        p.drawString(30, y_position, text)
        y_position -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=report.pdf'})

if __name__ == '__main__':
    app.run(debug=True)
