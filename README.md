# Jeopardy Question Answering System

## Overview
This project simulates IBM Watson's Jeopardy challenge by processing and answering Jeopardy-style questions. 

We have tested both state-of-the-art Information Retrival systems in 2 different programs and compared them in our documentation
- The folder **Lucerne** uses Apache Lucene, a high-performance, full-featured text search engine library written in Java, as its Information Retrieval (IR) backbone, written in java and yields better results and can be run as a trial as it is faster

- in **Whoosh** can be found the other IR system written in python, contains slightly more informationand was more tested but it runs much slower.



## How to Build and Run the Application
- Lucerne, java
	- Indexing Wikipedia Pages:
		- Run **Indexer.java** first to build the index
		- The index is stored in the _Jeopardy/src/main/resources/index_ directory.

	- Answering Questions
		- After indexing is complete, run **Watson.java** to start processing questions.
		- The application reads questions from _Jeopardy/src/main/resources/questions.txt_, searches for answers using the built index, and evaluates the answers based on the expected results.
		- Performance metrics and error analysis are displayed in the console.



## Features
- **Indexing**: Builds an index from a collection of Wikipedia pages, with each page treated as a separate document.
- **Question Processing**: Parses and answers questions from a provided file, comparing the system's answers with the correct answers.
- **Performance Metrics**: Evaluates the system's performance using Precision at 1 (P@1) and Mean Reciprocal Rank (MRR).
- **Error Analysis**: Provides a detailed analysis of the system's correct and incorrect answers.


## Prerequisites
- Java JDK 8 or higher
- Apache Lucene (included in the project's dependencies)
- The project's source files, including Indexer.java and Watson.java


