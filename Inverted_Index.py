import os                                       # for file system operations
from collections import defaultdict, Counter    # for frequency counting and efficient dictionaries
import json                                     # for saving inverted index and metadata to files
from nltk.tokenize import WhitespaceTokenizer   # basic tokenization by spaces
from Database_Manager import DBService          # custom DB connector

# ================================================= Introduction =======================================================
"""
# Run-in phase No. 3
--------------------

Class for efficiently building an inverted index from pre-cleaned text data stored in MySQL.

This class performs:
- Basic tokenization of already cleaned posts (assuming prior preprocessing).
- Construction of a global inverted index structure, including:
  - Document frequency (df) of each term.
  - Total term frequency (tf_total) across all documents.
  - List of post occurrences per term.
- Extraction of per-post metadata, including:
  - The most frequent term (max_tf_term) and its frequency (max_tf).
  - Total number of terms (length).
  - Additional metrics (likes, comments, date).
- Output of the inverted index and metadata to structured JSON files for further use.

All resulting JSON files are saved under the directory: 'data_store/json_posts'.
"""
# ======================================================================================================================

class InvertedIndexBuilder:

    def __init__(self):
        self.tokenizer = WhitespaceTokenizer()  # Only tokenize since data is already cleaned

    def tokenize_text(self, text):
        """Tokenizes cleaned text."""
        return self.tokenizer.tokenize(text) if text else []

    def build_inverted_index(self, db_service):
        posts = db_service.fetch_all_posts_for_indexing()
        if not posts:
            print("No posts found in the database.")
            return

        inverted_index = defaultdict(lambda: {'df': 0, 'tf_total': 0, 'post_ids': []})
        post_metadata = {}

        os.makedirs("data_store/json_posts", exist_ok=True)

        print(f"🔁 Starting to process {len(posts)} posts...")

        for idx, post in enumerate(posts):
            post_id = str(post['post_id'])
            text = post.get('clean_text', '')
            tokens = self.tokenize_text(text)

            if not tokens:
                continue

            freq = Counter(tokens)
            length = sum(freq.values())
            max_tf_term = max(freq, key=freq.get)
            max_tf = freq[max_tf_term]

            post_metadata[post_id] = {
                'max_tf_term': max_tf_term,
                'max_tf': max_tf,
                'length': length,
                'likes': post.get('likes'),
                'comments': post.get('comment_count'),
                'date': str(post.get('post_date_only')) if post.get('post_date_only') else None
            }

            for term, tf in freq.items():
                inverted_index[term]['tf_total'] += tf
                if post_id not in inverted_index[term]['post_ids']:
                    inverted_index[term]['df'] += 1
                    inverted_index[term]['post_ids'].append(post_id)

            with open(f'data_store/json_posts/post_{post_id}.json', 'w', encoding='utf-8') as f:
                json.dump(freq, f, ensure_ascii=False, indent=2)

            print(f"✅ Processed post {idx + 1} / {len(posts)} (ID: {post_id})")

        with open('data_store/inverted_index.json', 'w', encoding='utf-8') as f:
            json.dump(inverted_index, f, ensure_ascii=False, indent=2)

        with open('data_store/post_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(post_metadata, f, ensure_ascii=False, indent=2)

        print("✅ Inverted index and metadata built and saved successfully.")

# ===================================================== Main ===========================================================

if __name__ == '__main__':
    indexer = InvertedIndexBuilder()
    db = DBService(password='Ella3838')
    db.connect()

    indexer.build_inverted_index(db)

    db.close_connection()
