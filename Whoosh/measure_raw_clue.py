from whoosh import index, scoring
from whoosh.qparser import QueryParser
from tqdm import tqdm
from math import log
import sys

directory = sys.argv[1]

# Open the index
index_path = f'{directory}/Index'
ix = index.open_dir(index_path)

def ndcg_at_k(relevance_list, k):
    # Calculate DCG (Discounted Cumulative Gain)
    dcg = relevance_list[0] + sum(rel / log(i + 2, 2) for i, rel in enumerate(relevance_list[1:k]))

    # Calculate IDCG (Ideal Discounted Cumulative Gain)
    idcg = sum(rel / log(i + 2, 2) for i, rel in enumerate(sorted(relevance_list, reverse=True)[:k]))

    # Calculate NDCG
    ndcg = dcg / idcg if idcg > 0 else 0
    return ndcg

def mrr_at_k(rank_list, k):
    # Find the position of the first correct answer
    for i, rank in enumerate(rank_list[:k]):
        if rank == 1:  # Assuming 1 represents a correct result
            return 1 / (i + 1)
    return 0

def evaluate_jeopardy_system(questions_file):
    # Initialize metrics
    total_questions = 0
    correct_predictions = 0
    ndcg_values = []
    mrr_values = []

    # Open a file for writing QA information
    with open(f'./{directory}/results_raw_clue.txt', "w", encoding="utf-8") as output_file:
        with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
            # Process Jeopardy questions
            with open(questions_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i in tqdm(range(0, len(lines), 4), desc="Processing Questions", unit=" question"):
                    category = lines[i].strip()
                    clue = lines[i + 1].strip()
                    answer = lines[i + 2].strip()

                    # Search for the answer in the index
                    query_str = clue
                    query = QueryParser("content", ix.schema).parse(query_str)
                    results = searcher.search(query, limit=1)

                    # Write CATEGORY, CLUE, ANSWER, and NEWLINE to the file
                    output_file.write(f"\nCATEGORY: {category}\nCLUE: {clue}\nANSWER: {answer}\nRESULTS: {[result['title'] for result in results]}\n")

                    if results and results[0]['title'].lower() == answer.lower():
                        # If the answer is correct, add a new line stating it's correct
                        output_file.write("PRECISION AT 1: CORRECT\n")
                        correct_predictions += 1
                    else:
                        # If the answer is incorrect, add a new line stating it's incorrect
                        output_file.write("PRECISION AT 1: INCORRECT\n")

                    # Calculate relevance for NDCG
                    relevance_list = [1 if result['title'].lower() == answer.lower() else 0 for result in results]
                    if results:
                        ndcg_values.append(ndcg_at_k(relevance_list, 10))
                    else:
                        ndcg_values.append(0)

                    # Calculate rank for MRR
                    rank_list = [1 if result['title'].lower() == answer.lower() else 0 for result in results]
                    if results:
                        mrr_values.append(mrr_at_k(rank_list, 10))
                    else:
                        mrr_values.append(0)

                    if any(result['title'].lower() == answer.lower() for result in results):
                        output_file.write("CONTAINS RELEVANT ANSWER: YES\n")
                    else:
                        output_file.write("CONTAINS RELEVANT ANSWER: NO\n")

                    total_questions += 1

    # Calculate Precision at 1 (P@1)
    precision_at_1 = correct_predictions / total_questions if total_questions > 0 else 0

    # Calculate average NDCG and MRR
    average_ndcg = sum(ndcg_values) / len(ndcg_values) if ndcg_values else 0
    average_mrr = sum(mrr_values) / len(mrr_values) if mrr_values else 0

    print(f"\nTotal Questions: {total_questions}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Precision at 1 (P@1): {precision_at_1}")
    print(f"Average NDCG at 10: {average_ndcg}")
    print(f"Average MRR at 10: {average_mrr}")

# Example usage
questions_file_path = "../DataSets/questions.txt"
evaluate_jeopardy_system(questions_file_path)
