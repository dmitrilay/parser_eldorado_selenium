import os
import datetime

URLs = [
    'https://www.eldorado.ru/c/smartfony/',
    # 'https://www.eldorado.ru/c/televizory/',
]

options_web = {
    'profile.managed_default_content_settings.javascript': 2,
    'profile.managed_default_content_settings.images': 2,
    'profile.managed_default_content_settings.mixed_script': 2,
    'profile.managed_default_content_settings.media_stream': 2,
    'profile.managed_default_content_settings.stylesheets': 2
}



# file_path = "C:/Users/dmitr/OneDrive/Документы/1_Parser/mts.xlsx"
# name_f = os.path.normpath(f'{head}/data/{name_f}.xlsx')

# Каталог и путь до него
name_f = 'eldorado.xlsx'
head, tail = os.path.split(__file__)
current_time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M") + '_'
parent = os.path.dirname(head)

current_folder = os.path.normpath(os.path.normpath(f'{head}/data/{current_time}_{name_f}'))
external_folder = os.path.normpath(f"{parent}/{'parser_data'}/{name_f}")
