import math
import string
from pathlib import Path

import numpy as np
import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

nlp = spacy.load('en_core_web_sm')

path_raw: str = 'data/spam.csv'
path: str = 'data/spam_cleaned.csv'
encoding: str = 'CP1252'


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(path if Path(path).is_file() else path_raw,
                       header=0,
                       names=['Target', 'SMS'],
                       usecols=[0, 1],
                       encoding=encoding)


def preprocess(text: str) -> str:
    doc = nlp(text.casefold())
    text = [token.lemma_.translate(str.maketrans('', '', string.punctuation)) for token in doc]
    text = ['aanumbers' if any(char.isdigit() for char in token) else token for token in text]
    text = [token for token in text if not nlp.vocab[token].is_stop and len(token) > 1]
    return ' '.join(text)


def bag_of_words(x: pd.Series) -> pd.DataFrame:
    vectorizer = CountVectorizer()
    tdm = vectorizer.fit_transform(x)
    return pd.DataFrame(tdm.toarray(), columns=vectorizer.get_feature_names_out())


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    if not Path(path).is_file():
        df['SMS'] = df['SMS'].apply(preprocess)
        df.to_csv(path, index=False, encoding=encoding)
    return df


def calc_probabilities(X_train, y_train) -> pd.DataFrame:
    α = 1
    counts = bag_of_words(X_train).groupby(y_train.reset_index(drop=True)).sum()
    probs = (counts + α).divide(counts.sum(axis=1) + α * counts.shape[1], axis=0)
    return pd.DataFrame(data=[probs.loc['spam'], probs.loc['ham']],
                        index=['Spam Probability', 'Ham Probability']).T


def predict(probs: pd.DataFrame, X_test: pd.DataFrame, y_test: pd.DataFrame, prior_ham, prior_spam) -> pd.DataFrame:
    predictions = []
    probs_dict = probs.to_dict()
    for msg in X_test:
        words = [w for w in msg.split() if w in probs.index]
        spam = prior_spam * np.prod([probs_dict['Spam Probability'][w] for w in words])
        ham = prior_ham * np.prod([probs_dict['Ham Probability'][w] for w in words])
        predictions.append('spam' if spam > ham else 'ham' if spam < ham else 'unknown')

    return pd.DataFrame(data=zip(predictions, y_test),
                        columns=['Predicted', 'Actual'],
                        index=y_test.index)


def calc_metrics(predicts: pd.DataFrame) -> dict[str, float]:
    cm = predicts.groupby('Actual')['Predicted'].value_counts().unstack()
    tn, fp, fn, tp = cm.loc['ham', 'ham'], cm.loc['ham', 'spam'], cm.loc['spam', 'ham'], cm.loc['spam', 'spam']

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1 = 2 * (precision * recall) / (precision + recall)

    return {
        'Accuracy': accuracy,
        'Recall': recall,
        'Precision': precision,
        'F1': f1
    }


def main() -> None:
    df = load_dataset()
    df = prepare_data(df)
    X_test, X_train, y_test, y_train = train_test_split(df['SMS'].fillna(''),
                                                        df['Target'],
                                                        train_size=math.ceil(0.2 * len(df)),
                                                        random_state=43)
    # Convert to Bag of Words dataframes
    vectorizer = CountVectorizer()
    X_train_bow = vectorizer.fit_transform(X_train)
    X_test_bow = vectorizer.transform(X_test)

    # Convert text entries in the Target column to binary numbers
    y_train_binary = y_train.map({'ham': 0, 'spam': 1})
    y_test_binary = y_test.map({'ham': 0, 'spam': 1})

    # Train MultinomialNB model
    clf = MultinomialNB()
    clf.fit(X_train_bow, y_train_binary)

    # Make predictions
    predictions = clf.predict(X_test_bow)

    # Compute metrics
    accuracy = accuracy_score(y_test_binary, predictions)
    recall = recall_score(y_test_binary, predictions)
    precision = precision_score(y_test_binary, predictions)
    f1 = f1_score(y_test_binary, predictions)

    print({
        'Accuracy': accuracy,
        'Recall': recall,
        'Precision': precision,
        'F1': f1
    })


if __name__ == '__main__':
    main()


