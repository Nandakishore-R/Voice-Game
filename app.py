from flask import Flask, render_template, jsonify, request, session,Blueprint
import random
import csv
import speech_recognition as sr
import openpyxl
import calculate
from difflib import SequenceMatcher

app_blueprint = Blueprint('app', __name__)

#app_blueprint.secret_key = 'your_secret_key'
words = []
current_word = ""
current_level = 1
total_questions_answered = 0
correct_answers = 0
stage_settings = {
    1: {'time_limit': 60 , 'correct_answers_needed': 4},
    2: {'time_limit': 60, 'correct_answers_needed': 4},
    3: {'time_limit': 60, 'correct_answers_needed': 4},
}
# Load words from CSV file




def load_words_from_excel(file_path, sheet_name, level):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    words = []

    # Map levels to Excel columns (1 for 'A', 2 for 'B', 3 for 'C', etc.)
    level_column_index = {
        1: 1,  # Column index 1 for level 1
        2: 2,  # Column index 2 for level 2
        3: 3,  # Column index 3 for level 3
        # Add more mappings if there are more levels
    }
    column_index = level_column_index[level]

    # Start reading from row 2 to skip the header
    for row in sheet.iter_rows(min_row=2, min_col=column_index, max_col=column_index, values_only=True):
        word = row[0]
        if word:  # Ensure the cell is not empty
            words.append(word.strip())
    # print(f"Words loaded: {words}")
    return words





@app_blueprint.route('/')
def index():
    print('HIII ALLL')
    global current_level,correct_answers, total_questions_answered
    current_level = 1
    correct_answers = 0
    total_questions_answered = 0
    return render_template('index.html')
    pass

@app_blueprint.route('/start_game', methods=['POST'])
def start_game():
    print("current level")
    print(current_level)
    # session['current_level'] = session.get('current_level', 1)
    # current_level = session['current_level']
    # session['questions_answered'] = 0
    # session['correct_answers'] = 0
    selected_language = request.form['language']
    selected_word_type = request.form['wordType']
    print(f"Selected language: {selected_language}, Selected word type: {selected_word_type}")

    file_path = f'{selected_language}_words.xlsx'  # Example file naming
    sheet_name = selected_word_type


    global words
    words = load_words_from_excel(file_path, sheet_name, current_level)


    selected_word = random.choice(words)  # Randomly select a word

    return jsonify({
        'word': selected_word,
        'stage': f'Level {current_level}',
        'time_limit': stage_settings[current_level]['time_limit'],
        'correct_answers_needed': stage_settings[current_level]['correct_answers_needed']
    })
    

@app_blueprint.route('/end_stage', methods=['POST'])
def end_stage():
    print('HELLO ALL')
    global correct_answers, current_level, total_questions_answered
    level_completed = total_questions_answered >= 8
    eligible_for_next_level = correct_answers >= stage_settings[current_level]['correct_answers_needed']
    print(eligible_for_next_level)
    print(total_questions_answered)
    print(correct_answers)
    # Reset for the next stage
    message = ''
    game_over = False
    correct_answers = 0
    total_questions_answered = 0
    # session['correct_answers'] = 0
    print('Current level')
    print(current_level)

    if current_level >= 3:
        message = "Game Over. You've completed all levels!"
        game_over = True
    elif level_completed and eligible_for_next_level:
        current_level += 1  # Advance to the next level
        message += "End of Level" + str(current_level - 1)
        print('LEVEL IS')
        print(current_level)
    elif level_completed and not eligible_for_next_level:
        message += ". Try again to advance to the next level."


    return jsonify({
        'message': message,
        'eligible_for_next_level': eligible_for_next_level,
        'current_level': current_level,
        'game_over' : game_over
    })

@app_blueprint.route('/restart_game', methods=['POST'])
def restart_game():
    global current_level, correct_answers, total_questions_answered
    # Reset the game state for the user
    print('Restarting')
    current_level = 1
    correct_answers = 0
    total_questions_answered = 0
    return jsonify({'status': 'Game restarted'})


@app_blueprint.route('/skip_question', methods=['POST'])
def skip_question():
    global total_questions_answered
    total_questions_answered += 1
    print('Answered - ')
    print(total_questions_answered)
    
    return jsonify({})

@app_blueprint.route('/correct_update', methods=['POST'])
def correct_update():
    global total_questions_answered, correct_answers
    total_questions_answered += 1
    correct_answers += 1
    print('In correct update')
    print(total_questions_answered)
    return jsonify({})


@app_blueprint.route('/voice_input', methods=['POST'])
def voice_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for voice input...")
        audio = recognizer.listen(source)

    try:
        user_typed_word = recognizer.recognize_google(audio).lower()
        return jsonify({'voice_input': user_typed_word})
    except sr.UnknownValueError:
        return jsonify({'voice_input': ''})  # Handle recognition failure


# @app_blueprint.route('/check_level_completion', methods=['GET'])
# def check_level_completion():
#     global correct_answers, current_level, total_questions_answered
#     level_completed = total_questions_answered >= 5
#     eligible_for_next_level = correct_answers >= 4

#     if level_completed:
#         total_questions_answered = 0  # Reset for the next level
#         correct_answers = 0  # Reset correct answers
#         if eligible_for_next_level:
#             current_level += 1  # Advance to the next level

#     return jsonify({
#         'level_completed': level_completed,
#         'eligible_for_next_level': eligible_for_next_level,
#         'next_level': current_level
#     })

@app_blueprint.route('/compare_words', methods=['POST'])
def compare_words():
    data = request.get_json()
    player_word = data['player_word']
    correct_word = data['correct_word']
    print(player_word)
    print(correct_word)
    # Compare words using SequenceMatcher
    seq_matcher = SequenceMatcher(None, player_word, correct_word)
    similarity_ratio = seq_matcher.ratio()
    differences = list(seq_matcher.get_opcodes())

    # Decide if the word is close enough (e.g., ratio > 0.8)
    print('Similarity - ')
    print(similarity_ratio)
    print("Differences:")
    for tag, i1, i2, j1, j2 in differences:
        print(f"{tag}: {player_word[i1:i2]} --> {correct_word[j1:j2]}")
    return jsonify({
        'similarity_ratio': similarity_ratio
    })
