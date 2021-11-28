from bs4 import BeautifulSoup
import requests


def get_html(faculty=9, speciality=203, typeofstudy=1, ):
    return requests.get(
        "https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty={}&p_speciality={}&p_inst=0&p_typeofstudy={}".format(
            faculty, speciality, typeofstudy)).content


def get_snils_dictionary(faculty=9, speciality=203, typeofstudy=1):
    data = get_html(faculty, speciality, typeofstudy)
    dictionary = {}

    soup = BeautifulSoup(data, 'lxml')

    trs = soup.find("table", id='t_common').find_all('tr')

    for tr in trs:
        number = ''
        for n in tr.select('td:nth-of-type(1)'):
            number = n.text

        snils = ''
        for n in tr.select('td:nth-of-type(2)'):
            snils = n.text

        dictionary[number] = snils
    return dictionary


dict = get_snils_dictionary()

for d in dict.items():
    print(d[0], ' - ', d[1])