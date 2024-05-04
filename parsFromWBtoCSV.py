import requests
import csv
Name_Brand = str()

class ParseWB:
    def __init__(self, url:str):
        self.brand_id = self.__get_brand_id(url)

    @staticmethod
    def __get_brand_id(url:str):
        numbers = "0123456789"
        flag = 0
        brand_id = str()
        esornonumb = 0
        #Вместо использования регулярных фраз для определения id товара, написана небольшая функция для работы со строкой
        for i in range(len(url)): 
            if url[i] in numbers:
                esornonumb = 1
                break

        if ("brands" in url) and (esornonumb == 1):
            for i in range(len(url)):
                if (url[i-1] =="-" and (url[i] in numbers)) or (url[i-1] =="/" and (url[i] in numbers)):
                    flag = 1

                if (len(url) == i) or (url[i] not in numbers):
                    flag = 0

                if flag == 1:
                    brand_id += url[i]

        elif ("seller" in url) and (esornonumb == 1):
            pass

        elif esornonumb == 0:
            brandName = str()
            flag = 1

            for i in range(len(url)-1, 0, -1):

                if (url[i] =="/"):
                    flag = 0

                if flag == 1:
                    brandName += url[i]
                    
            brandName = brandName[::-1]
            brand_file = requests.get(f'https://static-basket-01.wbbasket.ru/vol0/data/brands/{brandName}.json')
            brand_id = brand_file.json()["id"]


        return brand_id
    
    def parse(self):
        i = 1
        response = requests.get(f'https://catalog.wb.ru/brands/v2/catalog?appType=1&brand={self.brand_id}&curr=rub&dest=-1257786&page={i}&sort=popular&spp=30')
        global Name_Brand
        Name_Brand = response.json()["data"]["products"][0]["brand"]
        Name_Brand = Name_Brand.replace(' ','_')
        self.__create_csv()
        while True:
            response = requests.get(f'https://catalog.wb.ru/brands/v2/catalog?appType=1&brand={self.brand_id}&curr=rub&dest=-1257786&page={i}&sort=popular&spp=30')
            
            items_info = response.json()["data"]
            if items_info['products']==[]:
                print("Обработано",i,"страниц")
                break
            i += 1
            self.__save_csv(items_info)

    def __create_csv(self):
        with open (f"D:\Proga\Парсинг\wb_data_{Name_Brand}.csv", mode = "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'Название', 'Брэнд', 'Цена', 'Количество продаж', 'Количество на складе', 'Рейтинг', 'В наличии'])

    def __save_csv(self, items):
        with open (f"D:\Proga\Парсинг\wb_data_{Name_Brand}.csv", mode = "a", newline = "") as file:
            writer = csv.writer(file)
            for product in items["products"]:
                writer.writerow([product["id"],
                                 product["name"],
                                 product["sizes"][0]["price"]["product"],
                                 product["brand"],
                                 product["ksort"],
                                 product["rating"],
                                 product["volume"]
                                 ])


if __name__ == "__main__":
    print("Введите ссылку на бренд")
    name = str(input())
    ParseWB(f"{name}").parse() 
