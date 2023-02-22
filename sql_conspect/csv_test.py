import csv

with open(f'file.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(('Название','Автор', 'Цена','Без скидки','Скидка','Карточка'))
    writer.writerow(('Какое-то название','какй то автор', '0.5','5000','4999,5','https://labirint.ru'))