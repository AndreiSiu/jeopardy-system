import subprocess

print('\n\nResults for using the improved indexer by using the entire clue as query string\nResults for each question can be found in the folder of the indexer variant')
subprocess.run(["python", "./measure_raw_clue.py", "./improved_indexer"])

print('\n\nResults for using the naive indexer by using the entire clue as query string\nResults for each question can be found in the folder of the indexer variant')
subprocess.run(["python", "./measure_raw_clue.py", "./naive_indexer"])

print('\n\nResults for using the improved indexer by using keywords from the clue as query string\nResults for each question can be found in the folder of the indexer variant')
subprocess.run(["python", "./measure_keywords_clue.py", "./improved_indexer"])

print('\n\nResults for using the naive indexer by using keywords from the clue as string\nResults for each question can be found in the folder of the indexer variant')
subprocess.run(["python", "./measure_keywords_clue.py", "./naive_indexer"])