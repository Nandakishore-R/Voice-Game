import cv2
import numpy as np
import os
import imageio
import webbrowser
import eng_to_ipa as ipa

# Specify the location of the "lipp" folder
lipp_folder = r'C:\Users\ORACLE\Documents\New folder\TypeGame\lipp'

# Define the mapping between IPA phonetic symbols and image filenames
phonetic_to_image = {
    'k': 'k.png',
    'æ': 'ae.png',
    't': 't.png',
    # Add more mappings for other phonetic symbols as needed
}

# Manually specify the IPA transcription for the word "cat"
ipa_transcription = ['k', 'æ', 't']

def create_lip_animation(ipa_transcription, output_filename):
    frames = []
    # Assume '0.png' is the neutral lip position at the start and end.
    frames.append(cv2.cvtColor(cv2.imread(os.path.join(lipp_folder, '0.png')), cv2.COLOR_BGR2RGB))
    for phoneme in ipa_transcription:
        image_filename = phonetic_to_image.get(phoneme)
        if image_filename:
            frame = cv2.cvtColor(cv2.imread(os.path.join(lipp_folder, image_filename)), cv2.COLOR_BGR2RGB)
            if frame is not None:
                frames.append(frame)
    frames.append(cv2.cvtColor(cv2.imread(os.path.join(lipp_folder, '0.png')), cv2.COLOR_BGR2RGB))
    # Create a GIF from the frames with a frame duration of 100 milliseconds
    if frames:
        output_path = os.path.abspath(output_filename)
        imageio.mimsave(output_path, frames, duration=0.1)  # Set frame duration to 100 milliseconds (0.1 seconds)
        return output_path  # Return the output path


def open_lip_animation(output_filename):
    output_path = os.path.abspath(output_filename)
    
    # Check if the output file exists
    if os.path.exists(output_path):
        webbrowser.open(output_path)  # Open the animation in the default web browser
    else:
        print(f"Error: The file {output_filename} does not exist.")

def main():
    word = "cat"  # Replace with your word
    ipa_transcription = ipa.convert(word)
    print(ipa_transcription)
    phonemes = [phoneme for phoneme in ipa_transcription if phoneme.isalpha()]
    #ipa_transcription = ['k', 'æ', 't']  # Manually specify the IPA transcription
    print(ipa_transcription)
    
    if not ipa_transcription:
        print("Error: Unable to convert the word to IPA.")
        return
    
    output_filename = "lip_animation.gif"  # Specify the output filename with the .gif extension
    gif_path = create_lip_animation(phonemes, output_filename)
    
    if gif_path:
        print(f"Lip animation saved to {gif_path} successfully.")
        open_lip_animation(gif_path)  # Open the animation

if __name__ == "__main__":
    main()
