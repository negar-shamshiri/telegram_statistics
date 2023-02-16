import json
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    """
    Generate chat statistics from a telegram group chat json file
    """
    def __init__(self, chat_json: Union[str, Path]):
        """
        :param chat_json: path to telegram export json file
        """
        # load data
        logger.info(f"Loading chat data from {chat_json}")
        with open(chat_json) as f:
            self.chat_data = json.load(f)

        self.normalizer = Normalizer()

        # load stopwords
        logger.info(f"Loading stopwords from {DATA_DIR / 'stopwords.txt'}")
        stop_words = open(DATA_DIR/'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))


    # generate word cloud
    def generate_word_cload(self, output_dir: Union[str, Path]):
        """Generates a word cloud from the chat data

        :param output_dir: path to output directory for word cloud
        """
        logger.info("Loading text content")
        text_content = ''

        for message in self.chat_data['messages']:
            if type(message['text']) is str:
                tokens = word_tokenize(message['text'])
                tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                text_content += f" {' '.join(tokens)}"
            
            elif type(message['text']) is list:
                for sub_message in message['text']:
                    if type(sub_message) is str:
                        tokens = word_tokenize(sub_message)
                        tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                        text_content += f" {' '.join(tokens)}"
                    
                    elif type(sub_message) is list:
                        for sub_sub_msg in sub_message:
                            tokens = word_tokenize(sub_sub_msg['text'])
                            tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                            text_content += f" {' '.join(tokens)}"

        # normalize, reshape for final word cloud
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)

        # generate word cloud
        logger.info("Generating word cloud")
        wordcloud = WordCloud(
            font_path=str(DATA_DIR/'BHoma.ttf'),
            background_color='white',
        ).generate(text_content)

        logger.info(f"Saving word cloud to {output_dir}")
        wordcloud.to_file(str(Path(output_dir)/ 'wordcloud.png'))


if __name__ =="__main__":
    chat_stats = ChatStatistics(chat_json=DATA_DIR/'python2022gp.json')
    chat_stats.generate_word_cload(output_dir=DATA_DIR)
