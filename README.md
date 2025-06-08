# 🔍 Modern Search Engine - Information Retrieval Project

## 📚 Project Description

This is a desktop-based ranked search engine written in **Python**, developed as part of an information retrieval course.
The application allows users to search social media posts using a ranked search method based on TF-IDF.

The application includes:

* A **modern GUI** (with Dark Mode and Light Mode support)
* A **ranked search engine** with TF-IDF logic
* **MySQL**-based post storage and retrieval
* **Inverted index** building for fast term access
* **Data cleaning** tools to preprocess and prepare the dataset

---

## 🗂️ Project Structure

```bash
.
├── data_store/
|    |----- json_posts
|    |----- inverted_index.json
|    |----- post_metadata.json
│── Data_Cleaner.py         # Cleans and preprocesses raw post text
│── Database_Manager.py     # Handles MySQL connection and post queries
│── dataset_2_posts.sql     # SQL script for importing the dataset into MySQL
├── gui.py                      # Main GUI for user interaction (Dark Mode enabled)
├── Inverted_Index.py           # Builds and stores an inverted index for posts
├── Ranked_search.py            # Implements TF-IDF ranking and cosine similarity
├── README.md                   # Project documentation
│──  search_engine_architecture.drawio
```

---

## 🛠️ Technologies Used

* **Python 3.11**
* **Tkinter** – GUI
* **MySQL** – Database
* **Regex (re)** and **time** – Utility modules
* **mysql-connector-python** – For connecting to MySQL

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.11
* MySQL Server
* Install required dependencies:

  ```bash
  pip install mysql-connector-python
  ```

### ▶️ Execution Order

> It is recommended to run the components in the following order:

1. **Database Setup:**

   * Import the dataset manually into your MySQL database:

     ```bash
     mysql -u root -p information_retrieval < dataset_2_posts.sql
     ```

2. **Data Cleaning:** *(Optional)*

   * If raw data exists and needs cleaning, run:

     ```bash
     python data_store/Data_Cleaner.py
     ```

3. **Inverted Index Construction:**

   * Build the index required for search:

     ```bash
     python Inverted_Index.py
     ```

4. **Launch GUI:**

   * Start the main graphical interface:

     ```bash
     python gui.py
     ```

---

## 🧠 Search Algorithm Overview

Implemented with **TF-IDF** (Term Frequency–Inverse Document Frequency):

* `Ranked_search.py` builds term-weight vectors for each post
* Computes **cosine similarity** between the query and post vectors
* Returns top 20 matching results

---

## 💡 Features

* 🟢 Single-word search
* 🟢 View top 20 results with metadata
* 🟢 Toggle between Light Mode and **Dark Mode**
* 🟢 Save results to `.txt`
* 🟢 Load previously saved results
* 🟢 Keyboard support:

  * `Enter` = Run search
  * `ESC` = Exit app

---

## 🔮 Future Enhancements

* Add support for multi-word or phrase-based queries
* Enhance UI responsiveness and accessibility
* \[Optional] Develop a web-based version using Flask
* \[Advanced] Integrate semantic vector search using BERT or Sentence Transformers

---

## 📄 License

This project is part of an academic course in Information Retrieval and is intended for educational use only.
