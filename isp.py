import csv
import eng_to_ipa as ipa
from gtts import gTTS
import os

# Load Hindi IPA dictionary from CSV
hindi_ipa_dict = {}
with open('Hindi_IPA_Phonetics.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        hindi_ipa_dict[row[0]] = row[1]

def is_hindi(word):
    # A basic check to see if the word contains any Hindi characters
    return any('\u0900' <= char <= '\u097F' for char in word)

def convert_to_ipa(word):
    if is_hindi(word):
        # Convert Hindi word to IPA using the dictionary
        return ''.join(hindi_ipa_dict.get(char, char) for char in word)
    else:
        # Convert English word to IPA
        return ipa.convert(word)

#def speak_text(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")

# Example usage
word = "बिल्ले"  # Replace with your word
ipa_transcription = convert_to_ipa(word)
print("IPA Transcription:", ipa_transcription)
#speak_text(word, 'en' if not is_hindi(word) else 'hi')
