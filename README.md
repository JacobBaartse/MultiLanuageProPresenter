# MultiLanuagePoPresenter
python script to generate a file that can be imported in propresenter 7 with multiple languages or tranlation(s)


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
