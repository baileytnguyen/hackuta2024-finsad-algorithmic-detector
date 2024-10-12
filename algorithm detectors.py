import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Fraud-related comments
fraud_comments = [
    "Svetlana Sarkisian Chowdhury a highly respected figure in her field. I suggest delving deeper into her credentials.",
    "Her name is. 'Lucinda Margaret Crist’. Just research the name. You’d find necessary details to set up an appointment.",
    "My CFA NICOLE ANASTASIA PLUMLEE a renowned figure in her line of work. I recommend researching her credentials.",
    "LAURELYN GROSS POHLMEIER is the licensed fiduciary I use. Just research the name.",
    "Elisse Laparche Ewing is my licenced Advisor. She has years of financial market experience under her belt.",
    "Don't be hesitant to contact Sonya Lee Mitchell and follow her directions.",
]

# Non-fraud comments provided by you
non_fraud_comments = [
    "Many folks overlook the importance of advisors until their emotions cause them problems. I recall a few summers ago, after my lengthy divorce, I needed support to keep my business going. I searched for licensed advisors and found someone extremely qualified. She helped grow my reserve from $175K to $550K, despite inflation.",
    "Find stocks with market-beating yields and shares that at least keep pace with the market for a long term. For a successful long-term strategy I recommend you seek the guidance a broker or financial advisor.",
    "Many folks overlook the importance of advisors until their emotions cause them problems. I recall a few summers ago, after my lengthy divorce, I needed support to keep my business going. I searched for licensed advisors and found someone extremely qualified. She helped grow my reserve from $175K to $550K, despite inflation."
]

# Combine the two categories
comments = fraud_comments + non_fraud_comments

# Labels: 1 for fraud, 0 for non-fraud
labels = [1] * len(fraud_comments) + [0] * len(non_fraud_comments)

# Common fraud patterns (regex-based)
fraud_patterns = [pip
    r'\bhighly respected\b',
    r'\blicensed\b',
    r'\bresearch the name\b',
    r'\blook up\b',
    r'\bschedule an appointment\b',
    r'\bnavigate the financial market\b',
    r'\bvaluable resource\b',
    r'\brenowned\b',
    r'\badvisor\b',
    r'\bfiduciary\b',
    r'\btrusted\b',
    r'\bmentor\b',
    r'\bguided\b',
    r'\bexperienced\b',
    r'\bfinancial expert\b',
]

# Feature extraction based on fraud patterns
vectorizer = CountVectorizer(vocabulary=fraud_patterns)
X = vectorizer.fit_transform(comments)

# Train a simple Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X, labels)

# Function to classify comments
def classify_comment(comment):
    comment_vector = vectorizer.transform([comment])
    prediction = clf.predict(comment_vector)
    return "Fraud" if prediction == 1 else "Non-Fraud"

# Example usage
test_comment = "I work with Sharon Lee Peoples as my fiduciary. Look up the name."
print(f"Test comment: {test_comment}")
print(f"Classification: {classify_comment(test_comment)}")

# Testing on a few comments
test_comments = [
    "Sharon Marissa Wolfe is the licensed advisor I use. Just research the name.",
    "Find stocks with market-beating yields and shares that at least keep pace with the market for a long term."
]
for comment in test_comments:
    print(f"Comment: {comment}")
    print(f"Classification: {classify_comment(comment)}")
    print("------")
