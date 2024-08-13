import speech_recognition as sr
import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')
def works(text):
    try:
       

    # Generate a response using the Generative AI model
        response = model.generate_content(text)

    # Initialize the text-to-speech engine
        engine = pyttsx3.init()

    # Set the speech rate
        engine.setProperty('rate', 200)

    # Speak the generated text
        engine.say(response.text)
        print(response.text)
    # Run the speech synthesizer
        engine.runAndWait()
   
    except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    
    # Adjust the recognizer sensitivity to ambient noise and record audio
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        print('procesing ...')
    
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    
    try:
        # Recognize speech using Google Web Speech API
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    
    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Say 'hello' to get a response. Press Ctrl+C to stop.")
    
    while True:
        # Recognize speech from the microphone
        response = recognize_speech_from_mic(recognizer, microphone)
        
        if response["success"] and response["transcription"]:
            # Convert transcription to lowercase and check for "hello"
            if "hello Ivan" in response["transcription"]:
                
                engine = pyttsx3.init()

    # Set the speech rate
                engine.setProperty('rate', 200)

    # Speak the generated text
                engine.say(response.text)

    # Run the speech synthesizer
                engine.runAndWait()
            else:
                print("You said: {}".format(response["transcription"]))
                works(response["transcription"])
  
        elif response["error"]:
            print("Error: {}".format(response["error"]))

if __name__ == "__main__":
    main()