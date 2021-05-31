import os
import html
import re
import pickle
import xml.etree.ElementTree as ET
from lxml import etree
from lxml import etree as ET2


def clean_data(filepath, filename):
    text = ''
    p1 = re.compile('(&nbsp;| {2,}|�|urlLink|Ã|Â|ï|¿|½|¯|¢)')
    p2 = re.compile('( \, )|(\,(?=[a-zA-Z]))')
    p3 = re.compile('( \. )|(\.(?=[a-zA-Z]))')
    p4 = re.compile('\. com(?=[^a-zA-Z])')
    p5 = re.compile('www\. (?=[a-zA-Z])')
    with open(filepath+filename, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            #line = p1.sub('', line)
            #line = p2.sub(', ', line)
            #line = p3.sub('. ', line)
            #line = p4.sub('.com', line)
            #line = p5.sub('www.', line)
            text += line
    with open(filepath+filename, 'w', encoding='utf-8') as w:
        w.write(text)


class GroupData():
    def __init__(self, gender, age, industry, astrology, date, post):
        self.gender = gender
        self.age = age
        self.industry = industry
        self.astrology = astrology
        self.date = date
        self.post = post


def get_data(filepath, filename):
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
        gender = info[0]
        age = info[1]
        industry = info[2]
        astrology = info[3]

        
        for child in root:
            if child.tag == 'date':
                date = child.text 
            elif child.tag == 'post':
                data_sample = GroupData(gender, age, industry, astrology, date, child.text.strip('\n \t'))
                data_list.append(data_sample)
    except etree.XMLSyntaxError:
        print('Error 2', filename)
    return data_list


def get_filename(filepath):
    filename = os.listdir(filepath)
    # return a list of file name
    return filename


if __name__ == '__main__':
    '''
    data_list = []
    filepath = '/Users/tan/OneDrive - xiaozhubaoxian/blog/blogs/'
    filename_list = get_filename(filepath)
    for filename in filename_list:
        #clean_data(filepath, filename)
        data_list += get_data('./blogs/', filename)

    with open('./group_data_objects.pickle','wb') as p:
        pickle.dump(data_list, p)
    '''
    with open('./group_data_objects.pickle', 'rb') as f:
        data_list = pickle.load(f)

    for i in data_list[:2]:
        print(i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')




'''
# test
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
text = "i was waiting for my DESTINY.what should i do with myself,tell me o' my heartwhat should i do with myself,tell me....should i fly, with this beautiful nature.or should i play with these winds.should i try to reach the skies,or should i pray to the mother earth.what should i do with myself friendstell me....she talked in such a way,gave me dreams with thousand colours.like i stand in the middle of island,and she shows me all the love she has,my first dream , "
p2 = re.compile('( \, )|(\,(?=[a-zA-Z]))')
p3 = re.compile('( \. )|(\.(?=[a-zA-Z]))')
text = p2.sub(', ', text)
text = p3.sub('. ', text)
print(text)'''
