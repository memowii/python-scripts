import requests
import urllib.request
import time
from bs4 import BeautifulSoup

import re
import datetime

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
    
    def h1(text, toc=False):
        return '# {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    def h2(text, toc=False):
        return '## {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    def h3(text, toc=False):
        return '### {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    def h4(text, toc=False):
        return '#### {}{}'.format(text, ' <!-- omit in toc -->' if toc else '')

    def hr():
        return '---'

    def link(text, href):
        return '[{}]({})'.format(text, href)

# print(Markdown.h1('Curso de Programación en Bash Shell'))
# print(Markdown.link("I'm an inline-style link", 'https://www.google.com'))
# print(Markdown.h1(Markdown.link('Introducción a Terminal y Línea de Comandos', 'https://platzi.com/clases/bash-shell/')))

class Readme:
    FILE_NAME = 'readme.md'
    FILE_MODE_W = 'w'

    def __init__(self, course_url):
        self.course_url = course_url
        self.platzi_class = PlatziClass(self.course_url)

    def create_readme(self):
        file = open(Readme.FILE_NAME, Readme.FILE_MODE_W)
        
        link_class_title = Markdown.link(self.platzi_class.get_title(), self.platzi_class.url)
        class_title = Markdown.h1(link_class_title)
        file.write(class_title)
        file.write('\n\n')

        modules = self.platzi_class.get_modules()
        for module in modules:
            module_title = Markdown.h2(module.get_title())
            file.write(module_title)
            file.write('\n\n')

            lessons = module.get_lessons()
            for lesson in lessons:
                link_lesson_title = Markdown.link(lesson.get_title(), lesson.get_link())
                lesson_title = Markdown.h3(link_lesson_title)
                file.write(link_lesson_title)
                file.write('\n\n\n\n')
                file.write(Markdown.hr())
                file.write('\n\n')
        file.write(Markdown.h4('Resources:', True))
        file.close()
        

readme = Readme('https://platzi.com/clases/bash-shell/')
readme.create_readme()