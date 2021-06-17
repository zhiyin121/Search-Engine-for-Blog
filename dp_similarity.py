from sentence_transformers import SentenceTransformer, util

class SentenceTransformers:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
        return

    def get_scores(self, query, documents):  # query = [''], documents = ['doc1','doc2',...]
        #Compute embedding for both lists
        embeddings_q = self.model.encode(query, convert_to_tensor=True)
        embeddings_ds = self.model.encode(documents, convert_to_tensor=True)
        #print(embeddings_q.shape)
        #print(embeddings_ds.shape)
        #Compute cosine-similarits
        cosine_scores = util.pytorch_cos_sim(embeddings_q, embeddings_ds)
        #print(cosine_scores.shape)
        # Output the pairs with their score
        #for i in range(len(documents)):
            #print("{} \t\t {} \t\t Score: {:.4f}".format(query[0], documents[i], cosine_scores[0][i]))

        return cosine_scores[0]

if __name__ == '__main__':
    query = ['The cat sits outside']
    documents = ['The dog plays in the garden',
                'A woman watches TV',
                'The new movie is so great']
                
    score = SentenceTransformers()
    result = score.get_scores(query, documents)
    #print(type(result))
