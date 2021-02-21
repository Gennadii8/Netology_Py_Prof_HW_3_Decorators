import xml.etree.ElementTree as ET
import os
import json
import datetime


def write_logs_with_path(path):
    def write_logs(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'w', encoding="utf-8") as f:
                f.write(f'Вызвана функция {old_function.__name__}\n')
                f.write(f'В {datetime.datetime.now()}\n')
                f.write(f'С аргументами {args}, {kwargs}\n')
                f.write(f'Возвращено {old_function(*args, **kwargs)}\n')

        return new_function
    return write_logs


output_file_path = os.path.join(os.getcwd(), 'output_loger.txt')


@write_logs_with_path(path=output_file_path)
def find_10_most_common_words(file, word_lenght=6, top_lenght=10):
    list_of_descr = []
    list_top_of_frequency = []

    def xml_find_every_description():
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(file_path_1, parser)
        root = tree.getroot()
        news_xml = root.findall("channel/item")
        for news in news_xml:
            descr = news.find("description")
            list_of_descr.append(descr.text)
        return(list_of_descr)

    def json_find_every_description():
        with open(file, encoding="utf-8") as f:
            json_data = json.load(f)
        for every_descr in json_data["rss"]["channel"]["items"]:
            list_of_descr.append(every_descr["description"])
        return(list_of_descr)

    def transformation_file():
        list_of_words_in_descr = []
        set_of_descr = set()
        dict_frequency_of_occurrences = {}

        for one_descr in list_of_descr:
            one_split_decr = one_descr.split()
            for every_word in one_split_decr:
                list_of_words_in_descr.append(every_word)

        for one_word in list_of_words_in_descr:
            if len(one_word) > word_lenght:
                set_of_descr.add(one_word)

        for word in list_of_words_in_descr:
            if len(word) > word_lenght:
                if word not in dict_frequency_of_occurrences.keys():
                    dict_frequency_of_occurrences[word] = 1
                else:
                    dict_frequency_of_occurrences[word] += 1

        nonlocal list_top_of_frequency
        list_top_of_frequency = list(dict_frequency_of_occurrences.items())
        list_top_of_frequency.sort(key=lambda i: -i[1])
        print(list_top_of_frequency)
        # for i in list_top_of_frequency[0:top_lenght]:
        #     print(f'{i[0]}:{i[1]}')

    if 'xml' in file:
        xml_find_every_description()
    elif 'json' in file:
        json_find_every_description()
    transformation_file()
    return list_top_of_frequency[0]


if __name__ == '__main__':
    file_path_1 = os.path.join(os.getcwd(), 'newsafr.xml')
    file_path_2 = os.path.join(os.getcwd(), 'newsafr.json')
    find_10_most_common_words(file_path_1)


