import json  # for reading JSON files
import os  # for checking file existence

from nltk.stem import PorterStemmer  # for stemming query terms
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords  # for removing common stopwords

import re  # for regex-based cleanup
import string  # for removing punctuation
import math  # for improved IDF calculation

# ================================================= introduction ======================================================
"""
# Run-in phase No. 4
--------------------

Class for searching terms in the inverted index.
Includes:
- Preprocessing queries
- Retrieving post IDs using inverted_index.json
- Optionally showing post metadata
Supports:
- Search for a single word only
- Displays up to 20 posts
- Graceful exit with 'exit'
- Ranking results (by TF-IDF)
"""
# =====================================================================================================================

class SearchEngine:

    def __init__(self, index_path='data_store/inverted_index.json', metadata_path='data_store/post_metadata.json'):
        # Load the inverted index and metadata files
        self.inverted_index = self._load_json(index_path)
        self.post_metadata = self._load_json(metadata_path)
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer = WhitespaceTokenizer()
        self.debug = False  # Debug mode to enable extra logging

    def _load_json(self, path):
        # Load JSON data from the given file path
        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            return {}
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def preprocess_query(self, Query):
        """ Tokenizes and stems the query using same logic used in index building. """
        Query = Query.lower()
        Query = re.sub(r'[@#]\w+', '', Query)  # remove mentions and hashtags
        Query = Query.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        tokens = self.tokenizer.tokenize(Query)  # tokenize on whitespace

        # Apply stemming and stopword filtering
        return [self.stemmer.stem(word) for word in tokens if word.isalpha() and word not in self.stop_words]

    def search(self, Query):
        """ Returns a ranked list of up to 20 matching post IDs for the query. """
        terms = self.preprocess_query(Query)
        if not terms:
            print("⚠️ No valid term in the query after preprocessing.")
            return []

        term = terms[0]  # Only one term allowed for this search
        print(f"🔍 Searching for term: {term}")

        scores = {}  # dictionary to hold tf-idf scores for each post

        if term not in self.inverted_index:
            print(f"❗ Term '{term}' not found in index.")
            return []

        post_list = self.inverted_index[term]['post_ids']  # list of post IDs where term appears
        df = self.inverted_index[term]['df']  # document frequency
        total_docs = len(self.post_metadata)
        idf = math.log(1 + total_docs / df) if df else 0  # improved IDF calculation

        for PID in post_list:
            post_file = f'data_store/json_posts/post_{PID}.json'
            if os.path.exists(post_file):
                with open(post_file, 'r', encoding='utf-8') as file:
                    freqs = json.load(file)
                tf = freqs.get(term, 0)  # term frequency in this post
                tfidf = tf * idf  # basic tf-idf score
                if self.debug:    # for debugging
                    print(f"[DEBUG] Post: {PID} | TF: {tf} | IDF: {idf:.4f} | TF-IDF: {tfidf:.4f}")
                scores[PID] = scores.get(PID, 0) + tfidf
            else:
                print(f"⚠️ JSON file missing for post {PID}. Skipping.")

        # sort posts by their tf-idf score in descending order
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        print("\n🏆 Top matching posts:")
        for PID, score in ranked[:20]:
            print(f"Post ID: {PID} | Score: {score:.4f}")

        return [PID for PID, _ in ranked[:20]]  # return top 20 post IDs

    def show_post_info(self, post_id):
        """ Prints metadata for a given post ID. """
        if post_id in self.post_metadata:
            data = self.post_metadata[post_id]
            print(f"\n📄 Post ID: {post_id}")
            for k, v in data.items():
                print(f"{k}: {v}")
        else:
            print(f"⚠️ Post ID {post_id} not found in metadata.")


# ===================================================== Main ==========================================================

if __name__ == '__main__':
    import nltk
    nltk.download('punkt')  # download tokenizer
    nltk.download('stopwords')  # download stopword list

    engine = SearchEngine()
    while True:
        query = input("\nEnter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("\n👋 Search canceled by user. Bye!")
            break

        if not query:
            continue

        matched_posts = engine.search(query)

        if not matched_posts:
            print("❌ No results found.")
        else:
            print(f"\n✅ Found {len(matched_posts)} matching posts.")
            for pid in matched_posts:
                engine.show_post_info(pid)
