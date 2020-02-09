import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import numpy as np 

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'


def load_ground_truth():
    return pd.read_csv(PATH_TRUTH)


def format_tags_as_list(data):
    for i, row in data.iterrows():
        data.at[i, 'mood'] = literal_eval(row['mood'])
    return data


def scatterplot(x_data, y_data, x_label="", y_label="", title="", color="r", yscale_log=False):
    # Create the plot object
    _, ax = plt.subplots()

    # Plot the data, set the size (s), color and transparency (alpha)
    # of the points
    ax.scatter(x_data, y_data, s=10, color=color, alpha=0.75)

    if yscale_log == True:
        ax.set_yscale('log')

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def main():
    data = load_ground_truth()
    data = format_tags_as_list(data)

    # plot the arousal-valence values of dataset
    # scatterplot(data['arousal'], data['valence'], 'Arousal', 'Valence', 'Arousal-Valence of Songs', "g", False)

    # plot number of songs for every tag
    mood_info = data['mood'].apply(pd.Series).stack().value_counts()
    # drop tags with one hundred occurences
    m = mood_info[mood_info < 45]
    print(m)
    mood_info = mood_info[mood_info > 100]
    mood_info.plot.bar(x='Mood Tag', y='Count')
    plt.show()
    

if __name__ == '__main__':
    main()
