## How it works:
# We read from one file and write to other and save image to other
# folder. All in one loop over jupyter cells.

import argparse
import sys
import json
import base64
import os
from io import TextIOWrapper
import logging
import re

def markdown_to_org(markdown_lines: list[str]) -> list[str]:
    org_lines = []

    # Convert headers
    header_pattern = re.compile(r'^(#+) (.+)$')
    for line in markdown_lines:
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            header_text = match.group(2)
            org_lines.append('*' * level + ' ' + header_text)
        else:
            org_lines.append(line)



    # Convert source blocks
    org_lines2 = []
    source_block_pattern = re.compile(r'^```[ ]*(\w+)[ ]*$')
    in_source_block = False
    source_block_language = ''
    for line in org_lines:

        if in_source_block:
            if line.strip() == '```':
                in_source_block = False
                org_lines2.append('#+end_src')
            else:
                org_lines2.append(line)
        else:
            m = source_block_pattern.match(line)
            if m:
                in_source_block = True
                source_block_language = m.group(1)
                org_lines2.append(f'#+begin_src {source_block_language} :results none :exports code :eval no')
            else:
                org_lines2.append(line)

    org_lines2 = [s.replace("<br>", "") for s in org_lines2]


    return org_lines2

# source_filename = './draw-samples.ipynb'
DIR_AUTOIMGS = './autoimgs'
org_babel_min_lines_for_block_output = 10 # ob-core.el org-babel-min-lines-for-block-output


def jupyter2org(f:TextIOWrapper, source_file_jupyter: str,
                target_images_dir: str):
    "Main loop."

    # PRINT = lambda *x: print("".join(x))
    # f = open("out.org", "w")
    def PRINT(*args):
        "Write to target functiion."
        if args and isinstance(args[0], list):
            lines = [e for a in args for e in a]
            return f.write("\n".join([x.rstrip() for x in lines]) + '\n')
        else:
            return f.write("".join(args) + '\n')
    # PRINT = lambda *x: f.write("".join(x) + '\n')

    try:
        with open(source_file_jupyter, "r", encoding="utf-8") as infile:
            myfile = json.load(infile)
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    # -- -- parse file -- --
    language_ofkernels = myfile["metadata"]["language_info"]["name"]

    for i, cell in enumerate(myfile["cells"]):
        # -- collect source
        source_lines = cell["source"]
        # -- ORG SRC block header
        header = f"#+begin_src {language_ofkernels} :results output :exports both :session s1"
        tail = "#+end_src"

        # -- collect outputs
        outputs = []
        if "outputs" in cell:
            for j, output in enumerate(cell["outputs"]):
                o = {"text": None, "file_path": None, "data_descr": None}
                # -- test
                if "text" in output:
                    outputs_text = output["text"]
                    o["text"] = outputs_text
                # -- data
                if "data" in output and "image/png" in output["data"]:
                    # - 1) save image 2) insert link to output text 3) format source block header with link
                    # - decode image and remember link to file
                    b64img = base64.b64decode(output["data"]["image/png"])
                    filen = f'{i}_{j}.png'
                    local_image_file_path = os.path.join(DIR_AUTOIMGS, filen)
                    o["file_path"] = local_image_file_path
                    # - save to file
                    with open(os.path.join(target_images_dir, filen), 'wb') as b64imgfile: # real path
                        b64imgfile.write(b64img)
                    # - add description for link
                    if "text/plain" in output["data"]:
                        o["data_descr"] = output["data"]["text/plain"]
                    # - change header for image
                    if "graphics" not in header:  # add only first image to header
                        # -- ORG SRC block header
                        header = f"#+begin_src {language_ofkernels} :results file graphics :file {local_image_file_path} :exports both :session s1"
                outputs.append(o)

        # -- print markdown / code
        if cell["cell_type"] == "markdown":
            PRINT(markdown_to_org(source_lines))
            # source_lines = [s.replace("<br>", "") for s in source_lines]
            # PRINT(source_lines[0].replace("#", "*"))
            # if len(source_lines) > 1:
            #     PRINT(source_lines[1:])
            # PRINT('# asd')
        else:  # == "code":
            PRINT(header)
            PRINT(source_lines)
            PRINT(tail)
            PRINT()

        # -- print outputs - text and data
        for k, o in enumerate(outputs):
            # -- test
            # o = {"text": None, "data_file": None, "data_descr": None}
            if o["text"] is not None:
                if len(o["text"]) <= org_babel_min_lines_for_block_output:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else "")) # add index for several RESULT
                    PRINT("".join([": " + t for t in o["text"]])) # .startswith()
                    PRINT()
                else:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else ""))
                    PRINT("#+begin_example")
                    for t in o["text"]:
                        if t[0] == '*' or t.startswith("#+"):
                            PRINT("," + t)
                        else:
                            PRINT(t)
                    PRINT("#+end_example")
                    PRINT()
            if o["file_path"] is not None:
                # if RESULT is ferst we don't add name to it
                if o["text"] is not None and k == 0:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else ""))
                else:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else "")) # add index for several RESULT
                # - PRINT link
                # desc = "" if o["data_descr"] is None else "[" + "".join(o["data_descr"]) + "]"
                desc = "" if o["data_descr"] is None else "".join(o["data_descr"])
                PRINT("[[file:" + o["file_path"] + "]] " + desc)
                PRINT()


def j2p_main(source_file_jupyter: str, target_file_org: str = None,
             overwrite: bool = False):
    # print(source_file_jupyter, target_file_org, overwrite)
    if target_file_org:
        s_path = os.path.dirname(target_file_org)
        target_images_dir = os.path.normpath(os.path.join(s_path, DIR_AUTOIMGS))
    else:
        target_images_dir = DIR_AUTOIMGS
    # - create directory for images:
    if not os.path.exists(target_images_dir):
        os.makedirs(target_images_dir)
    # - create target_file_org
    if target_file_org is None:
        target_file_org = os.path.splitext(source_file_jupyter)[0] + '.org'
    # - overwrite?
    if not overwrite:
        if os.path.isfile(target_file_org):
            logging.critical("File already exist.")
            return
    # - create target file and start conversion
    with open(target_file_org, "w") as f:
        jupyter2org(f, source_file_jupyter, target_images_dir)


# def parse_arguments():

# return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Jupyter notebook to Org file (Emacs) and vice versa",
        usage="j2o myfile.ipynb [-w] [-j myfile.ipynb] [-o myfile.org]")
    parser.add_argument("jupfile_", nargs='?', default=None,
                        help="Jupyter file")
    parser.add_argument("-j", "--jupfile",
                        help="Jupyter file")
    parser.add_argument("-o", "--orgfile",
                        help="Target filename of Org file. If not specified, " +
                        "it will use the filename of the Jupyter file and append .ipynb")
    parser.add_argument("-w", "--overwrite",
                        action="store_true",
                        help="Flag whether to overwrite existing target file.")
    args = parser.parse_args()
    jupf = args.jupfile_ if args.jupfile_ else args.jupfile
    if not jupf:
        parser.parse_args(["-h"])
    else:
        j2p_main(jupf, args.orgfile, args.overwrite)


if __name__ == "__main__":
    main()
