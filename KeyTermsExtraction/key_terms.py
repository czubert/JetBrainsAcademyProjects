import nltk
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation


class KeyTermsExtractor:
    def __init__(self, file_path):
        # Initialize the set of filter items including punctuation and stopwords
        self.filter_items = set(punctuation) | set(stopwords.words('english'))
        # Store the file path
        self.file_path = file_path
        # Lists to store titles and stories
        self.titles = list()
        self.stories = list()  # noun tokens, joined in str: documents for calculating TF-IDF
        # Dictionary to store keywords and their TF-IDF scores
        self.key_words = self.calculate_tf_idf()

    def parse_xml(self):
        # Parse XML file and get the root element
        root = etree.parse(self.file_path).getroot()
        # Iterate through each item in the XML
        for item in root[0]:
            # Extract title and story from XML item
            title, story = [item.find(f'value[@name="{tag}"]').text for tag in ("head", "text")]
            # Add title to titles list
            self.titles.append(title)
            # Process story and add to stories list
            tokens = self.process_text(story)
            self.stories.append(' '.join(tokens))

    def print_key_words(self):
        # Iterate through key words dictionary and print title along with top 5 key words
        for title, key_words in self.key_words.items():
            print(f'{title}:')
            print(*[key_word[0] for key_word in key_words], '\n')

    def process_text(self, some_text: str) -> list:
        # Tokenize text into words and convert to lowercase
        tokens = nltk.tokenize.word_tokenize(some_text.lower())
        # Initialize lemmatizer
        lemmatizer = WordNetLemmatizer()
        # Filter out stopwords and punctuation, and lemmatize remaining words
        filtered_tokens = list(filter(lambda x: x not in self.filter_items, tokens))
        # Filter out non-noun tokens using NLTK's part-of-speech tagging
        processed_tokens = filter(lambda x: nltk.pos_tag([x])[0][1] == 'NN',
                                  [lemmatizer.lemmatize(token) for token in filtered_tokens])
        return list(processed_tokens)

    def calculate_tf_idf(self) -> dict:
        # Parse XML to extract titles and stories
        self.parse_xml()
        # Initialize TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        # Compute TF-IDF scores for stories
        tfidf_matrix = vectorizer.fit_transform(self.stories)
        # Get feature names (terms)
        terms = vectorizer.get_feature_names_out()
        # Dictionary to store TF-IDF scores for each document
        tfidf_scores = dict()
        # Iterate through each document
        for document_index in range(len(self.stories)):
            # Get TF-IDF scores for each term in the document
            words_score = list(((term, score) for term, score in zip(terms, tfidf_matrix.toarray()[document_index])))
            # Select top 10 TF-IDF scores and then top 5 from them
            ten_best_scores = sorted(words_score, key=lambda x: (x[1]), reverse=True)[:10]
            five_best_scores = sorted(ten_best_scores, key=lambda x: (x[1], x[0]), reverse=True)[:5]
            # Add top 5 keywords and their scores to dictionary
            tfidf_scores[self.titles[document_index]] = five_best_scores
        return tfidf_scores


def main():
    # File name of the XML containing news data
    filename = 'news.xml'
    # Create instance of KeyTermsExtractor
    key_terms_extractor = KeyTermsExtractor(filename)
    # Print keywords extracted from news articles
    key_terms_extractor.print_key_words()


if __name__ == '__main__':
    main()
