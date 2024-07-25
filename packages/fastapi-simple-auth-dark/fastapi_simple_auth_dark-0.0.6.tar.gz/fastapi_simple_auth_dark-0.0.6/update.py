#!/usr/bin/env python

import argparse
import os
import toml
import re
import hashlib

verbose = False

def sha1(file_path):
    sha1 = hashlib.sha1()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                sha1.update(chunk)
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"
    return sha1.hexdigest()


def list_files_recursive(directory, regexes=None):

    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            for regex in regexes:
                if re.search(regex, file):
                    # print("append", file)
                    files_list.append(os.path.join(root, file))
                    break  # Stop checking other regexes if one matches
            else:
                # print("skip", file)
                pass

    return files_list

def get_args():

    def_src = os.path.expanduser('~/repo/fastapi-simple-auth-basic/')
    def_dst = 'fastapi_simple_auth_dark'

    parser = argparse.ArgumentParser()
    parser.add_argument('src', nargs='?', type=str, default=def_src, 
                        help=f'Input repo of fastapi-simple-auth-basic : {def_src}')
    parser.add_argument('-d', '--dest', type=str, default=def_dst, help=f'Destination: {def_dst}')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help=f'Verbose mode')
    return parser.parse_args()

# vprint function
def vprint(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def fix_css(path: str):

    vprint("fix CSS file", path)

    pattern = r'\{[^{}]*\}'
    replacement = '''{
  --background: #000; /* Background color */
  --background-footer: #222; /* Background color */
  --background-content: #222; /* Background color */
  --text-color: #ccc; /* Text color */
}'''

    with open(path, 'r') as file:
        content = file.read()

    content = re.sub(pattern, replacement, content, count=1)

    with open(path, 'w') as file:
       file.write(content)

def main():

    global verbose

    args = get_args()

    verbose = args.verbose

    src = os.path.join(args.src, 'fastapi_simple_auth_basic')
   
    #recursively list all files in args.dest
    for f in list_files_recursive(src, ['\.html$', '\.py$','\.css$', '\.js$', '\.svg$']):
        frel = os.path.relpath(f, src)
        # print(frel)
        dst = os.path.join('.', args.dest, frel)
        # print(dst)
        srchash = sha1(f)
        dsthash = sha1(dst)
        if srchash != dsthash:
            print(f"COPY {f} to {dst}")
            # os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(f, 'rb') as src_file, open(dst, 'wb') as dst_file:
                dst_file.write(src_file.read())
        else:
            vprint(f"skip {f}")


    fix_css(os.path.join('.', args.dest, 'statics', 'css', 'styles.css'))


        

if __name__ == '__main__':
    main()