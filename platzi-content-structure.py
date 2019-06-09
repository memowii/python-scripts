import requests
import urllib.request
import time
from bs4 import BeautifulSoup

import re
import datetime

class PlatziClass:

    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()

    def get_response(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response
        else:
            raise Exception('An error occurred when making the resquest. Status code {}.'.format(response.status_code))

    def get_soup(self):
        response = self.get_response()
        return BeautifulSoup(response.text, 'html.parser')

    def get_class_title(self):
        course_banner_title = self.soup.select('.CourseBanner-title')[0]
        return course_banner_title.span.text

    def get_modules(self):
        modules = self.soup.select('.Concept')
        return list(map(lambda module: PlatziModule(module), modules))

    def get_class_duration(self):
        total_duration = 0
        modules = self.get_modules()
        for module in modules:
            lessons = module.get_lessons()
            for lesson in lessons:
                total_duration += lesson.get_duration()
        return total_duration

    def get_formated_class_duration(self):
        class_duration = self.get_class_duration()
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

    def __init__(self, soup_lesson):
        self.lesson = soup_lesson

    def get_link(self):
        return self.lesson.a['href']

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



platzi_clase = PlatziClass('https://platzi.com/clases/bash-shell/')
print(platzi_clase.get_formated_class_duration())