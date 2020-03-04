from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

PATH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_low.csv'

PATH_HIGH_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_clustered_label_truth.csv'
PATH_LOW_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_clustered_label_truth.csv'

label_cols = ['airy_x', 'ambient_x', 'angry_x', 'animated_x', 'astonishing_x', 'big_x', 'bizarre_x', 'black_x',
              'bleak_x', 'boisterous_x',
              'boring_x', 'breezy_x', 'bright_x', 'buoyant_x', 'calm_x', 'cheerful_x', 'cheery_x', 'choral_x',
              'comfortable_x',
              'complex_x', 'constant_x', 'contented_x', 'contrasting_x', 'cool_x', 'curious_x', 'dark_x', 'daze_x',
              'deafening_x', 'deep_x',
              'dejected_x', 'delicate_x', 'delighted_x', 'despondent_x', 'different_x', 'difficult_x', 'dim_x',
              'distinctive_x',
              'dreamy_x', 'dull_x', 'earthy_x', 'easy_x', 'eccentric_x', 'ecstasy_x', 'ecstatic_x', 'eerie_x',
              'elated_x', 'emphatic_x',
              'encouraging_x', 'energetic_x', 'enveloping_x', 'extraordinar_x', 'familiar_x', 'fashionable_x', 'fast_x',
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
              'sunny_x', 'sweet_x', 'traditional_x', 'trance_x', 'unconventional_x', 'upbeat_x', 'weighty_x', 'weird_x',
              'wistful_x', 'zippy_x']


def load_file(path):
    return pd.read_csv(path)


def cluster(data):
    kmeans = KMeans(n_clusters=30)

    y = kmeans.fit_predict(data[label_cols])
    data['Cluster'] = y

    # visualise
    centers = kmeans.cluster_centers_
    print(centers)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
    plt.show()

    label_sets = {}
    for i in range(0, 30):
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

    for x in range(0, 30):
        data[repr(label_sets[x])] = 0

    return data


def main():
    data = load_file(PATH_HIGH_CLUSTERED)
    #
    # data_cluster = data.drop(columns=['id'])
    # artist_encoder = LabelEncoder()
    # data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    # title_encoder = LabelEncoder()
    # data['title'] = title_encoder.fit_transform(data['title'].astype(str))
    #
    # data_cluster = cluster(data_cluster)
    #
    # data['artist'] = artist_encoder.inverse_transform(data['artist'])
    # data['title'] = title_encoder.inverse_transform(data['title'])
    #
    # data = pd.merge(data, data_cluster, on=['artist', 'title'])
    #
    # print(data.head())

    label_sets = {0: "{'serene', 'mellow', 'relaxed', 'breezy', 'calm'}",
                  1: "{'cheerful', 'happy', 'elated', 'contented', 'delighted', 'ecstatic'}",
                  2: "{'wistful', 'heavy', 'melancholy', 'sad', 'mournful'}",
                  3: "{'angry', 'fiery', 'passionate', 'heated', 'storming'}",
                  4: "{'quiet', 'upbeat', 'dark', 'slow', 'different', 'happy', 'heavy', 'mellow', 'sad', 'strange', "
                     "'weird', 'jazzy', 'repetitive', 'loud', 'deep'}",
                  5: "{'luminous', 'sunny', 'eerie', 'cool', 'bleak', 'happy', 'constant', 'sad', 'relaxed', 'dull', "
                     "'dark', 'low', 'mild', 'orchestral', 'monotonous', 'black', 'old', 'light', 'scary', 'mellow', "
                     "'bright', 'choral', 'weird', 'different', 'repetitive', 'calm', 'somber', 'funky', 'rich', "
                     "'jazzy', 'deep', 'upbeat', 'boring', 'slow', 'dim', 'harmonious', 'strange', 'repeated'}",
                  6: "{'delicate', 'eerie', 'soft', 'sad', 'space', 'relaxed', 'comfortable', 'dark', 'sweet', 'low', "
                     "'soothing', 'orchestral', 'old', 'light', 'mellow', 'trance', 'choral', 'easy', 'loud', 'calm', "
                     "'operatic', 'quiet', 'upbeat', 'slow', 'ambient'}",
                  7: "{'happy', 'soft', 'hard', 'daze', 'ecstasy', 'space', 'rapture', 'odd', 'fast', 'distinctive', "
                     "'low', 'curious', 'quick', 'old', 'mellow', 'trance', 'weird', 'different', 'repetitive', "
                     "'contrasting', 'astonishing', 'extraordinary', 'jazzy', 'quiet', 'dreamy', 'peculiar', "
                     "'ambient', "
                     "'eccentric', 'strange', 'bizarre'}",
                  8: "{'sexy', 'lively', 'flashy', 'animated', 'zippy', 'jazzy'}",
                  9: "{'eerie', 'space', 'dark', 'low', 'orchestral', 'heavy', 'light', 'mellow', 'trance', 'choral', "
                     "'weird', 'different', 'repetitive', 'loud', 'calm', 'funky', 'jazzy', 'airy', 'deep', 'upbeat', "
                     "'slow', 'ambient', 'strange'}",
                  10: "{'eerie', 'soft', 'sad', 'space', 'dark', 'low', 'orchestral', 'scary', 'mellow', 'trance', "
                      "'choral', 'weird', 'different', 'repetitive', 'loud', 'calm', 'airy', 'deep', 'quiet', 'slow', "
                      "'ambient', 'strange'}",
                  11: "{'upbeat', 'encouraging', 'happy', 'cheery', 'hopeful', 'buoyant'}",
                  12: "{'dark', 'profound', 'fast', 'deep', 'different', 'low', 'emphatic', 'heavy', 'hard', 'rich', "
                      "'difficult', 'boisterous', 'deafening', 'complex', 'loud', 'quiet', 'big'}",
                  13: "{'modish', 'fashionable', 'funky', 'earthy', 'unconventional', 'hip'}",
                  14: "{'weird', 'eccentric', 'curious', 'eerie'}",
                  15: "{'dark', 'slow', 'eerie', 'low', 'happy', 'soft', 'orchestral', 'hard', 'light', 'mellow', "
                      "'sad', 'choral', 'weird', 'different', 'loud', 'jazzy', 'calm'}",
                  16: "{'dark', 'slow', 'deep', 'fast', 'low', 'ambient', 'funky', 'scary', 'strange', 'mellow', "
                      "'space', 'weird', 'jazzy', 'airy', 'quiet'}",
                  17: "{'upbeat', 'fast', 'low', 'happy', 'ambient', 'quick', 'funky', 'trance', 'space', 'weird', "
                      "'jazzy', 'repetitive', 'loud', 'quiet'}",
                  18: "{'eerie', 'soft', 'sad', 'space', 'dark', 'low', 'light', 'mellow', 'trance', 'weird', "
                      "'different', 'loud', 'funky', 'jazzy', 'airy', 'deep', 'slow', 'ambient', 'strange'}",
                  19: "{'eerie', 'sad', 'dark', 'low', 'orchestral', 'scary', 'mellow', 'trance', 'choral', 'weird', "
                      "'repetitive', 'loud', 'jazzy', 'deep', 'quiet', 'upbeat', 'slow', 'ambient', 'strange'}",
                  20: "{'fluid', 'enveloping', 'ambient'}",
                  21: "{'upbeat', 'dark', 'slow', 'fast', 'happy', 'soft', 'ambient', 'funky', 'old', 'mellow', "
                      "'strange', 'sad', 'weird', 'jazzy', 'loud'}",
                  22: "{'happy', 'soft', 'hard', 'space', 'dark', 'fast', 'low', 'light', 'mellow', 'trance', 'weird', "
                      "'different', 'repetitive', 'loud', 'calm', 'funky', 'jazzy', 'airy', 'deep', 'ambient', "
                      "'strange'}",
                  23: "{'upbeat', 'fast', 'different', 'ambient', 'funky', 'scary', 'strange', 'trance', 'space', "
                      "'weird', 'jazzy', 'repetitive', 'loud', 'deep'}",
                  24: "{'choral', 'dark', 'slow', 'deep', 'eerie', 'low', 'ambient', 'orchestral', 'heavy', 'scary', "
                      "'strange', 'space', 'weird', 'different', 'repetitive', 'loud', 'quiet'}",
                  25: "{'peaceful', 'reticent', 'soft', 'silent', 'muted', 'quiet'}",
                  26: "{'eerie', 'soft', 'sad', 'space', 'dark', 'low', 'light', 'scary', 'mellow', 'trance', "
                      "'choral', "
                      "'weird', 'different', 'loud', 'airy', 'quiet', 'slow', 'ambient', 'strange'}",
                  27: "{'loud', 'fast', 'heavy'}",
                  28: "{'dark', 'heavy', 'weighty', 'melancholy', 'despondent'}",
                  29: "{'eerie', 'soft', 'space', 'dark', 'fast', 'low', 'quick', 'scary', 'trance', 'choral', "
                      "'weird', 'different', 'repetitive', 'loud', 'calm', 'operatic', 'funky', 'jazzy', 'airy', "
                      "'quiet', 'upbeat', 'ambient', 'strange'}"}

    # for m, row in data.iterrows():
    #     l_set = label_sets.get(row['Cluster'])
    #     data.loc[m, l_set] = 1

    for i in [4, 5, 6, 7, 9, 10, 12, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 29]:
        odd_rows = data.loc[data['Cluster'] == i]
        odd_row_labels = set()
        for n, row in odd_rows.iterrows():
            for label in label_cols:
                if row[label] == 1:
                    odd_row_labels.add(label)
        print("Cluster")
        print(i)
        print(odd_row_labels)

    print(data.head())

    # data.to_csv(PATH_HIGH_CLUSTERED, index=False)


if __name__ == '__main__':
    main()
