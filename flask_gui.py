from flask import Flask, request, make_response
from SongEditorPro7Generic import get_text_block_names, gen_pro_data
import json

app = Flask(__name__)


class MemoryFile(object):
    def __init__(self):
        self.data = b""

    def write(self, stuff):
        self.data += stuff.encode()


def json_download(request):
    form_data = request.form
    text_block_names = get_text_block_names()
    song_text = {}
    for text_block_name in text_block_names:
        a_song_text = form_data[text_block_name].replace("\r", "")
        song_text[text_block_name] = (a_song_text+"\n").split("\n")
    mem_file = MemoryFile()
    json.dump(song_text, mem_file)
    response = make_response(mem_file.data)
    response.headers.set('Content-Type', 'binary/json')
    response.headers.set('Content-Disposition', 'attachment', filename=f'{form_data["SongName"]}.json')
    return response


def song_download(request):
    # https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database
    form_data = request.form
    # print([form_data])
    text_block_names = get_text_block_names()
    song_text = {}
    for text_block_name in text_block_names:
        a_song_text = form_data[text_block_name].replace("\r", "")
        song_text[text_block_name] = (a_song_text+"\n").split("\n")
    line_count = int(form_data["NumLines"])
    song_binary = gen_pro_data(text_block_names, song_text, line_count)
    response = make_response(song_binary)
    response.headers.set('Content-Type', 'binary/pro')
    response.headers.set('Content-Disposition', 'attachment', filename=f'{form_data["SongName"]}.pro')
    return response


@app.route("/", methods=["GET", "POST"])
def song_input():
    loaded_dict = {}
    # https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=1
    if request.method == "POST":
        if "action" in request.files:
            if request.files["action"]:
                # load song data from json file
                json_data = request.files["action"]
                loaded_dict = json.load(json_data.stream)
                loaded_dict["song_title"] = json_data.filename.replace(".json", "")

        if "action" in request.form:
            action = request.form["action"]
            if action == "pro":
                return song_download(request)
            if action == "json":
                return json_download(request)
    title = ""
    content = ""

    text_block_names = get_text_block_names()
    for name in text_block_names:
        title += f"<th>{name}</th>"

    for name in text_block_names:
        if name in loaded_dict:
            song_text = "\n".join(loaded_dict[name]).rstrip("\n")
            content += f"""<td><textarea  style="white-space:pre;" id ="{name}" name="{name}" rows="50" cols="50" class="linked" >{song_text}</textarea></td>\n"""
        else:
            content += f"""<td><textarea  style="white-space:pre;" id ="{name}" name="{name}" rows="50" cols="50" class="linked" ></textarea></td>\n"""

    with open("GroupNames.txt", "r") as group_names:
        labels = group_names.read().split("\n")
    label_string = ""
    num_labels_per_line = 13
    for index in range((len(labels)//num_labels_per_line)+1):
        label_string += "\""
        label_string += "\"&nbsp; &nbsp; \"".join(labels[index*num_labels_per_line:(index+1)*num_labels_per_line]) + "\"<br/>\n"
    song_title = ""
    if "song_title" in loaded_dict:
        song_title = loaded_dict["song_title"]

    jquiry_scripts = """        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> 
     <script>
    $(function(){
    $('.linked').scroll(function(){
        $('.linked').scrollTop($(this).scrollTop());
    })

})
</script>"""
    style = """            <style>
            input[type=file]{
                width:110px;
                color:transparent;
            }
            textarea {
            font-family: 'Courier New', monospace;
            resize: none;
            }
            html * {
               font-family: 'Sonus', 'Arial';
            }
            </style>"""
    html = f"""<!DOCTYPE html>
        <head>
            {jquiry_scripts}
            {style}
        </head>
        <body  style="background-color:LightGray;">
        <form action=# method="post"  enctype="multipart/form-data">
            <label>Song name:</label>
            <input id="SongName" name="SongName" type="text" value="{song_title}" size="100">
            <br/>
            <br/>
            <label>Number of lines per slide:</label>
            <input id="NumLines" name="NumLines" type="number" value="2" min="1" max="10" required size="5">
            <br/>
            <table style='font-family:"Courier New"'>
                <tr>{title}</tr>
                <tr>{content}</tr>
            </table>
            <table><tr>
            <td>Possible Group labels:</td><td> {label_string}</td>
            </tr></table>
            <br/><br/>
            <button type="submit" name="action" value=pro>Download .pro</button>
            <button type="submit" name="action" value=json>Download .json</button>
            <br/><br/>
            <label  name="json_file">Reload .json file:</label>
            <input type="file" name="action" value=load_json accept=".json" onchange="form.submit()" />
        </form>
    </body></html>"""
    return html


# for local testing  should be commented when used while web hosting.
# if __name__ == '__main__':
#     app.run(debug=True)
