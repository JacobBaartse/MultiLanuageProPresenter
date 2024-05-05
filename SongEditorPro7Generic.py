import presentation_pb2
from uuid import uuid1
import pickle

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
            if line_index >= len(song_texts[text_block_name]):
                return slides
            if not to_next_line:
                if (song_texts[text_block_name][line_index].strip() == "") or (lines_in_slide == max_line_count):
                    if slide:
                        slides.append(slide)
                    slide = {}
                    lines_in_slide = 0
                if song_texts[text_block_name][line_index].strip() == "":
                    to_next_line = True
            if not to_next_line:
                if song_texts[text_block_name][line_index] in labels:
                    to_next_line = True
                    slide["label"] = song_texts[text_block_name][line_index]
            if not to_next_line:
                if text_block_name in slide:
                    slide[text_block_name] += "\\par " + encode_for_rtf(song_texts[text_block_name][line_index])
                else:
                    slide[text_block_name] = encode_for_rtf(song_texts[text_block_name][line_index])
                if index == len(text_block_names) - 1:
                    lines_in_slide += 1
        line_index += 1


def save_song(text_block_names, song_texts, line_count, output_filename):
    #  store also as pickle file.
    with open(output_filename + '.pkl', 'wb+') as f:
        pickle.dump(song_texts, f)

    intro_uuid = make_uuid()
    cue_group_names = {"Intro": 0,
                       }

    sample_file = r"Template.pro"
    presentation_obj = presentation_pb2.Presentation()
    file1 = open(sample_file, mode='rb')
    presentation_obj.ParseFromString(file1.read())

    rtf_data_big_font = b'{\\rtf0\\ansi\\ansicpg1252' \
                        b'{\\fonttbl\\f0\\fnil ArialMT;}' \
                        b'{\\colortbl;\\red255\\green255\\blue255;\\red255\\green255\\blue255;}' \
                        b'{\\*\\expandedcolortbl;\\csgenericrgb\\c100000\\c100000\\c100000\\c100000;\\csgenericrgb\\c100000\\c100000\\c100000\\c0;}' \
                        b'{\\*\\listtable}' \
                        b'{\\*\\listoverridetable}' \
                        b'\\uc1\\paperw37980\\margl0\\margr0\\margt0\\margb0\\pard\\li0\\fi0\\ri0\\qc\\sb0\\sa0\\sl240\\slmult1\\slleading0\\f0\\b0\\i0\\ul0\\strike0\\fs160\\expnd0\\expndtw0\\cf1\\strokewidth0\\strokec1\\nosupersub\\ulc0\\highlight2\\cb2 '

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
        for element in presentation_obj.cues[-1].actions[0].slide.presentation.base_slide.elements:
            text_block_name = element.element.name
            if text_block_name in slide_text:
                element.element.uuid.string = make_uuid()
                element.element.text.rtf_data = rtf_data_big_font + slide_text[text_block_name].encode() + b"}"
            else:
                element.element.uuid.string = make_uuid()
                element.element.text.rtf_data = empty_rtf

    add_slide(presentation_obj, cue_group_names, slide_label="Interlude")
    add_slide(presentation_obj, cue_group_names, slide_label="Ending")

    with open(output_filename + ".pro", "wb") as pro_file:
        pro_file.write(presentation_obj.SerializeToString())


if __name__ == "__main__":
    current_verses = [{'text': 'Test song l1 verse 1 engels.\n Song trail l1 verse 1 vertaling.', 'label': 'Verse 1'}, {'text': 'Test song l2 verse 1 engels.\n Song trail l2 verse 1 vertaling.', 'label': 'Verse 1'}, {'text': 'Test song l1 verse 2 engels,\n Song trail l1 verse 2 vertaling,\nTest song l2 verse 2 engels.\n Song trail l2 verse 2 vertaling.', 'label': 'Verse 2'}]
    output_filename = r"C:\Users\fam_b\Downloads\test_1.pro"

    save_song(current_verses, output_filename)

