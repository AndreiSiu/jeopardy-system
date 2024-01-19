import subprocess
import sys

if len(sys.argv) < 3:
    print("Please provide following command line parameters:\n1. True if you want to run the first indexer; False if you do no want\n2. True if you want to run the second indexer; False if you do not want")
else:
    # Should the naive variant of the indexer run (naive_indexer)
    should_run_naive_indexer = sys.argv[1]

    if should_run_naive_indexer == 'True':
        subprocess.run(["python", "./naive_indexer/indexer.py"])

    # Should the improved variant of the indexer run (improved_indexer)
    should_run_improved_indexer = sys.argv[2]

    if should_run_improved_indexer == 'True':
        subprocess.run(["python", "./improved_indexer/indexer.py"])