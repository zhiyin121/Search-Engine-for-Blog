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
```


#### example 1
```  
  -> What do you search for:
  ----input----
     New York

  -> Loading...
  -> Ranking...
  -> Ready to return results...

  ----return result----
  -> 354351 1499735 female 24 indUnk Pisces 01,August,2004 before new york 
     208066 3586075 male 46 indUnk Virgo 08,July,2004 New York   urlLink 
     64234 946952 female 25 Education Leo 04,August,2004 New York as told by ME   Here's the  urlLink photojournal . Enjoy! 
     394008 2420099 male 25 Telecommunications Pisces 09,March,2004 This is the weather page for the part of New York I will be in. 
     72249 3165287 male 17 Student Aquarius 20,June,2004 DAMN!!! I MISS NEW YORK...:-(
    ...
```

#### example 2
```
  -> What do you search for:
  ----input----
    childerm

  -> Loading...
  -> Do you mean "childern"?
  -> Except the change?(enter:y/n)  |  Additional options(enter:add)

  ----input----
     add

  -> {0: ['children'], 1: ['childre']}
     choose one candidates or keep the original?(enter:number/i)

  ----input----
      1

  ----return result----
  -> Ranking...
  -> Ready to return results...
  -> 256402 1524664 female 23 Law Capricorn 22,May,2004...
     252193 2462056 male 15 Student Leo 10,July,2004...
     ...
```

