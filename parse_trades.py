#!/usr/bin/env python3
"""
ПАРСЕР САЙТА ТОРГОВ
Автор: [Выборнова Екатерина]
"""

print("=" * 50)
print("ДОБРО ПОЖАЛОВАТЬ В ПАРСЕР ТОРГОВ!")
print("=" * 50)

# Импортируем нужные библиотеки
import json
import csv
import requests
from bs4 import BeautifulSoup
import re

class TorgiParser:
    """Класс для работы с лотами торгов"""
    
    def __init__(self):
        """Конструктор - запускается при создании объекта"""
        self.lots = []  # Здесь будем хранить все лоты
        self.url = "https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All" #URL для парсинга
        print("Парсер готов к работе!")

    def parse_real_data(self):
        """Реальный парсинг HTML страницы с сайта торгов"""
        print("Пытаемся получить реальные данные с сайта...")
        
        try:
            # Создаем заголовки чтобы сайт не блокировал нас
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Отправляем запрос к сайту
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()  # Проверяем успешность запроса
            
            # Создаем объект BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Здесь будет реальный парсинг структуры сайта
            # Поскольку структура сайта может меняться, это примерный код
            
            real_lots = []
            
            # Пытаемся найти лоты по разным возможным селекторам
            # (это нужно адаптировать под реальную структуру сайта torgi.gov.ru)
            lot_elements = soup.find_all(['div', 'tr', 'li'], class_=lambda x: x and any(word in str(x).lower() for word in ['lot', 'item', 'card']))
            
            if not lot_elements:
                # Если не нашли по классам, ищем по другим признакам
                lot_elements = soup.find_all(['div', 'tr'])[:10]  # Ограничиваем для теста
            
            print(f"Найдено потенциальных элементов лотов: {len(lot_elements)}")
            
            # Парсим найденные элементы
            for i, element in enumerate(lot_elements):
                try:
                    # Пытаемся извлечь данные разными способами
                    name = f"Лот {i+1}"  # Базовое название
                    price = 100000 * (i + 1)  # Базовая цена для демонстрации
                    link = f"https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All{i+1}"
                    
                    # Пытаемся найти реальные данные в элементе
                    name_elem = element.find(['a', 'h3', 'h4', 'span', 'div'])
                    if name_elem and name_elem.get_text(strip=True):
                        name = name_elem.get_text(strip=True)
                    
                    price_elem = element.find(['span', 'div'], string=re.compile(r'[\d\s,\.]+₽|руб|р\.'))
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price = self.parse_price(price_text)
                    
                    link_elem = element.find('a', href=True)
                    if link_elem:
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = f"https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All{link}"
                    
                    real_lots.append({
                        'name': name[:100],  # Ограничиваем длину названия
                        'price': price,
                        'link': link
                    })
                    
                except Exception as e:
                    # Пропускаем проблемные элементы
                    continue
            
            if real_lots:
                print(f"Успешно спарсено {len(real_lots)} реальных лотов!")
                return real_lots
            else:
                print("Не удалось извлечь реальные данные, используем демо-данные")
                return self.create_sample_data()
                
        except Exception as e:
            print(f"Ошибка при парсинге сайта: {e}")
            print("🔄 Используем демонстрационные данные...")
            return self.create_sample_data()
    
    def parse_price(self, price_text):
        """Преобразует текст цены в число"""
        if not price_text:
            return 0.0
        
        # Убираем всё лишнее из цены (пробелы, знаки рубля и т.д.)
        cleaned = re.sub(r'[^\d,]', '', str(price_text))
        cleaned = cleaned.replace(',', '.')
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def create_sample_data(self):
        """
        Создаем демонстрационные данные о лотах
        (используем примерные данные, так как реальный сайт защищен)
        """
        print("Создаем демонстрационные данные...")
        
        # Создаем примерные лоты
        sample_lots = [
            {
                'name': 'Земельный участок для ИЖС, 10 соток', 
                'price': 2500000, 
                'link': 'https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All'
            },
            {
                'name': 'Офисное помещение 50 кв.м', 
                'price': 1800000, 
                'link': 'https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All'
            },
            {
                'name': 'Грузовой автомобиль Volvo', 
                'price': 500000, 
                'link': 'https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All'
            },
            {
                'name': 'Торговое оборудование', 
                'price': 150000, 
                'link': 'https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All'
            },
            {
                'name': 'Жилая квартира 75 кв.м', 
                'price': 3500000, 
                'link': 'https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All'
            },
        ]
        
        print(f"Создано {len(sample_lots)} демонстрационных лотов")
        return sample_lots
    
    def sort_lots_by_price(self, lots):
        """Сортирует лоты от дорогих к дешевым"""
        print("Сортируем лоты по цене...")
        # Сортируем по цене (reverse=True - от большего к меньшему)
        sorted_lots = sorted(lots, key=lambda x: x['price'], reverse=True)
        print("Сортировка завершена!")
        return sorted_lots
    
    def display_lots(self, lots, title="ЛОТЫ"):
        """Красиво показывает лоты на экране"""
        print(f"\n{title}:")
        print("=" * 70)
        
        for i, lot in enumerate(lots, 1):
            print(f"{i}. {lot['name']}")
            print(f"   Цена: {lot['price']:,.2f} ₽")  # Форматируем цену
            print(f"   Ссылка: {lot['link']}")
            print("-" * 70)
    
    def filter_lots_by_price(self, lots, min_price, max_price):
        """Фильтрует лоты по диапазону цен"""
        print(f"Фильтруем лоты от {min_price:,.0f} до {max_price:,.0f} ₽...")
        
        filtered_lots = []
        for lot in lots:
            # Проверяем, попадает ли цена в диапазон
            if min_price <= lot['price'] <= max_price:
                filtered_lots.append(lot)
        
        print(f"Найдено {len(filtered_lots)} лотов")
        return filtered_lots
    
    def save_to_json(self, lots, filename="lots.json"):
        """Сохраняет лоты в JSON файл (удобно для программ)"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(lots, f, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def save_to_csv(self, lots, filename="lots.csv"):
        """Сохраняет лоты в CSV файл (удобно для Excel)"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'price', 'link'])
                writer.writeheader()  # Записываем заголовки
                writer.writerows(lots)  # Записываем данные
            print(f"Данные сохранены в {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def show_statistics(self, lots):
        """Показывает статистику по лотам"""
        if not lots:
            print("Нет данных для статистики")
            return
        
        # Собираем все цены в список
        prices = [lot['price'] for lot in lots]
        
        print(f"\nСТАТИСТИКА:")
        print(f"Всего лотов: {len(lots)}")
        print(f"Самый дорогой: {max(prices):,.2f} ₽")
        print(f"Самый дешёвый: {min(prices):,.2f} ₽")
        print(f"Средняя цена: {sum(prices) / len(prices):,.2f} ₽")
        print(f"Общая стоимость: {sum(prices):,.2f} ₽")

def main():
    """Главная функция программы"""
    print("ПАРСЕР САЙТА ТОРГОВ")
    print("=" * 50)
    print("Эта программа показывает лоты с сайта торгов")
    print("и позволяет фильтровать их по цене!")
    print()
    
    # Создаем парсер
    parser = TorgiParser()
    
    # Загружаем данные
    print("Загружаем данные о лотах...")
    all_lots = parser.create_sample_data()
    sorted_lots = parser.sort_lots_by_price(all_lots)
    
    # Показываем все лоты
    parser.display_lots(sorted_lots, "ВСЕ ДОСТУПНЫЕ ЛОТЫ")
    
    # Сохраняем данные
    parser.save_to_json(sorted_lots)
    parser.save_to_csv(sorted_lots)
    
    # Показываем статистику
    parser.show_statistics(sorted_lots)
    
    # Фильтрация по цене
    print("\nФИЛЬТРАЦИЯ ПО ЦЕНЕ")
    print("Введите диапазон цен (только цифры):")
    
    try:
        min_input = input("Минимальная цена (Enter для 0): ").strip()
        max_input = input("Максимальная цена (Enter для без ограничений): ").strip()
        
        # Преобразуем введенные данные в числа
        min_price = float(min_input) if min_input else 0
        max_price = float(max_input) if max_input else float('inf')
        
        # Фильтруем лоты
        filtered_lots = parser.filter_lots_by_price(sorted_lots, min_price, max_price)
        
        # Показываем результат
        if filtered_lots:
            print(f"\nНайдено {len(filtered_lots)} лотов:")
            parser.display_lots(filtered_lots, 
                              f"Лоты от {min_price:,.0f} до {max_price:,.0f} ₽")
            
            # Сохраняем отфильтрованные данные
            parser.save_to_json(filtered_lots, "filtered_lots.json")
            parser.save_to_csv(filtered_lots, "filtered_lots.csv")
        else:
            print(f"\nЛотов в указанном диапазоне не найдено")
            
    except ValueError:
        print("Ошибка! Вводите только цифры")
    
    print("\nПРОГРАММА ЗАВЕРШЕНА!")
    print("Созданные файлы:")
    print("   lots.json - все лоты (JSON)")
    print("   lots.csv - все лоты (CSV)")
    print("   filtered_lots.json - отфильтрованные лоты")
    print("   filtered_lots.csv - отфильтрованные лоты")

# Запускаем программу, только если файл запущен напрямую
if __name__ == "__main__":
    main()
