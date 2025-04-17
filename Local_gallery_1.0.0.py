import os
import sys
import argparse
import dominate
from dominate.tags import *
from urllib.parse import quote
import lg_func
import lg_style


parser = argparse.ArgumentParser(description='Local_gallery is a python script to create photo galleries')

parser.add_argument('folderPath', help='Path to the folder you want to use.')
parser.add_argument('-l', metavar='l', default='0', help='0 = preview, 1 = solo, 2 = preview and solo. If not specified 0 is chosen.')
parser.add_argument('-e', metavar='e', default='0', help='Activates error log file if set to 1')
parser.add_argument('-s', metavar='s', default='1', help='If set to 0 some safety checks are turn off, this will make the script faster but can lead to errors.')

args = parser.parse_args()


cwd = os.getcwd()
root_directory = args.folderPath
if root_directory[-1:] == '"':
    root_directory = root_directory[:-1]
if root_directory[-1:] == '\\':
    root_directory = root_directory[:-1]
pageTitle = root_directory.rsplit('\\', 1)
l_options_list = ['0','1','2']

if not args.l in l_options_list:
    print(f'[!]args -l {args.l}: is not a valid option. \n[i]Type -h to show valid options.')
    sys.exit()

if args.l != '0': # Create solo galleries om args.l on 1 and 2
    #################
    ### Solo part ###
    #################
    cwd_thumbs = cwd + '\\solopage\\thumbsS\\' + pageTitle[1]
    lg_func.get_files_in_directories_solo(root_directory, args.s)
    files_in_directories = lg_func.read_all_files_from_db('lg_previews.db', 'solo')
    thumbnails_of_files = lg_func.generate_thumbnails(files_in_directories, args.e)

    lg_func.save_thumbnails_to_directory(thumbnails_of_files, args.e, cwd_thumbs, 'lg_previews.db', 'solo')
    thumb_dict = lg_func.read_thumbnails_from_db('lg_previews.db', 'solo')
    file_Amount = lg_func.read_amount_from_db('lg_previews.db', 'solo')
    info_from_directory = lg_func.directory_info(files_in_directories)

    for (folder_name, file_paths), (_, thumbnails) in zip(files_in_directories.items(), thumb_dict.items()):
        doc = dominate.document(title=str(pageTitle[1]))
        with doc.head:
            style(lg_style.lgStyle)
        with doc:
            h1(folder_name)
            if args.l == '1':
                h3(root_directory)
            for (folder_nameI, file_pathsI), (_, amountsI) in zip(info_from_directory.items(), file_Amount.items()):
                if folder_name == folder_nameI:
                   h2('Sample size: ' + file_pathsI + ' | Valid files: ' + str(amountsI[0]))

            # Loop through the files and their corresponding thumbnails
            for file_path, thumbnail in zip(file_paths, thumbnails):
                
                # Define the relative path to the thumbnail and the original image
                thumb_path = f'thumbsS/' + pageTitle[1] + f'/{thumbnail}'
                link_image_path_s = 'file:///' + quote(os.path.abspath(file_path))
                # Create the HTML for the thumbnail link
                a(img(src=thumb_path), href=link_image_path_s, _class='photo')

        with open('solopage/Solo_' + folder_name +'.html', 'w', encoding="utf-8") as f:
            f.write(doc.render())
        thumb_path = ''
        link_image_path_s = ''

if args.l != '1': # Create Preview on 0 and 2
    ###############
    ### Preview ###
    ###############
    cwd_thumbs = cwd + '\\thumbsR\\' + pageTitle[1]
    lg_func.get_files_in_directories(root_directory, args.s)
    files_in_directories = lg_func.read_all_files_from_db('lg_previews.db', 'preview')
    thumbnails_of_files = lg_func.generate_thumbnails(files_in_directories, args.e)

    lg_func.save_thumbnails_to_directory(thumbnails_of_files, args.e, cwd_thumbs, 'lg_previews.db', 'preview')
    thumb_dict = lg_func.read_thumbnails_from_db('lg_previews.db', 'preview')
    file_Amount = lg_func.read_amount_from_db('lg_previews.db', 'preview')
    info_from_directory = lg_func.directory_info(files_in_directories)
 
    doc = dominate.document(title=str(pageTitle[1]))

    with doc.head:
        style(lg_style.lgStyle)
        

    with doc:
        h2(root_directory)
        # Get folder name and use it as a title
        for (folder_name, file_paths), (_, thumbnails) in zip(files_in_directories.items(), thumb_dict.items()):
            if args.l == '0':
                
                try:
                    folderURL = file_paths[0].rsplit('\\', 1)
                except:
                    folderURL = 'No Path'
                link_folder_path = 'file:///' + quote(os.path.abspath(folderURL[0]))
                a(h1(folder_name), href=link_folder_path)
            else:
                link_folder_path = quote(folder_name)

                a(h1(folder_name), href='solopage/Solo_' + link_folder_path + '.html')

            # Get resulotion and amount of files in folder. Used as a subtitle
            for (folder_nameI, file_pathsI), (_, amountsI) in zip(info_from_directory.items(), file_Amount.items()):
                if folder_name == folder_nameI:
                    h2('Sample size: ' + file_pathsI + ' | Valid files: ' + str(amountsI[0]))

            # Loop through the files and their corresponding thumbnails
            for file_path, thumbnail in zip(file_paths, thumbnails):
                thumbnail_name = os.path.basename(thumbnail)  # Get the filename of the thumbnail
                thumb_path = f'thumbsR/' + pageTitle[1] + f'/{folder_name}/{thumbnail_name}'
                # Making the link work with normal left click, depending on browser and security settings
                # this might not work as intended
                link_image_path = 'file:///' + quote(os.path.abspath(file_path))

                # Create the HTML for the thumbnail link
                a(img(src=thumb_path), href=link_image_path, _class='photo')

    # Writes the html
    with open(str(pageTitle[1])+'.html', 'w', encoding="utf-8") as f:
        f.write(doc.render())

# Clean up
if os.path.exists('lg_previews.db'):
    try:
        os.remove('lg_previews.db')
        print("[i] Temporery database(lg_previews.db) removed.")
    except:
        print("[!]Can not delete the lg_previews.db")
else:
    print('[!] Database not found.')