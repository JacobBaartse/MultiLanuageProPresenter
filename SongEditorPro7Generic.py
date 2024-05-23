import presentation_pb2
from uuid import uuid1
import json

TEMPLATE = 0


def make_uuid():
    tmp = uuid1().urn.split("uuid:")[1]
    return tmp


def add_que_group(presentation_obj, cue_group_names, slide_label, slide_uuid):
    presentation_obj.cue_groups.add()
    cue_group_id = len(presentation_obj.cue_groups) - 1
    cue_group_names[slide_label] = cue_group_id
    presentation_obj.cue_groups[cue_group_id].CopyFrom(presentation_obj.cue_groups[TEMPLATE])
    presentation_obj.cue_groups[cue_group_id].group.uuid.string = make_uuid()
    presentation_obj.cue_groups[cue_group_id].group.name = slide_label
    presentation_obj.cue_groups[cue_group_id].group.application_group_identifier.string = make_uuid()
    presentation_obj.cue_groups[cue_group_id].group.application_group_name = slide_label
    # presentation_obj.cue_groups[cue_group_id].cue_identifiers.add()  # there is already one in the template.
    presentation_obj.cue_groups[cue_group_id].cue_identifiers[-1].string = slide_uuid


def add_slide(presentation_obj, cue_group_names, slide_label):
    slide_uuid = make_uuid()
    add_que_group(presentation_obj, cue_group_names, slide_label, slide_uuid)
    presentation_obj.cues.add()
    presentation_obj.cues[-1].CopyFrom(presentation_obj.cues[TEMPLATE])
    presentation_obj.cues[-1].uuid.string = slide_uuid
    presentation_obj.cues[-1].actions[0].slide.presentation.base_slide.elements[0].element.uuid.string = make_uuid()
    presentation_obj.cues[-1].actions[0].slide.presentation.base_slide.elements[1].element.uuid.string = make_uuid()


def encode_for_rtf(some_string):
    some_string = some_string.replace("\\", "\\\\")
    some_string = some_string.replace("\r", "")
    some_string = some_string.replace("{", "\\u123?")
    some_string = some_string.replace("}", "\\u125?")
    return some_string


def get_text_block_names():
    names = []
    sample_file = r"Template.pro"
    presentation_obj = presentation_pb2.Presentation()
    file1 = open(sample_file, mode='rb')
    presentation_obj.ParseFromString(file1.read())
    for element in presentation_obj.cues[-1].actions[0].slide.presentation.base_slide.elements:
        names.append(element.element.name)
    return names


def split_slides(text_block_names, song_texts, max_line_count):
    slides = []
    slide = {"label": "Verse 1"}
    with open("GroupNames.txt", "r") as group_names:
        labels = group_names.read().split("\n")
    line_index = 0
    lines_in_slide = 0
    while True:
        to_next_line = False
        for index, text_block_name in enumerate(text_block_names):
            if line_index >= len(song_texts[text_block_names[0]]):
                return slides
            if not to_next_line:  # slide complete
                if (song_texts[text_block_names[0]][line_index].strip() == "") or (lines_in_slide == max_line_count):
                    if slide:  # skip empty slides
                        slides.append(slide)
                    slide = {}
                    lines_in_slide = 0
                if song_texts[text_block_names[0]][line_index].strip() == "":
                    to_next_line = True
            if not to_next_line:  # store any group label
                if song_texts[text_block_names[0]][line_index] in labels:
                    to_next_line = True
                    slide["label"] = song_texts[text_block_name][line_index]
            if not to_next_line:  # append lines to slide
                if len(song_texts[text_block_name]) > line_index:
                    if text_block_name in slide and slide[text_block_name]:
                        slide[text_block_name] += "\\par " + encode_for_rtf(song_texts[text_block_name][line_index])
                    else:
                        slide[text_block_name] = encode_for_rtf(song_texts[text_block_name][line_index])
                if index == len(text_block_names) - 1:
                    lines_in_slide += 1
        line_index += 1


def gen_pro_data(text_block_names, song_texts, line_count):
    intro_uuid = make_uuid()
    cue_group_names = {"Intro": 0,
                       }

    sample_file = r"Template.pro"
    presentation_obj = presentation_pb2.Presentation()
    file1 = open(sample_file, mode='rb')
    presentation_obj.ParseFromString(file1.read())

    colors = [b"\\red255\\green255\\blue255;",
              b"\\red0\\green255\\blue255;",
              b"\\red255\\green255\\blue0;",
              b"\\red255\\green0\\blue255;",
              b"\\red125\\green125\\blue255;",
              b"\\red125\\green255\\blue125;",
              b"\\red255\\green125\\blue125;"]
    rtf_data_big_font = b'{\\rtf0\\ansi\\ansicpg1252' \
                        b'{\\fonttbl\\f0\\fnil ArialMT;}' \
                        b'{\\colortbl;FONT_COLOR\\red0\\green0\\blue0;}' \
                        b'\\uc1\\fs160\\cf1\\cb2 '

    # remove text from intro slide
    empty_rtf = r"{\rtf1\ansi}".encode()
    presentation_obj.cues[0].actions[0].slide.presentation.base_slide.elements[0].element.text.rtf_data = empty_rtf
    presentation_obj.cues[0].actions[0].slide.presentation.base_slide.elements[1].element.text.rtf_data = empty_rtf
    # update reference to intro slide
    presentation_obj.cue_groups[0].group.name = "Intro"
    presentation_obj.cue_groups[0].cue_identifiers[0].string = intro_uuid
    presentation_obj.cues[0].uuid.string = intro_uuid
    presentation_obj.cue_groups[-1].group.application_group_identifier.string = make_uuid()

    slide_label = None
    song_texts = split_slides(text_block_names, song_texts, line_count)
    for slide_text in song_texts:
        slide_uuid = make_uuid()
        if "label" in slide_text:
            slide_label = slide_text["label"]
        if slide_label in cue_group_names:
            cue_group_id = cue_group_names[slide_label]
            presentation_obj.cue_groups[cue_group_id].cue_identifiers.add()
            presentation_obj.cue_groups[cue_group_id].cue_identifiers[-1].string = slide_uuid
        else:
            add_que_group(presentation_obj, cue_group_names, slide_label, slide_uuid)

        presentation_obj.cues.add()
        presentation_obj.cues[-1].CopyFrom(presentation_obj.cues[TEMPLATE])
        presentation_obj.cues[-1].uuid.string = slide_uuid
        for index, element in enumerate(presentation_obj.cues[-1].actions[0].slide.presentation.base_slide.elements):
            text_block_name = element.element.name
            if text_block_name in slide_text:
                element.element.uuid.string = make_uuid()
                element.element.text.rtf_data = rtf_data_big_font.replace(b"FONT_COLOR", colors[index]) + slide_text[text_block_name].encode() + b"}"
            else:
                element.element.uuid.string = make_uuid()
                element.element.text.rtf_data = empty_rtf

    add_slide(presentation_obj, cue_group_names, slide_label="Interlude")
    add_slide(presentation_obj, cue_group_names, slide_label="Ending")
    return presentation_obj.SerializeToString()


class MemoryFile(object):
    def __init__(self):
        self.data = b""

    def write(self, stuff):
        self.data += stuff.encode()


def save_song(text_block_names, song_texts, line_count, output_filename):
    #  store also as pickle file.
    mem_file = MemoryFile()
    json.dump(song_texts, mem_file)

    with open(output_filename + '.json', 'wb+') as f:
        f.write(mem_file.data)

    with open(output_filename + ".pro", "wb") as pro_file:
        pro_file.write(gen_pro_data(text_block_names, song_texts, line_count))


if __name__ == "__main__":
    print(get_text_block_names())
