import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags
from sklearn.metrics import precision_recall_fscore_support

# Download necessary NLTK data files
nltk.download("punkt_tab")
nltk.download("maxent_ne_chunker_tab")
nltk.download("words")
nltk.download("averaged_perceptron_tagger_eng")

def named_entity_recognition(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Perform part-of-speech tagging
    pos_tags = pos_tag(tokens)
    # Perform named entity recognition
    ne_tree = ne_chunk(pos_tags)
    # Convert the tree to IOB format
    iob_tags = tree2conlltags(ne_tree)
    return iob_tags

def evaluate_ner(true_labels, predicted_labels):
    precision, recall, fscore, _ = precision_recall_fscore_support(true_labels, predicted_labels, average='weighted')
    return precision, recall, fscore

# Example usage
text = "Barack Obama was born in Hawaii. He was elected president in 2008."
iob_tags = named_entity_recognition(text)
print(iob_tags)

# Example evaluation (using dummy data for demonstration)
true_labels = ['B-PERSON', 'I-PERSON', 'O', 'O', 'O', 'B-GPE', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
predicted_labels = ['B-PERSON', 'I-PERSON', 'O', 'O', 'O', 'B-GPE', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
precision, recall, fscore = evaluate_ner(true_labels, predicted_labels)
print(f"Precision: {precision}, Recall: {recall}, F-score: {fscore}")