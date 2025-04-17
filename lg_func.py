import os
import random
from PIL import Image, ImageFile
import time
import sqlite3

#
# version: 1.0.0
#

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Setup database connection and tables
def setup_database(db_path='lg_previews.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Table for preview gallery
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS folder_previews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT,
            file_path TEXT,
            file_index INTEGER,
            file_count_summary TEXT,
            thumbnail_path TEXT
        )
    ''')
    # Table for solo gallery
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solo_gallery_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT,
            file_path TEXT,
            file_index INTEGER,
            file_count_summary TEXT,
            thumbnail_path TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def save_to_database(cursor, folder_name, file_path, file_index, file_count_summary):
    cursor.execute('''
        INSERT INTO folder_previews (folder_name, file_path, file_index, file_count_summary)
        VALUES (?, ?, ?, ?)
    ''', (folder_name, file_path, file_index, file_count_summary))

def get_files_in_directories(root_dir, safety, min_resolution=(300, 400), db_path='lg_previews.db'):
    start_time = time.time()
    print('[i] Getting files for preview gallery')
    
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
    
    conn, cursor = setup_database(db_path)

    for foldername, subfolders, filenames in os.walk(root_dir):
        folder_name = os.path.basename(foldername)
        files = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]

        valid_files = []
        
        if not folder_name:
            continue

        base_name = folder_name
        suffix = 1

        # Generate a unique name for the folder_name else the result stack.
        while True:
            cursor.execute("SELECT 1 FROM folder_previews WHERE folder_name = ?", (folder_name,))
            if cursor.fetchone():
                folder_name = f"{base_name}_{suffix}"
                suffix += 1
            else:
                break

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in allowed_extensions:
                continue

            file_path = os.path.join(foldername, filename)

            if safety == '0':
                valid_files.append(file_path)
            else:
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        if width >= min_resolution[0] and height >= min_resolution[1]:
                            valid_files.append(file_path)
                        else:
                            print("[!]" + str(file_path) + ": " + str(width) + "x" + str(height) + ", excluded.")
                except Exception as e:
                    print(f"[!] Could not open image {filename} due to error: {e}")

        if valid_files:
            file_count_summary = f"{len(valid_files)} | Total files: {len(files)}"

            if len(valid_files) > 3:
                third = len(valid_files) // 3
                selected_files = [
                    random.choice(valid_files[:third]),
                    random.choice(valid_files[third:2*third]),
                    random.choice(valid_files[2*third:])
                ]
            else:
                selected_files = valid_files
            for idx, path in enumerate(selected_files):
                save_to_database(cursor, folder_name, path, idx, file_count_summary)

    conn.commit()
    conn.close()

    end_time = time.time()
    print(f'Duration: {end_time - start_time:.4f} sec')

# Save each valid image file individually
def save_solo_file(cursor, folder_name, file_path, file_index, file_count_summary):
    cursor.execute('''
        INSERT INTO solo_gallery_files (folder_name, file_path, file_index, file_count_summary)
        VALUES (?, ?, ?, ?)
    ''', (folder_name, file_path, file_index, file_count_summary))

# Main function to gather and save images
def get_files_in_directories_solo(root_dir, saftey, min_resolution=(300, 400), db_path='lg_previews.db'):
    start_time = time.time()
    print('[i] Getting files for solo galleries')
    
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
    conn, cursor = setup_database(db_path)

    for foldername, subfolders, filenames in os.walk(root_dir):
        folder_name = os.path.basename(foldername)
        files = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]

        if not folder_name:
            continue

        base_name = folder_name
        suffix = 1

        # Generate a unique name for the folder_name else the result stack.
        while True:
            cursor.execute("SELECT 1 FROM solo_gallery_files WHERE folder_name = ?", (folder_name,))
            if cursor.fetchone():
                folder_name = f"{base_name}_{suffix}"
                suffix += 1
            else:
                break        

        valid_files = []

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in allowed_extensions:
                continue

            file_path = os.path.join(foldername, filename)

            if saftey == '0':
                valid_files.append(file_path)
            else:
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        if width >= min_resolution[0] and height >= min_resolution[1]:
                            valid_files.append(file_path)
                        else:
                            print("[!]" + str(file_path) + ": " + str(width) + "x" + str(height) + ", excluded.")
                except Exception as e:
                    print(f"[!] Could not open image {filename} due to error: {e}")

        if valid_files:
            file_count_summary = f"{len(valid_files)} | Total files: {len(files)}"
            for idx, path in enumerate(valid_files):
                save_solo_file(cursor, folder_name, path, idx, file_count_summary)

    conn.commit()
    conn.close()

    end_time = time.time()
    print(f'Duration: {end_time - start_time:.4f} sec')

def read_all_files_from_db(db_path, table):
    if table == 'solo':
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT folder_name, file_path FROM solo_gallery_files")
        rows = cursor.fetchall()
        conn.close()

    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT folder_name, file_path FROM folder_previews")
        rows = cursor.fetchall()
        conn.close()

    files_dict = {}
    for folder, path in rows:
        files_dict.setdefault(folder, []).append(path)

    return files_dict

def read_thumbnails_from_db(db_path, table):
    if table == 'solo':
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT folder_name, thumbnail_path FROM solo_gallery_files WHERE thumbnail_path IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()

    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT folder_name, thumbnail_path FROM folder_previews")
        rows = cursor.fetchall()
        conn.close()
    
    thumbs_dict = {}
    for folder, path in rows:
        thumbs_dict.setdefault(folder, []).append(path)

    return thumbs_dict

def read_amount_from_db(db_path, table):
    if table == 'solo':
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT folder_name, file_count_summary FROM solo_gallery_files WHERE file_index = 0")
        rows = cursor.fetchall()
        conn.close()
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT folder_name, file_count_summary FROM folder_previews WHERE file_index = 0")
        rows = cursor.fetchall()
        conn.close()

    thumbs_dict = {}
    for folder, path in rows:
        thumbs_dict.setdefault(folder, []).append(path)
    return thumbs_dict

def create_thumbnail(image_path, args, max_width=300, max_height=400):
    try:
        with Image.open(image_path) as img:
            # Check if the image has an alpha channel (RGBA)
            if image_path.lower().endswith('.gif'):
                img = img.copy()

            elif img.mode == 'RGBA':
                # Convert RGBA to RGB (removes alpha channel)
                img = img.convert('RGB')

            elif img.mode == 'LA':
                img = img.convert('L')  # Convert LA to L (grayscale)
            
            elif img.mode == "P" and img.info.get('transparency') is not None:
                # Convert to RGBA to properly handle transparency
                img = img.convert("RGBA")

            elif img.mode == 'P':
                img = img.convert('RGB')  # Convert P mode (palette-based) to RGB
            
            # Get the current dimensions of the image
            width, height = img.size

            # Calculate the scaling factor to fit within both width and height constraints
            scaling_factor = min(max_width / width, max_height / height)

            if scaling_factor < 1:
                # Resize the image while maintaining the aspect ratio
                new_width = int(width * scaling_factor)
                new_height = int(height * scaling_factor)
                img = img.resize((new_width, new_height))
                
            return img
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        if args == '1':
            with open('error_log.txt', 'a') as logWrite:
                logWrite.write(f'{image_path}: {e}\n')
            logWrite.close
        return None

def generate_thumbnails(files_dict3, argsE):
    start_time = time.time()
    thumbnails_dict = {}
    print('[i]Creating thumbs')
    # Iterate over each folder in the files_dict
    for folder_name, file_paths in files_dict3.items():
        folder_thumbnails = {}
        
        # Generate thumbnail for each file
        for file_path in file_paths:
            thumbnail = create_thumbnail(file_path, argsE)
            if thumbnail:
                folder_thumbnails[file_path] = thumbnail
        
        # Store the folder's thumbnails in the new dictionary
        thumbnails_dict[folder_name] = folder_thumbnails
    end_time = time.time()
    time_duration = str(end_time - start_time)
    print(f'Duration: {time_duration:.4} sec')
    return thumbnails_dict

def save_thumbnails_to_directory(thumbnails_dict, argsE, root_dir, db_path, table):
    start_time = time.time()
    print('[i]Saving thumbs and updating DB')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for folder_name, thumbnails in thumbnails_dict.items():
        folder_path = os.path.join(root_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for file_path, thumbnail in thumbnails.items():
            if thumbnail is None:
                continue

            original_filename = os.path.basename(file_path)
            base_name, ext = os.path.splitext(original_filename)
            thumbnail_filename = f"{base_name}_thm{ext}"
            thumbnail_path = os.path.join(folder_path, thumbnail_filename)

            try:
                if ext.lower() in ['.jpg', '.jpeg']:
                    thumbnail.convert('RGB').save(thumbnail_path, 'JPEG')
                else:
                    thumbnail.save(thumbnail_path)

                # Save relative thumbnail path to DB
                rel_thumb_path = os.path.relpath(thumbnail_path, root_dir).replace('\\', '/')
                if table == 'solo':
                    cursor.execute('''
                        UPDATE solo_gallery_files
                        SET thumbnail_path = ?
                        WHERE file_path = ?
                    ''', (rel_thumb_path, file_path))
                else:
                    cursor.execute('''
                        UPDATE folder_previews
                        SET thumbnail_path = ?
                        WHERE file_path = ?
                    ''', (rel_thumb_path, file_path))

            except Exception as e:
                print(f"Error saving thumbnail for {thumbnail_filename}: {e}")
                if argsE == '1':
                    with open('error_log.txt', 'a') as logWrite:
                        logWrite.write(f'{thumbnail_filename}: {e}\n')

    conn.commit()
    conn.close()

    end_time = time.time()
    print(f'Duration: {end_time - start_time:.4f} sec')

def directory_info(files):
    size_dict = {}
    for folder_name, file_paths in files.items():
        try:
            im = Image.open(file_paths[1])
            width, height = im.size
            iSize = str(width) + ' x ' + str(height)
            size_dict[folder_name] = iSize
        except:
            size_dict[folder_name] = 'Unknown'
    return size_dict