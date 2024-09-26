# Install necessary packages
#!pip install wordcloud
#!pip install fileupload
#!pip install ipywidgets
#!jupyter nbextension install --py --user fileupload
#!jupyter nbextension enable --py fileupload

# Import necessary libraries
import wordcloud
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
import sys

# Function to calculate word frequencies
def calculate_frequencies(file_contents):
    # List of punctuations and uninteresting words
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", 
                           "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", 
                           "its", "they", "them", "their", "what", "which", "who", "whom", "this", "that", "am", 
                           "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", 
                           "but", "at", "by", "with", "from", "here", "when", "where", "how", "all", "any", "both", 
                           "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]
    
    # Dictionary to hold word frequencies
    d = {}
    words = file_contents.split()
    
    for word in words:
        word = ''.join([char for char in word if char not in punctuations])  # Remove punctuations
        if word.lower() not in uninteresting_words and word.isalpha():  # Check if the word is interesting
            if word.lower() in d:
                d[word.lower()] += 1
            else:
                d[word.lower()] = 1
    
    # Generate word cloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(d)
    return cloud.to_array()

# File uploader widget
def _upload():
    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(filename, len(decoded.read()) / 2 ** 10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)

# Call the upload widget
_upload()

# Generate and display the word cloud
try:
    myimage = calculate_frequencies(file_contents)
    plt.imshow(myimage, interpolation='nearest')
    plt.axis('off')
    plt.show()
except NameError:
    print("Please upload a file to generate the word cloud.")
