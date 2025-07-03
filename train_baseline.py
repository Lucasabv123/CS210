# train_baseline.py
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support, classification_report

# Database URL (adjust host if needed)
DATABASE_URL = "postgresql://crm_user:crm_pass@localhost:5432/crm_db"


def load_features(csv_path='rolling_window_features.csv'):
    """
    Load rolling-window features from CSV.
    """
    df = pd.read_csv(csv_path)
    return df


def load_subscription_labels(engine):
    """
    Fetch subscription end_date for each contact from Postgres.
    Returns a DataFrame with columns [contact_id, end_date].
    """
    query = "SELECT contact_id, end_date FROM subscriptions;"
    df = pd.read_sql(query, engine)
    df['end_date'] = pd.to_datetime(df['end_date'])
    return df


def label_churn(df):
    """
    Label churn for contacts whose subscription ended within the last 7 days.
    Adds a 'churned' boolean column to df.
    """
    now = pd.Timestamp.now()
    df['churned'] = df['end_date'].between(
        now - pd.Timedelta(days=7),
        now
    ).fillna(False)
    return df


def train_and_evaluate(df):
    """
    Train a Logistic Regression baseline with class balancing and threshold tuning.
    """
    # Prepare features and labels
    X = df[['interactions_last_7d']]
    y = df['churned']

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Train with class weights to handle imbalance
    model = LogisticRegression(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)

    # Predict probabilities
    probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)

    # Determine optimal threshold (example: 0.3)
    threshold = 0.3
    preds = (probs >= threshold)

    # Metrics at threshold
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, preds, average='binary', zero_division=0
    )

    # Detailed report
    report = classification_report(y_test, preds, zero_division=0)

    # Output results
    print("Baseline Logistic Regression Results:")
    print(f"ROC-AUC: {auc:.3f}")
    print(f"Using threshold: {threshold}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1 Score: {f1:.3f}")
    print("\nClassification Report (threshold {}):".format(threshold))
    print(report)


if __name__ == '__main__':
    engine = create_engine(DATABASE_URL)

    # Load data
    features_df = load_features()
    labels_df = load_subscription_labels(engine)
    df = features_df.merge(labels_df, on='contact_id', how='left')

    # Label churn
    df = label_churn(df)

    # Show distribution
    print("Churn label distribution:")
    print(df['churned'].value_counts())

    # Train and evaluate
    train_and_evaluate(df)
