import argparse
import sys
import matplotlib.pyplot as plt
from os import path
from src.utils import get_dir_files
from wordcloud import WordCloud
from stop_words import get_stop_words

custom_stop_words = ['media', 'omessi']


def run(txt_input: str, img_output: str, stop_words_language: str):
    txt_files_name, txt_files_paths = get_dir_files(dir_path=txt_input, extension_filter='.txt')
    ita_stopwords = get_stop_words(stop_words_language)

    for file_name, file_path in zip(txt_files_name, txt_files_paths):
        fig_path = path.join(img_output, file_name.replace('.txt', '.png'))
        with open(file_path, 'r') as f:
            corpus = f.readlines()
            corpus_mono_line = ' '.join(corpus)
            wordcloud = WordCloud(width=800, height=800,
                                  background_color='white',
                                  stopwords=set(ita_stopwords),
                                  min_font_size=10).generate(corpus_mono_line)
            plt.figure(figsize=(8, 8), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(fig_path)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_input', type=str, required=False, default="../data/chat_parsed")
    parser.add_argument('--img_output', type=str, required=False, default="../data/word_cloud/")
    parser.add_argument('--stop_words_language', type=str, required=False, default="it")
    params, _ = parser.parse_known_args(argv)
    run(params.txt_input, params.img_output, params.stop_words_language)


if __name__ == '__main__':
    main(sys.argv[1:])
