import pickle
from Inv_Index import InvertedIndex
from pro_part1 import WAND_Algo

fname = './Data/sample_documents.pickle'
documents = pickle.load(open(fname,"rb"))

inverted_index = InvertedIndex(documents).get_inverted_index()

query_terms = ["President","New","York"]
top_k = 2

topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)

print('Top-k result = ', topk_result)
print('Evaluation Count = ', full_evaluation_count)
