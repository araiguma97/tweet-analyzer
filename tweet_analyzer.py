import csv
from janome.tokenizer import Tokenizer
import re

def main() :
    # yyyy/MM/dd,hh:mm,"tweet contents"
    input_path = r'tweets.csv'
    hour_path = r'hour.csv'
    word_path = r'word.csv'
    count_by_hour(input_path, hour_path)
    count_word(input_path, word_path)

def count_by_hour(input_path, output_path) :
    l = None

    # 入力ファイルを読み込む
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    # 時間ごとに数える
    hours = {}
    for i in range(0, 24) :
        hours[str(i).zfill(2)] = 0
    for row in l :
        hour = row[1][0:2]
        if hour in hours :
            hours[hour] = hours[hour] + 1

    # 出力ファイルに書き込む
    with open(output_path, 'w') as f :
        writer = csv.writer(f, lineterminator='\n')
        for k, v in sorted(hours.items(), key=lambda x: x[0]) :
            writer.writerow([str(k), str(v)])

def count_word(input_path, output_path) :
    l = None

    # 入力ファイルを読み込む
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    # 形態素解析インスタンスを生成する
    tokenizer = Tokenizer()

    # 単語の数を数える
    words = {}
    for row in l :
        content = row[2]
        tokens = tokenizer.tokenize(content)
        for token in tokens :
            # 名詞でなければ、数えない
            if '名詞' not in token.part_of_speech.split(',')[0] :
                continue
            if '数' in token.part_of_speech.split(',')[1] :
                continue
            # 半角記号であれば、数えない
            # MeCab辞書では、半角記号は'名詞,サ変接続,*,*'として分類されている
            if '名詞,サ変接続,*,*' in token.part_of_speech :
                continue
            surface = token.surface
            if surface in words :
                words[surface] = words[surface] + 1
            else :
                words[surface] = 1

    # 出力ファイルに書き込む
    with open(output_path, 'w') as f :
        writer = csv.writer(f, lineterminator='\n')
        for k, v in sorted(words.items(), key=lambda x: -x[1]) :
            writer.writerow([str(k), str(v)])

if __name__ == '__main__' :
    main()
