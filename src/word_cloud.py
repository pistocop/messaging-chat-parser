import argparse
import sys
from src.utils import get_txt_files
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from stop_words import get_stop_words


def run(txt_input: str, img_output: str):
    txt_files_name, txt_files_paths = get_txt_files(txt_input)
    ita_stopwords = get_stop_words('it')
    for file_path in txt_files_paths:
        with open(file_path, 'r') as f:
            corpus = f.readlines()
            corpus_mono_line = ' '.join(corpus)
            wordcloud = WordCloud(width=800, height=800,
                                  background_color='white',
                                  stopwords=set(ita_stopwords),
                                  min_font_size=10).generate(corpus_mono_line)
            # plot the WordCloud image
            plt.figure(figsize=(8, 8), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.show()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_input', type=str, required=False, default="../data/output/")
    parser.add_argument('--img_output', type=str, required=False, default="../data/output/word_cloud/")
    params, _ = parser.parse_known_args(argv)
    run(params.txt_input, params.img_output)


if __name__ == '__main__':
    main(sys.argv[1:])
