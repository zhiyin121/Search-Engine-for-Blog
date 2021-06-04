# Search-Engine-for-Blog

## Objectives
* A statistical and neural network based search engine for [Blog Corpus](https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm)
* Returns contextually similar results by adding semantically and contextually relevant words
* Sensitive to the named entities, the negative forms of adjectives through linguistic settings

## Usage
* Download the whole package
* Download the [Blog Corpus](https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm), unzip it and place it in the package file path
* Download the Pre-loaded [documents](https://xiaozhubaoxian-my.sharepoint.com/:u:/g/personal/tan_ms_hellseed_eu/ESlEak6Z_HlAqr3uEH17O6YB3gUdpbTeqLDxXNxV_PYhKQ?e=VxFPmI), unzip it and place it in the package file path
* Run the code in the package file location
```
  -> python main.py
```

## Example
* Enter a query
```
  -> Query example:
     #1 New York           --- (sensitive to named entities)
     #2 I'm not happy      --- (understand adjective phrases modified by 'not')
     #3 apple slow         --- (ambiguity)
     #4 apple pie          --- (ambiguity)
     #5 Americam           --- (auto correct typo)

  -> What do you search for:
     New York
```
* Output
```
  -> Loading...
  -> Ranking...
  -> Soon to return results...
  
  -> 354351 1499735 female 24 indUnk Pisces 01,August,2004 before new york 
     208066 3586075 male 46 indUnk Virgo 08,July,2004 New York   urlLink 
     64234 946952 female 25 Education Leo 04,August,2004 New York as told by ME   Here's the  urlLink photojournal . Enjoy! 
     394008 2420099 male 25 Telecommunications Pisces 09,March,2004 This is the weather page for the part of New York I will be in. 
     72249 3165287 male 17 Student Aquarius 20,June,2004 DAMN!!! I MISS NEW YORK...:-(
    ...
```


