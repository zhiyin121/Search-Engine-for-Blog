# Search-Engine-for-Blog

## Objectives
* A statistical and neural network based search engine for [Blog Corpus](https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm).
* It returns contextually similar results by adding semantically and contextually relevant words. It is sensitive to the named entities, the negative forms of adjectives through linguistic settings.

## Usage
* Download the whole package
* Download the [Blog Corpus](https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm), unzip it and place it in the package file path
* Download the Pre-loaded [documents](), unzip it and place it in the package file path
* Run the code in the package file location
```python
  -> python main.py
```
* Enter a query
```python
  #Query example:

    #1 New York           --- (Sensitive to named entities)
    #2 I'm not happy      --- (understand adjective phrases modified by 'not')
    #3 apple slow         --- (ambiguity)
    #4 apple pie          --- (ambiguity)

  # What do you search for:
  New York
```
* Output
```python
  -> Lodaing...
  -> Ranking...
```


### Example
