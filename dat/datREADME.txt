In your script:
from dat import dat_main as data_main
...
self.dat = data_main.Data()
...
audio_visual_data = bytearray(self.dat.data("file_name_without_extension"))
# Then use something that can handle the bytes e.g:
self.bgPicImg = Image.open(io.BytesIO(audio_visual_data))


Folder structure:
/program
programscript.py

        /dat
	dat_main.py
	icon.ico
	datREADME.txt

	    /img
	    __init__.py
	    image1.py

	    /etc
	    __init__.py
	    audioVisual1.py
