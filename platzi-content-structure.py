import requests
from bs4 import BeautifulSoup
import datetime
import argparse
import re
from urllib.parse import urlparse


class PlatziClass:
    PYTHON_PARSER = 'html.parser'
    RESPONSE_OK = 200

    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()

    def get_response(self):
        response = requests.get(self.url)
        if response.status_code == PlatziClass.RESPONSE_OK:
            return response
        else:
            raise Exception('An error occurred when making the resquest. Status code {}.'.format(response.status_code))

    def get_soup(self):
        response = self.get_response()
        return BeautifulSoup(response.text, PlatziClass.PYTHON_PARSER)

    def get_title(self):
        course_banner_title = self.soup.select('.CourseBanner-title')[0]
        return course_banner_title.span.text

    def get_modules(self):
        modules = self.soup.select('.Concept')
        return list(map(lambda module: PlatziModule(module), modules))

    def get_duration(self):
        total_duration = 0
        modules = self.get_modules()
        for module in modules:
            lessons = module.get_lessons()
            for lesson in lessons:
                total_duration += lesson.get_duration()
        return total_duration

    def get_formated_duration(self):
        class_duration = self.get_duration()
        return str(datetime.timedelta(minutes=class_duration))


class PlatziModule:

    def __init__(self, soup_module):
        self.module = soup_module

    def get_title(self):
        return self.module.header.div.h3.text
    
    def get_lessons(self):
        lessons = self.module.section.contents
        return list(map(lambda lesson: PlatziLesson(lesson), lessons))


class PlatziLesson:
    MINUTES_PATTERN = '(\d+):(\d+)'
    HOST_NAME = 'https://platzi.com'

    def __init__(self, soup_lesson):
        self.lesson = soup_lesson

    def get_link(self):
        return PlatziLesson.HOST_NAME + self.lesson.a['href']

    def get_title(self):
        return self.lesson \
                   .select('.MaterialContent-title')[0] \
                   .text

    def get_duration(self):
        text_duration = self.lesson \
                            .select('.MaterialContent-duration')[0] \
                            .text
        matches = re.search(PlatziLesson.MINUTES_PATTERN, text_duration)
        text_minutes = matches.group(1)
        return int(text_minutes)


class Markdown:
    SPECIAL_CHARS_DICT = {
        'á': '%C3%A1',
        'é': '%C3%A9',
        'í': '%C3%AD',
        'ó': '%C3%B3',
        'ú': '%C3%BA',
        'ñ': '%C3%B1'
    }

    @staticmethod
    def h1(text, toc=False):
        return '# {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    @staticmethod
    def h2(text, toc=False):
        return '## {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    @staticmethod
    def h3(text, toc=False):
        return '### {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    @staticmethod
    def h4(text, toc=False):
        return '#### {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    @staticmethod
    def hr():
        return '---'

    @staticmethod
    def link(text, href):
        return '[{}]({})'.format(text, href)

    @staticmethod
    def slug(text):
        word_array = Markdown.get_word_array(text)
        return '#' + '-'.join(word_array)

    @staticmethod
    def change_special_chars(text):
        changed_text = text
        for special_char, symbol in Markdown.SPECIAL_CHARS_DICT.items():
            if special_char in changed_text:
                changed_text = changed_text.replace(special_char, symbol)
        return changed_text

    @staticmethod
    def get_word_array(text):
        word_array = []
        i = 0
        while i < len(text):
            if text[i].isalpha():
                word = ''
                while i < len(text) and text[i].isalpha():
                    word += text[i]
                    i += 1
                changed_word = Markdown.change_special_chars(word.lower())
                word_array.append(changed_word)
            i += 1
        return word_array

    @staticmethod
    def index_link(text):
        return Markdown.link(text, Markdown.slug(text))


class Readme:
    FILE_NAME = 'readme.md'
    FILE_MODE_W = 'w'
    RESOURCES_LINE = 'Resources:'
    NEW_LINE_CHAR = '\n'
    INDEX_INDENTATION_LEVEL_1 = '* '
    INDEX_INDENTATION_LEVEL_2 = '  - '
    INDEX_INDENTATION_LEVEL_3 = '    + '

    def __init__(self, course_url):
        self.course_url = course_url
        self.platzi_class = PlatziClass(self.course_url)

    def create_readme(self):
        file = open(Readme.FILE_NAME, Readme.FILE_MODE_W)

        link_class_title = Markdown.link(self.platzi_class.get_title(),
                                         self.platzi_class.url)
        class_title = Markdown.h1(link_class_title)
        file.write(class_title)
        file.write(Readme.NEW_LINE_CHAR * 2)

        file.write(self.create_index())

        modules = self.platzi_class.get_modules()
        for module in modules:
            module_title = Markdown.h2(module.get_title())
            file.write(module_title)
            file.write(Readme.NEW_LINE_CHAR * 2)

            lessons = module.get_lessons()
            for lesson in lessons:
                link_lesson_title = Markdown.link(lesson.get_title(), lesson.get_link())
                lesson_title = Markdown.h3(link_lesson_title)
                file.write(lesson_title)
                file.write(Readme.NEW_LINE_CHAR * 4)
                file.write(Markdown.hr())
                file.write(Readme.NEW_LINE_CHAR * 2)
        file.write(Markdown.h4(Readme.RESOURCES_LINE, True))
        file.close()

    def create_index(self):
        index = ''

        class_title = self.platzi_class.get_title()
        index_class_title = Readme.INDEX_INDENTATION_LEVEL_1 + Markdown.index_link(class_title)
        index += index_class_title
        index += Readme.NEW_LINE_CHAR

        modules = self.platzi_class.get_modules()
        for module in modules:
            module_title = module.get_title()
            index_module_title = Readme.INDEX_INDENTATION_LEVEL_2 + Markdown.index_link(module_title)
            index += index_module_title
            index += Readme.NEW_LINE_CHAR

            lessons = module.get_lessons()
            for lesson in lessons:
                lesson_title = lesson.get_title()
                index_lesson_title = Readme.INDEX_INDENTATION_LEVEL_3 + Markdown.index_link(lesson_title)
                index += index_lesson_title
                index += Readme.NEW_LINE_CHAR
        index += Readme.NEW_LINE_CHAR
        return index


def is_valid_url(url):
    parse_result = urlparse(url)
    return bool(parse_result.scheme) and bool(parse_result.netloc)


def is_platzi_class(path):
    match_object = re.search('^/clases/.*?/', path)
    return len(match_object.group(0)) == len(path)


def is_platzi_url(url):
    if is_valid_url(url):
        parse_result = urlparse(url)
        return parse_result.netloc == 'platzi.com' and is_platzi_class(parse_result.path)


def main():
    parser = argparse.ArgumentParser(description="Receives a Platzi course url and creates a readme with its respective modules and lessons.")
    parser.add_argument('URL', help='URL used to fetch the information of a Platzi course.')
    args = parser.parse_args()
    if is_platzi_url(args.URL):
        readme = Readme(args.URL)
        readme.create_readme()
    else:
        print('The URL is not a URL from a Platzi course.')


main()

# hacer que reciva un path para guardar el readme
# hacer que reciva un nombre de archivo para el readme
# compartir en platzi, de algún modo
# checar caracter '?'
# checar caracter '!'