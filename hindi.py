import speech_recognition as sr
import openai
from itertools import groupby
import os
import re

def process_transcript(transcript):
    # Split the transcript into words and remove consecutive duplicates
    words = transcript.split()
    processed_words = [word for i, word in enumerate(words) if i == 0 or word != words[i-1]]

    # Remove repeated characters in each word
    processed_transcript = ' '.join([''.join([k for k, g in groupby(word)]) for word in processed_words])
    return processed_transcript

def predict_with_openai(processed_text, language):
    try:
        prompt_text = f"In the {language} language, a person said '{processed_text}'. What could be the complete and correct word they are trying to say?"
        response = openai.Completion.create(
            model="text-davinci-003",  # Replace with the latest model as needed
            prompt=prompt_text,
            max_tokens=10
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error in prediction: {e}"

def recognize_speech_from_mic(recognizer, microphone, language_code):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {"success": True, "error": None, "transcript": ""}
    try:
        response["transcript"] = recognizer.recognize_google(audio, language=language_code)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def main():
    # Use environment variable for OpenAI API key
    openai.api_key = os.getenv('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')

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    language = input("Please specify the language (English/Hindi): ").strip().lower()
    language_code = "hi-IN" if language == "hindi" else "en-US"

    if language not in ["english", "hindi"]:
        print("Invalid language. Please choose English or Hindi.")
        return

    print("Please speak now.")
    response = recognize_speech_from_mic(recognizer, microphone, language_code)

    if response["success"]:
        processed_transcript = process_transcript(response["transcript"])
        print("Processed Transcript:", processed_transcript)

        prediction = predict_with_openai('Haaaa lllllll oo', language)
        print("OpenAI Prediction:", prediction)
    else:
        print("Error:", response["error"])

if __name__ == "__main__":
    main()
