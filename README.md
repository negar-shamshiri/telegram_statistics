# telegram_statistics
Export Statistics for a Telegram Group Chat

## Description
This program downloads and extracts json file of a telegram group to generate a word cloud from this data.

![WordCloud](wordcloud.png)

## How to Run
First, in main repo directory, run the following code to add `src` to your `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then run:
```
python src/chat_statistics/stats.py
```
to generate a word cloud of json data in `DATA_DIR`