import json
from collections import Counter
from pathlib import Path
from loguru import logger


import arabic_reshaper
import matplotlib.pyplot as pl
from bidi.algorithm import get_display
from wordcloud import WordCloud

from src.data import DATA_DIR


class ChatStatistics:
     """Generates chat statistics from a telegram chat json file
     """
     def __init__(self, chat_json: str):
          """
          :param chat_json : path to telegram export json file
          """

          #load chat data
          logger.info(f"Loading chat data from{chat_json}...")
          with open(chat_json) as f:
               self.chat_data = json.load(f)


     def generate_word_cloud(self, output_dir):
          """Generates a word cloud from the chat data

          :param output_dir: path to output directory for word cloud image
          """
          logger.info("Loading text content...")
          text_content = ''

          for msg in self.chat_data['messages']:
               if type(msg['text']) is str:
                    text_content += f" {msg['text']}"
          
          #remove stop words
          x = Counter(text_content.split()).most_common()
          x = x[12:3000]

          text_content_new = ''

          for i  in x:
               text_content_new += f' {i[0]} ' * i[1]

          #reshape for final word cloud
          text_content_new = arabic_reshaper.reshape(text_content_new)
          #text_content_new = get_display(text_content_new)

          logger.info("Generating word cloud...")
          
          wordcloud = WordCloud(
               width=1200, height=1200,
               font_path= str(DATA_DIR / './BHoma.ttf'),
               background_color='white',
          ).generate(text_content_new)

          logger.info(f"Saving word cloud to {output_dir}...")
          wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))




if __name__ == "__main__":
     chat_stats = ChatStatistics(chat_json=DATA_DIR / 'online_messages.json')
     chat_stats.generate_word_cloud(output_dir=DATA_DIR)
     print('Done!')