import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from apyori import apriori


def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df.set_index('Date', inplace=True)
        return df
    except Exception as e:
        raise e


def draw_chart(df):
    plt.figure(figsize=(15, 5))
    top_20_items = df.itemDescription.value_counts().head(20)
    sns.barplot(x=top_20_items.index, y=top_20_items.values, hue=top_20_items.index, legend=False)
    plt.xlabel('Item Description', size=15)
    plt.xticks(rotation=45)
    plt.ylabel('Count of Items', size=15)
    plt.title('Top 20 Items purchased by customers', color='green', size=20)
    plt.tight_layout()
    return plt.gcf()


def get_association_rules(transactions):
    rules = apriori(transactions, min_support=0.00030, min_confidence=0.05, min_lift=2, min_length=2)
    results = list(rules)
    return inspect(results)


def inspect(results):
    lhs = [tuple(result[2][0][0])[0] for result in results]
    rhs = [tuple(result[2][0][1])[0] for result in results]
    supports = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
