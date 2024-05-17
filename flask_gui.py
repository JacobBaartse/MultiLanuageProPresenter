from flask import Flask, request, make_response
from SongEditorPro7Generic import get_text_block_names, gen_pro_data
app = Flask(__name__)


@app.route("/")
def home():
    return "<html><body>home page</body></html>"


@app.route("/gen_pro_file", methods=["POST", ])
def song_download():
    # https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database
    form_data = request.form
    # print([form_data])
    text_block_names = get_text_block_names()
    song_text = {}
    for text_block_name in text_block_names:
        song_text[text_block_name] = (form_data[text_block_name]+"\n").split("\n")
    line_count = int(form_data["NumLines"])
    song_binary = gen_pro_data(text_block_names, song_text, line_count)
    response = make_response(song_binary)
    response.headers.set('Content-Type', 'binary/pro')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.pro' % form_data["SongName"])
    return response


@app.route("/input_song", methods=["GET", ])
def song_input():
    # https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=1
    title = ""
    content = ""

    text_block_names = get_text_block_names()
    for name in text_block_names:
        title += f"<th>{name}</th>"

    for name in text_block_names:
        content += f"""<td><textarea id ="{name}" name="{name}" rows="50" cols="50"></textarea></td>"""

    with open("GroupNames.txt", "r") as group_names:
        labels = group_names.read().split("\n")
    label_string = ""
    num_labels_per_line = 13
    for index in range((len(labels)//num_labels_per_line)+1):
        label_string += "\""
        label_string += "\"&nbsp; &nbsp; \"".join(labels[index*num_labels_per_line:(index+1)*num_labels_per_line]) + "\"</br>"

    html = f"""<html><body>
        <form action=gen_pro_file method="post">
            <label>Song name:</label>
            <input id="SongName" name="SongName" type="text" required size="100">
            <br/>
            <br/>
            <label>Number of lines per slide:</label>
            <input id="NumLines" name="NumLines" type="number" value="2" min="1" max="10" required size="5">
            <br/>
            <table>  
                <tr>{title}</tr>
                <tr>{content}</tr>
            </table>
            <div>{label_string}</div>
            <br/>
            <button type="submit">Download</button>
        </form>
    </body></html>"""
    return html


if __name__ == "__main__":
    app.run()