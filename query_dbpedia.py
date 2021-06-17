from SPARQLWrapper import SPARQLWrapper, JSON

def query(in_data):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(in_data)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results

if __name__ == "__main__":
    print('Please enter your SPARQL queries:')
