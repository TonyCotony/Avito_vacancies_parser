from avito_vacancy_parser import AvitoVacancy
from settings import settings

if __name__ == '__main__':
    link = settings.link.link_to_pars
    parser = AvitoVacancy(link)
    parser.get_first_page()

print('qwe')
