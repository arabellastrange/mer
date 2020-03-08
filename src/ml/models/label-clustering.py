from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

PATH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_low.csv'

PATH_HIGH_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_more_clustered_label_truth.csv'
PATH_LOW_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_more_clustered_label_truth.csv'

label_cols_x = ['airy_x', 'ambient_x', 'angry_x', 'animated_x', 'astonishing_x', 'big_x', 'bizarre_x', 'black_x',
                'bleak_x', 'boisterous_x',
                'boring_x', 'breezy_x', 'bright_x', 'buoyant_x', 'calm_x', 'cheerful_x', 'cheery_x', 'choral_x',
                'comfortable_x',
                'complex_x', 'constant_x', 'contented_x', 'contrasting_x', 'cool_x', 'curious_x', 'dark_x', 'daze_x',
                'deafening_x', 'deep_x',
                'dejected_x', 'delicate_x', 'delighted_x', 'despondent_x', 'different_x', 'difficult_x', 'dim_x',
                'distinctive_x',
                'dreamy_x', 'dull_x', 'earthy_x', 'easy_x', 'eccentric_x', 'ecstasy_x', 'ecstatic_x', 'eerie_x',
                'elated_x', 'emphatic_x',
                'encouraging_x', 'energetic_x', 'enveloping_x', 'extraordinary_x', 'familiar_x', 'fashionable_x',
                'fast_x',
                'fiery_x',
                'flashy_x', 'fluid_x', 'funky_x', 'gray_x', 'happy_x', 'hard_x', 'harmonious_x', 'heated_x', 'heavy_x',
                'hip_x', 'hopeful_x',
                'jazzy_x', 'light_x', 'lively_x', 'loud_x', 'low_x', 'luminous_x', 'melancholy_x', 'mellow_x', 'mild_x',
                'modish_x', 'monotonous_x',
                'mournful_x', 'muted_x', 'odd_x', 'old_x', 'operatic_x', 'orchestral_x', 'passionate_x', 'peaceful_x',
                'peculiar_x', 'profound_x',
                'quick_x', 'quiet_x', 'rapture_x', 'relaxed_x', 'repeated_x', 'repetitive_x', 'reticent_x', 'rich_x',
                'sad_x', 'scary_x',
                'serene_x', 'sexy_x', 'silent_x', 'slow_x', 'snappy_x', 'soft_x', 'somber_x', 'soothing_x', 'space_x',
                'storming_x', 'strange_x',
                'sunny_x', 'sweet_x', 'traditional_x', 'trance_x', 'unconventional_x', 'upbeat_x', 'weighty_x',
                'weird_x',
                'wistful_x', 'zippy_x']

label_cols = ['airy', 'ambient', 'angry', 'animated', 'astonishing', 'big', 'bizarre', 'black',
              'bleak', 'boisterous',
              'boring', 'breezy', 'bright', 'buoyant', 'calm', 'cheerful', 'cheery', 'choral',
              'comfortable',
              'complex', 'constant', 'contented', 'contrasting', 'cool', 'curious', 'dark', 'daze',
              'deafening', 'deep',
              'dejected', 'delicate', 'delighted', 'despondent', 'different', 'difficult', 'dim',
              'distinctive',
              'dreamy', 'dull', 'earthy', 'easy', 'eccentric', 'ecstasy', 'ecstatic', 'eerie',
              'elated', 'emphatic',
              'encouraging', 'energetic', 'enveloping', 'extraordinary', 'familiar', 'fashionable',
              'fast',
              'fiery',
              'flashy', 'fluid', 'funky', 'gray', 'happy', 'hard', 'harmonious', 'heated', 'heavy',
              'hip', 'hopeful',
              'jazzy', 'light', 'lively', 'loud', 'low', 'luminous', 'melancholy', 'mellow', 'mild',
              'modish', 'monotonous',
              'mournful', 'muted', 'odd', 'old', 'operatic', 'orchestral', 'passionate', 'peaceful',
              'peculiar', 'profound',
              'quick', 'quiet', 'rapture', 'relaxed', 'repeated', 'repetitive', 'reticent', 'rich',
              'sad', 'scary',
              'serene', 'sexy', 'silent', 'slow', 'snappy', 'soft', 'somber', 'soothing', 'space',
              'storming', 'strange',
              'sunny', 'sweet', 'traditional', 'trance', 'unconventional', 'upbeat', 'weighty', 'weird',
              'wistful', 'zippy']


def load_file(path):
    return pd.read_csv(path)


def cluster(data):
    kmeans = KMeans(n_clusters=40)

    y = kmeans.fit_predict(data[label_cols])
    data['Cluster'] = y

    # visualise
    centers = kmeans.cluster_centers_
    print(centers)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
    plt.show()

    label_sets = {}
    for i in range(0, 40):
        labels = set()
        cluster_rows = data.loc[data['Cluster'] == i]
        for n, row in cluster_rows.iterrows():
            for label in label_cols:
                if row[label] == 1:
                    labels.add(label)
        print("On Cluster: ")
        print(i)
        print(labels)
        label_sets[i] = labels

    for x in range(0, 40):
        data[repr(label_sets[x])] = 0

    return data


def main():
    data = load_file(PATH_HIGH_CLUSTERED)
    data['mood'] = ''

    label_sets = {}
    for y in range(0, 40):
        cluster_rows = data.loc[data['Cluster'] == y]
        cluster_tags = set()
        for x, label_row in cluster_rows.iterrows():
            for label in label_cols_x:
                if label_row[label] == 1:
                    cluster_tags.add(label)

        if len(cluster_tags) == 0:
            cluster_tags.add('none')
        print("Cluster")
        print(y)
        print(cluster_tags)
        label_sets[y] = cluster_tags

    for z, mood_row in data.iterrows():
        data.at[z, 'mood'] = label_sets.get(mood_row['Cluster'])

    print(data.head())
    data.to_csv(PATH_HIGH_CLUSTERED, index=False)


if __name__ == '__main__':
    main()
