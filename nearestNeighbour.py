import sys
import os
import math

FOLDER = "preprocessedData/"
NUM_NEIGHBOURS = 99


class InvertedIndex:

    def __init__(self):
        self.total_documents = 0
        # term: document_frequency
        self.df = {}
        # doc_id: {term: frequency}
        self.tf = {}
        # doc_id: magnitude
        self.magnitude = {}
        # doc_id: max_frequency
        self.max_freq = {}

    def addData(self, doc_id, term):
        if doc_id not in self.tf:
            self.tf[doc_id] = {}

        # Update term frequency of term
        if term not in self.tf[doc_id]:
            self.tf[doc_id][term] = 1

            # Update number of docs term appears in
            if term not in self.df:
                self.df[term] = 1
            else:
                self.df[term] += 1
        else:
            self.tf[doc_id][term] += 1

        # Update max frequency for each document
        if doc_id not in self.max_freq:
            self.max_freq[doc_id] = -999

        if self.tf[doc_id][term] > self.max_freq[doc_id]:
            self.max_freq[doc_id] = self.tf[doc_id][term]

        self.total_documents = len(self.tf)

    def getSimilarDocuments(self, query_tokens):
        """Get all documents with at least one word in token"""
        similar_documents = []
        for doc_id, term_frequency_data in self.tf.items():
            for token in query_tokens:
                if token in term_frequency_data:
                    similar_documents.append(doc_id)
                    break

        return similar_documents

    def getWeightVector(self, tokens, doc_id):
        """Given terms in query, get the document weight vector"""
        weights = []

        for token in tokens:
            weight = self._getWeight(token, doc_id)
            weights.append(weight)

        return weights

    def getQueryWeightVector(self, tokens):
        """Get the query weight vector"""
        weights = []

        # Create frequency table for query (like new document)
        term_frequency_data = {}
        for token in tokens:
            if token not in term_frequency_data:
                term_frequency_data[token] = 1
            else:
                term_frequency_data[token] += 1

        for token in tokens:
            idf = self.getInverseDocFreq(token)

            tf = -1
            if token not in term_frequency_data:
                tf = 0
            else:
                tf = term_frequency_data[token]

            weight = tf * idf
            weights.append(weight)

        return weights

    def getMagnitude(self, doc_id):
        """Get length/magnitude of whole document vector"""
        if doc_id not in self.magnitude:
            squared_sum = 0

            for term, frequency in self.tf[doc_id].items():
                weight = self._getWeight(term, doc_id)
                weight_squared = weight * weight

                squared_sum += weight_squared

            doc_magnitude = math.sqrt(squared_sum)

            self.magnitude[doc_id] = doc_magnitude

        return self.magnitude[doc_id]

    def getInverseDocFreq(self, term):
        if term in self.df:
            return math.log10(self.total_documents / self.df[term])
        else:
            return 0

    def _getWeight(self, term, doc_id):
        term_freq = 0
        if term in self.tf[doc_id]:
            term_freq = self.tf[doc_id][term]

        idf = self.getInverseDocFreq(term)
        return term_freq * idf


def main():
    filename_list = _getFilenameList(FOLDER)

    # Vectors counting number correct for increasing number of neighbours
    num_correct = [0 for _ in range(1, NUM_NEIGHBOURS + 1, 2)]
    male_correct = [0 for _ in range(1, NUM_NEIGHBOURS + 1, 2)]
    female_correct = [0 for _ in range(1, NUM_NEIGHBOURS + 1, 2)]

    # print(filename_list)

    documents = {}
    for filename in filename_list:
        file = open(FOLDER + filename, 'r')
        file_text = file.read()
        documents[filename] = file_text

    for index in range(0, 146):
        # Test files this round
        male_filename = "male" + str(index) + ".txt"
        female_filename = "female" + str(index) + ".txt"

        train_list = filename_list.copy()
        train_list.remove(male_filename)
        train_list.remove(female_filename)

        inverted_index = InvertedIndex()

        for training_file in train_list:
            train_text = ""
            train_text = documents[training_file]

            inverted_index = indexDocument(
                train_text, training_file, inverted_index)

        male_text = documents[male_filename]

        relevant_documents = retrieveDocuments(male_text, inverted_index)

        predictions = getPredictions(
            relevant_documents, inverted_index)

        for index, prediction in enumerate(predictions):
            if prediction == "male":
                male_correct[index] += 1
                num_correct[index] += 1

        female_text = documents[female_filename]

        relevant_documents = retrieveDocuments(female_text, inverted_index)

        predictions = getPredictions(
            relevant_documents, inverted_index)

        for index, prediction in enumerate(predictions):
            if prediction == "female":
                female_correct[index] += 1
                num_correct[index] += 1

    for index, num_correct_value in enumerate(num_correct):
        num_neighbors = (index * 2) + 1
        print("Number of Neighbours: ", num_neighbors)
        print("Accuracy: ", num_correct[index] / (146 * 2))
        print("Female Accuracy: ", female_correct[index] / 146)
        print("Male Accuracy: ", male_correct[index] / 146)


def indexDocument(text, doc_id, inverted_index):
    for token in text.split():
        inverted_index.addData(doc_id, token)

    return inverted_index


def retrieveDocuments(query, inverted_index):
    query_tokens = query.split()

    # Ignore query_id as part of query tokens
    query_weight_vector = inverted_index.getQueryWeightVector(query_tokens)

    # Get set of documents that include at least one word from query
    similar_documents = inverted_index.getSimilarDocuments(query_tokens)

    relevant_documents = {}
    for doc_id in similar_documents:
        doc_weight_vector = inverted_index.getWeightVector(
            query_tokens, doc_id)

        dot_product = _getDotProduct(query_weight_vector, doc_weight_vector)

        doc_magnitude = inverted_index.getMagnitude(doc_id)

        query_magnitude = math.sqrt(sum(i * i for i in query_weight_vector))

        similarity_score = dot_product / \
            (float(doc_magnitude) * query_magnitude)

        relevant_documents[doc_id] = similarity_score

    return relevant_documents


def getPredictions(relevant_documents, inverted_index):
    sorted_results = sorted(relevant_documents.items(),
                            key=lambda kv: kv[1], reverse=True)

    predictions = []

    num_male = 0
    num_female = 0

    count = 0

    for doc_id, similarity_score in sorted_results:
        if count % 2 == 1:
            if num_male > num_female:
                predictions.append("male")
            else:
                predictions.append("female")

        if count == NUM_NEIGHBOURS:
            break

        if "female" in str(doc_id):
            num_female += 1
        elif "male" in str(doc_id):
            num_male += 1
        else:
            print("Invalid document name")

        count += 1

    return predictions


def _getDotProduct(a, b):
    return sum(i * j for i, j in zip(a, b))


def _getFilenameList(directory_string):
    file_list = []
    for file in os.listdir(directory_string):
        filename = os.fsdecode(file)

        file_list.append(filename)

    return file_list


if __name__ == "__main__":
    main()
