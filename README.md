# MultiLanuagePoPresenter
python script to generate a file that can be imported in propresenter 7 with multiple languages or tranlation(s)


prerequisites:
- windows
- python 3.x

required python packages
- protobuf
  ( pip3 install protobuf )

To change the Text Object names in the generated presentation:
- Open propresenter 7 
- create a New Presentation with the name Template
- add the Text object for all required languages
- Give all Text objects a unique name
- put them in the correct order in the Object list
- export the Presentation to this directory (replacing the current Template.pro file)

start the Multi language editor example:
- cd \MultiLanguageProPresenter
- c:\python11\python3 Main.py


