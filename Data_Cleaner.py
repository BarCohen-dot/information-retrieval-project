import re  # for regular expression operations (e.g., removing URLs, mentions)
import string  # for punctuation removal
from nltk.corpus import stopwords  # to load stopwords for filtering common words
from nltk.stem import PorterStemmer  # for stemming words to their root form
from nltk.tokenize import WhitespaceTokenizer  # for basic whitespace-based tokenization
from Database_Manager import DBService  # for database operations

# ================================================= introduction =======================================================
"""
# Run-in phase No. 2
--------------------

Class for cleaning and preprocessing raw text data from posts.
Performs:
- Lowercasing
- Extracting URLs
- Stopword removal
- Punctuation cleanup
- Stemming
- Token filtering (only alphabetic)
Also includes function to clean all posts from database and update cleaned text.
"""
# ======================================================================================================================

class DataCleaner:

    def __init__(self, language='english'):
        self.stop_words = set(stopwords.words(language))  # Load English stopwords
        self.stemmer = PorterStemmer()  # Initialize stemmer
        self.tokenizer = WhitespaceTokenizer()  # Use whitespace tokenizer

    def extract_urls(self, text):
        """Extracts all URLs from text."""
        return re.findall(r'http\S+|www\S+', text)

    def clean_text(self, text):
        """
        Cleans a given text string by applying standard NLP preprocessing steps:
        - Convert to lowercase
        - Remove links, hashtags, mentions
        - Remove punctuation, digits, emojis
        - Tokenize text
        - Remove stopwords
        - Filter short and non-alphabetic words
        - Apply stemming
        param text: Raw input string
        return: Cleaned and stemmed string
        """
        if not text:
            return ""

        text = text.lower()                                               # Lowercase
        text = re.sub(r'https?://\S+|www\.\S+', '', text)    # Remove URLs
        text = re.sub(r'[@#]\w+', '', text)                  # Remove hashtags and mentions
        text = re.sub(r'\d+', '', text)                      # Remove digits
        text = re.sub(r'[^\x00-\x7F]+', '', text)            # Remove emojis and non-ASCII characters
        text = text.translate(str.maketrans('', '', string.punctuation))   # Remove punctuation
        tokens = self.tokenizer.tokenize(text)                             # Tokenize (assuming whitespace tokenizer)

        cleaned_tokens = [                  # Filter : stopwords, short words (words < 3), non-alphabetic
            self.stemmer.stem(word)
            for word in tokens
            if word not in self.stop_words and word.isalpha() and len(word) > 2
                         ]

        return " ".join(cleaned_tokens)

    def clean_and_store_all_posts(self, db_service):
        """
        Retrieves all posts from database, cleans the text, extracts URLs,
        and updates them in the existing posts table.
        Additional logic:
        - Sets post_url to NULL if empty
        - Converts negative likes to 0
        - Splits post_date into DATE and TIME components (only if column exists)
        - Updates the original 'posts' table with clean_text and extracted_urls
        """
        posts = db_service.fetch_all_posts()
        if not posts:
            print("No posts found in the database.")
            return

        cursor = db_service.connection.cursor()

        cursor.execute("SHOW COLUMNS FROM posts")
        existing_columns = set(row[0] for row in cursor.fetchall())  # Get current column names

        # Force re-creation of clean_text and extracted_urls to guarantee overwrite
        if 'clean_text' in existing_columns:
            cursor.execute("ALTER TABLE posts DROP COLUMN clean_text")
        if 'extracted_urls' in existing_columns:
            cursor.execute("ALTER TABLE posts DROP COLUMN extracted_urls")
        if 'post_date_only' in existing_columns:
            cursor.execute("ALTER TABLE posts DROP COLUMN post_date_only")
        if 'post_time_only' in existing_columns:
            cursor.execute("ALTER TABLE posts DROP COLUMN post_time_only")

        cursor.execute("ALTER TABLE posts ADD COLUMN clean_text TEXT")
        cursor.execute("ALTER TABLE posts ADD COLUMN extracted_urls TEXT")
        cursor.execute("ALTER TABLE posts ADD COLUMN post_date_only DATE")
        cursor.execute("ALTER TABLE posts ADD COLUMN post_time_only TIME")

        for idx, post in enumerate(posts):
            post_id = post['post_id']
            text = post['text']
            post_date_raw = post.get('post_date')
            likes = post.get('likes')
            url = post.get('post_url')

            clean = self.clean_text(text)  # Clean text
            extracted_urls = ", ".join(self.extract_urls(text)) if text else None  # Extract URLs

            if url is not None and (url == '' or url.isspace()):
                url = None  # Normalize empty URL

            if likes is not None and likes < 0:
                likes = 0  # Normalize likes

            date_part = None
            time_part = None
            if post_date_raw:
                try:
                    date_part = post_date_raw.strftime('%Y-%m-%d')
                    time_part = post_date_raw.strftime('%H:%M:%S')
                except Exception as e:
                    print(f"[Warning] Failed to drop column 'post_date': {e}")

            cursor.execute("""
                UPDATE posts
                SET clean_text = %s,
                    extracted_urls = %s,
                    post_url = %s,
                    likes = %s,
                    post_date_only = %s,
                    post_time_only = %s
                WHERE post_id = %s
            """, (clean, extracted_urls, url, likes, date_part, time_part, post_id))
            print(f"✅ Processed post {idx + 1} / {len(posts)}")

        if 'post_date' in existing_columns:
            try:
                cursor.execute("ALTER TABLE posts DROP COLUMN post_date")  # Drop original column
            except Exception as e:
                print(f"[Warning] Failed to drop column 'post_date': {e}")

        db_service.connection.commit()
        cursor.close()
        print("✅ All posts cleaned and updated in 'posts' table with structured date and time.")


# ===================================================== Main ===========================================================

if __name__ == '__main__':  # Run this only when executing the file directly
    import nltk  # For downloading necessary tokenizers and stopwords
    nltk.download('punkt')  # Punkt: tokenizer models used by word_tokenize
    nltk.download('stopwords')  # English stopwords

    cleaner = DataCleaner()  # Create instance of cleaner
    db = DBService(password='Ella3838')  # Connect to the database with password
    db.connect()  # Establish DB connection

    cleaner.clean_and_store_all_posts(db)  # Clean and update all posts in DB

    db.close_connection()  # Close connection to DB
