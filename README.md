# Local_gallery
Create preview or full galleries displayed in html.
---

The script creates a preview gallery of every sub folder with images to a html page.
Every sub folder with at least 1 image will be displayed.
If there's more then 3 images the script will choose 1 from the first thirds, 1 from the second and 1 from the third.
You also have the possibility to create galleries for every image in a folder as a separate gallery.
If you choose to create both preview and solo galleries then you can navigate from the preview to the solo galleries.

---

Dependences:
dominate

---

To use the script start it from a terminal with command
Local_gallery_1.0.0.exe [folder path to where you galleries are]

ex py C:\folder\Local_gallery_1.0.0.py C:\galleries

or C:\folder\Local_gallery_1.0.0.exe C:\galleries

Use flag -l 0-2 for what you type of galleries you want. 0 is default.
0 = preview, 1 = solo, 2 = preview and solo. 

ex py C:\folder\Local_gallery_1.0.0.py -l 2 C:\galleries
or C:\folder\Local_gallery_1.0.0.exe -l 2 C:\galleries

Use flag -e to save errors to a log file in the folder that the script runs from.

ex py C:\folder\Local_gallery_1.0.0.py -e C:\galleries
or C:\folder\Local_gallery_1.0.0.exe -e C:\galleries

Use flag -s to switch if extra safety checks should be used or not, 1 is default.
Switching the checks to 0 speed up the gallery build time but can lead to errors.

ex py C:\folder\Local_gallery_1.0.0.py -s 0 C:\galleries
or C:\folder\Local_gallery_1.0.0.exe -s 0 C:\galleries

---

Thumbnails can be adjusted by changing the values in lg_func.py in the create_thumbnail function and lg_style.py under /* Thumbnails Images */.
Style of the html galleries can be modified by changing the lg_style.py file.
Created thumbnails gets saved to the folders thumbsR and thumbsS

---

Supported file formats:
.jpg, .jpeg, .png, .webp, .gif*, .bmp

*only displays the first frame of the gif.

---
Preview
![Pre_163820](https://github.com/user-attachments/assets/013ead00-4727-47aa-b3c2-831a31112dbd)


Solo
![solo_164000](https://github.com/user-attachments/assets/8a89799c-5c92-465f-8f24-ffb1c70b9f82)
