
from flask import Blueprint, render_template, Response, jsonify,request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

calculate_blueprint = Blueprint('calculate', __name__)

# Sample JSON data

current_data = {}
@calculate_blueprint.route('/charts')
def charts():
    global current_data
    word_stats = process_data(current_data)
    return render_template('charts2.html', word_stats=word_stats)
    pass


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

@calculate_blueprint.route('/', methods=['GET', 'POST'])
def index():
    global current_data  # Refer to the global variable

    if request.method == 'POST':
        json_data = request.json
        current_data = json_data  # Store the received data
        word_stats = process_data(json_data)
        return render_template('index2.html', word_stats=word_stats)

    word_stats = process_data(current_data)  # Use the stored data
    return render_template('index2.html', word_stats=word_stats)
        

@calculate_blueprint.route('/report',)
def report():
    global current_data  # Refer to the global variable
    word_stats = process_data(current_data)  # Use the stored data
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


