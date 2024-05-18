# MultiLanguage ProPresenter
python script to generate a file that can be imported in propresenter 7 with multiple languages or tranlation(s)

introduction video: 
- https://www.youtube.com/watch?v=z6BaM3yR2-k

prerequisites:
- windows
- python 3.x  (howto install: https://www.youtube.com/watch?v=pmwwX_B7EtQ&t=16s)

required python packages
- protobuf
  (on the command prompt run: pip install protobuf )

This program needs a Template to know:
- how many languages or translations are used
- what the text box names are

To create this Template:
- Open propresenter 7 
- create a New Presentation with the name Template
- add the Text object for all required languages or translations
- Give all Text objects a unique name
- put them in the correct order in the Object list
- export the Presentation to this directory (replacing the current Template.pro file)


Group names:
- if you have created additional groups in propresenter, you can also add them to this program
open the file GroupNames.txt and add the additional group names


To start the Multi language editor; example:
- cd \your foler name\MultiLanguageProPresenter
- python3 Main.py


In this program you can 
- paste your song
- add group names like Verse 1, Chorus, etc
- put the translation next to the song text
- click save to store it in the Download directory ( now you can import it into propresenter )

Additional commands required on Linux mint:
ModuleNotFoundError: No module named 'tkinter'
- sudo apt update -y && sudo apt install -y python3.10-tk
- sudo apt install python3-pip
- pip install --upgrade protobuf


Deployment as a website:
- have a website supporting flask
- entrypoint for flask is flask_gui.py

howto website example:
- for more info see also https://help.pythonanywhere.com/pages/Flask/
- create an account on pythonanywhere.com
- create a virtual environment
- in this environment install :
  - pip install protobuf
  - pip install flask
- add a new web app ; select flask
- make the "Source code"  and  "Working directory"  the same
- upload all files to this directory
- select the virtual environment that has been created
- flask_gui.py is the entrypoint for the web gui
