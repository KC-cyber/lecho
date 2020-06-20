import speech_recognition as sr
import time
import os
from gtts import gTTS
import webbrowser

time_ = 0          
                        
def speak(audioString):
	tts = gTTS(text=audioString, lang='en')
	tts.save("audio.mp3")
	os.system("mpg321 audio.mp3")

def recordAudio(): 
	global time_
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		time_ = time.time()
		speak('Please speak.')
		audio = r.listen(source)
		print('Finished recording. Processing input.')
	data = ""
	try:
		data = r.recognize_google(audio)
		print("You said: " + data)
	except sr.UnknownValueError:
		print("I could not understand you,can you repeat?")
	except sr.RequestError:
		print("Not connected to the internet. Please try after sometime. ")
	return data
 
def assistant(data):
	global time_
	
	if data.startswith("search online for"): 
		text = ''
		data = data.split()
		n = data.index('for')
		n += 1
		text = data[n:]
		text = ' '.join(text)
		speak("OK. Searching online for "+text)
		try:
			webbrowser.open("https://www.google.co.in/search?q=" + text)
			#os.system("Mozilla-firefox https://www.google.co.in/search?q=" + text)
		except:
			speak('Oops! Some error occured')

	elif "where is" in data: 
		location = ''
		data = data.split()
		n = data.index('is')
		n += 1
		location = ' '.join(data[n+1:])
		speak("Hold on, I will show you where " + location + " is.")
		try:
			webbrowser.open("https://www.google.com/maps/place/" + location)
			#os.system("Mozilla-Firefox https://www.google.com/maps/place/" + location)
		except:
			speak('Oops! Some error occured')

	elif data == "how are you": 
		speak("I am fine. What about you?")
		data = recordAudio()
		if('i am fine' in data):
			speak('Good to hear that.')
		elif('i am not fine' in data):
			speak('Sorry to hear that, how can I cheer you up?')
	
	elif data=="hi":
		speak("Hello. How can i help you?")

	elif ((i in data for i in ('what','tell me')) and (i in data for i in ('time','date','day'))): 
		day,month,date,t,year = time.ctime().split()
		if('time' in data):
			speak('The time is,'+t)
		if('date' in data):
			speak('The date is,'+date+month+year)
		if('day' in data):
			speak('Today is, '+day+'day')

	else:
		speak('Sorry, I can not do that.') 

def main():
	data = recordAudio()
	if('bye' not in data):
		assistant(data)
		main()
	else:
		 speak("Good bye, have a nice day!")

speak("Hello. I am lecho, your Linux assistant. Please follow the instructions given in the manual. How may i help you?")
print("Note: Active internet connection is required USE THE COMMANDS EXACTLY LIKE HOW IT IS PRESCRIBED Manual:  a) Search online for 'query' - Searches for the string 'query' online. It uses the default web browser of your system.  b) What is the time/day/date - Tells the time/day/date respectively.  c) Where is 'place' - Opens a new tab on chrome and displays the location of 'place' in google maps.  d) Bye/Goodbye - quits the program")
main()
