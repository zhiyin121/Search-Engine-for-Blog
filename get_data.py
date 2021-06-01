import os
import html
import re
import pickle
import xml.etree.ElementTree as ET
from lxml import etree
from lxml import etree as ET2


# Clean and rewrite the text data in each file
def clean_data(filepath, filename):
    text = ''
    p1 = re.compile('(&nbsp;| {2,}|�|urlLink|Ã|Â|ï|¿|½|¯|¢)')
    p2 = re.compile('( \, )|(\,(?=[a-zA-Z]))')
    p3 = re.compile('( \. )|(\.(?=[a-zA-Z]))')
    p4 = re.compile('\. com(?=[^a-zA-Z])')
    p5 = re.compile('www\. (?=[a-zA-Z])')
    with open(filepath+filename, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            # uncomment base on need
            #line = p1.sub('', line)
            #line = p2.sub(', ', line)
            #line = p3.sub('. ', line)
            #line = p4.sub('.com', line)
            #line = p5.sub('www.', line)
            text += line
    with open(filepath+filename, 'w', encoding='utf-8') as w:
        w.write(text)


# Pack each instance(a instance = a blog) into a class object
class GroupData():
    def __init__(self, blog_id, user_id, gender, age, industry, astrology, date, post):
        self.blog_id = blog_id
        self.user_id = user_id
        self.gender = gender
        self.age = age
        self.industry = industry
        self.astrology = astrology
        self.date = date
        self.post = post


# Deconstruct the xml file
# Compose each instance based on the filename and content 
# Package it into a class object and add it to a list
def get_data(filepath, filename, index):
    f = open(filepath+filename)
    text = ''
    data_list = []
    try:
        for line in f:
            line = html.unescape(line)
            text += line
    except UnicodeDecodeError:
        print('Error 1', filename)
        
    #print(text)
    #root = ET.fromstring(text)
    parser = ET2.XMLParser(recover=True)
    try:
        root = ET2.fromstring(text, parser=parser)
        #root = tree.getroot()

        info = filename.split('.')
        user_id = info[0]
        gender = info[1]
        age = info[2]
        industry = info[3]
        astrology = info[4]

        
        for child in root:
            blog_id = index
            if child.tag == 'date':
                date = child.text 
            elif child.tag == 'post':
                data_sample = GroupData(blog_id, user_id, gender, age, industry, astrology, date, child.text.strip('\n \t'))
                data_list.append(data_sample)
                index += 1
    except etree.XMLSyntaxError:
        print('Error 2', filename)
    return data_list, index


def get_filename(filepath):
    filename = os.listdir(filepath)
    # Return a list of file name
    return filename


if __name__ == '__main__':
    # Get a data list
    data_lists = []
    filepath = '/Users/tan/OneDrive - xiaozhubaoxian/blog/blogs/'
    filename_list = get_filename(filepath)
    index = 0
    for filename in filename_list:
        #clean_data(filepath, filename)
        data_list, index = get_data('./blogs/', filename, index)
        data_lists += data_list

    # Store the data(class object) list into a pickle file
    with open('./group_data_objects.pickle','wb') as p:
        pickle.dump(data_lists, p)
    
    # Read a pickle file
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Print examples
    for i in data_lists[:30]:
        print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')




'''
# test html and xml parser
f = open('./blogs/3162067.female.24.Education.Cancer.xml')
text = ''
for line in f:
    line = html.unescape(line)
    text += line

#print(text)
#root = ET.fromstring(text)
parser = ET2.XMLParser(recover=True)
root = ET2.fromstring(text, parser=parser)
for child in root:
    print(child.tag, child.text)'''


'''
# test re
text = "i was waiting for my DESTINY.what should i do with myself,tell me o' my heartwhat should i do with myself,tell me....should i fly, with this beautiful nature.or should i play with these winds.should i try to reach the skies,or should i pray to the mother earth.what should i do with myself friendstell me....she talked in such a way,gave me dreams with thousand colours.like i stand in the middle of island,and she shows me all the love she has,my first dream , "
p2 = re.compile('( \, )|(\,(?=[a-zA-Z]))')
p3 = re.compile('( \. )|(\.(?=[a-zA-Z]))')
text = p2.sub(', ', text)
text = p3.sub('. ', text)
print(text)'''
