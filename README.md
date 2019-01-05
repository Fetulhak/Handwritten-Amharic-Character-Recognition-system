Amharic Handwritten character recognition system using convolutional neural net.


Pre-requisite 
Install Python3,opencv,numpy,sklearn,keras


This script works for two purpose
****************************************** 
1. For the saver folder it will save handwritten images to a given destination folder
run it by the command 
python upload_handler.py in cmd opened on the saver folder itself
then on your browser copy and paste http://localhost:8000/dropzone.html
on the drag and drop put your image and will be saved to destination folder.


************************************************
2. The second part of this script which is the main folder HRACRS text generate will be run by the command
python -m http.server --cgi 5000
it will be used to process the stored handwritten image and generate an editable text
then on your browser copy and paste http://localhost:5000/index.html
on your browser you will see the preprocess, the recognize and text generate buttons with their specific operations 

you can process the uploaded image by clicking the preprocess button and you will get the out put in the given destination folder

by clicking the recognize button you will get the converted text output in the text area field of the browser by clicking the generate text button

***********************************************
the END
