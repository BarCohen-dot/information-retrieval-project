import mysql.connector  # for connecting to MySQL databases from Python
import os               # for file path handling (like checking existence or joining paths)
import subprocess       # for running shell commands like executing external mysql commands

# ================================================= introduction =======================================================
"""
# Run-in phase No. 1
--------------------

Class for managing MySQL database connection and operations.
Handles connection, fetching posts, fetching post by ID, and loading SQL scripts.
"""
# ======================================================================================================================

class DBService:

    def __init__(self, host='localhost', user='root', password='Ella3838', database='information_retrieval'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establishes connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            print("✅ Connected successfully to the database.")
        except mysql.connector.Error as err:
            print(f"❌ Connection error: {err}")

    def fetch_all_posts(self):  # ** for Data_Cleaner Class **
        """Fetches all posts from the database."""
        if not self.connection:
            print("🔌 No active database connection.")
            return []

        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT post_id, text, post_date, likes, post_url FROM posts"
        cursor.execute(query)
        posts = cursor.fetchall()
        cursor.close()
        return posts

    def fetch_all_posts_for_indexing(self):  # ** for Inverted_Index Class **
        """
        Returns a list of posts including all necessary fields for inverted index building.
        Uses post_date_only instead of removed post_date.
        """
        if not self.connection:
            print("No active database connection.")
            return []

        cursor = self.connection.cursor(dictionary=True)
        query = """
                SELECT post_id, clean_text, likes, comment_count, post_date_only
                FROM posts;
                """

        cursor.execute(query)
        posts = cursor.fetchall()
        cursor.close()
        return posts

    def fetch_post_by_id(self, post_id):
        """Fetches a post by its ID."""
        if not self.connection:
            print("🔌 No active database connection.")
            return None

        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM posts WHERE post_id = %s"
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()
        cursor.close()
        return post

    def run_sql_script(self, filepath):
        """
        Loads a SQL script into the database using system-level mysql command.
        to dataset_2_posts.sql.
        :param filepath: path to the .sql file
        """
        if not os.path.isfile(filepath):
            print(f"❌ File not found: {filepath}")
            return

        command = f'mysql -u {self.user} -p{self.password} {self.database} < \"{filepath}\"'
        try:
            subprocess.run(command, shell=True, check=True)
            print("✅ SQL script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run SQL script: {e}")

    def close_connection(self):
        """Closes the connection to the database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Database connection closed.")

# ===================================================== Main ===========================================================

if __name__ == '__main__':
    db = DBService(password='Ella3838')  # Update with your password if needed
    db.connect()

    # Run SQL script
    sql_file_path = os.path.join(os.getcwd(), "dataset_2_posts.sql")
    db.run_sql_script(sql_file_path)
    db.close_connection()