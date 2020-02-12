import speech_recognition as sr

r=sr.Recognizer()
m=sr.Microphone()
t=""

with m as source:
	r.adjust_for_ambient_noise(source)
	audio = r.listen(source)
	try:
		t+=r.recognize_google(audio)
	except:
		t+=""


print(t)