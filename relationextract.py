import nltk
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk import tree2conlltags

# Download necessary NLTK data files
nltk.download("punkt_tab")
nltk.download("maxent_ne_chunker_tab")
nltk.download("words")
nltk.download("averaged_perceptron_tagger_eng")

# Define a function to extract entities and relationships
def extract_relationships(text):
    sentences = sent_tokenize(text)
    relationships = []

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        chunks = ne_chunk(pos_tags)
        iob_tags = tree2conlltags(chunks)

        # Extract named entities
        entities = []
        for word, pos, chunk in iob_tags:
            if chunk != "O":
                entities.append((word, chunk))

        # Extract relationships based on POS tags
        for i in range(len(pos_tags)):
            if pos_tags[i][1] == "VBZ":  # Verb, 3rd person singular present
                subject = None
                obj = None
                for j in range(i):
                    if pos_tags[j][1] in ("NNP", "NN"):
                        subject = pos_tags[j][0]
                for k in range(i + 1, len(pos_tags)):
                    if pos_tags[k][1] in ("NNP", "NN"):
                        obj = pos_tags[k][0]
                if subject and obj:
                    relationships.append((subject, pos_tags[i][0], obj))

    return relationships

# Define a function to validate extracted relationships against ground truth
def validate_relationships(extracted, ground_truth):
    correct = 0
    for rel in extracted:
        if rel in ground_truth:
            correct += 1
    accuracy = correct / len(ground_truth) if ground_truth else 0
    return accuracy

# Example usage
if __name__ == "__main__":
    resume_text = """
    John Doe is a software engineer at Google. He works on developing scalable web applications.
    Jane Smith is a data scientist at Microsoft. She specializes in machine learning and data analysis.
    """

    ground_truth = [
        ("John Doe", "is", "software engineer"),
        ("Jane Smith", "is", "data scientist"),
    ]

    extracted_relationships = extract_relationships(resume_text)
    print("Extracted Relationships:", extracted_relationships)

    accuracy = validate_relationships(extracted_relationships, ground_truth)
    print("Validation Accuracy:", accuracy)