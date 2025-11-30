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

class TorgiParser:
    """Класс для работы с лотами торгов"""
    
    def __init__(self):
        """Конструктор - запускается при создании объекта"""
        self.lots = []  # Здесь будем хранить все лоты
        print("Парсер готов к работе!")
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
                'link': 'https://torgi.gov.ru/lot/101'
            },
            {
                'name': 'Офисное помещение 50 кв.м', 
                'price': 1800000, 
                'link': 'https://torgi.gov.ru/lot/102'
            },
            {
                'name': 'Грузовой автомобиль Volvo', 
                'price': 500000, 
                'link': 'https://torgi.gov.ru/lot/103'
            },
            {
                'name': 'Торговое оборудование', 
                'price': 150000, 
                'link': 'https://torgi.gov.ru/lot/104'
            },
            {
                'name': 'Жилая квартира 75 кв.м', 
                'price': 3500000, 
                'link': 'https://torgi.gov.ru/lot/105'
            },
        ]
        
        print(f"Создано {len(sample_lots)} демонстрационных лотов")
        return sample_lots
          def sort_lots_by_price(self, lots):
        """Сортирует лоты от дорогих к дешевым"""
        print("🔄 Сортируем лоты по цене...")
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
            print(f"Цена: {lot['price']:,.2f} ₽")  # Форматируем цену
            print(f"Ссылка: {lot['link']}")
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
        
        print(f"\n СТАТИСТИКА:")
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
    print("\n ФИЛЬТРАЦИЯ ПО ЦЕНЕ")
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
            print(f"\n Найдено {len(filtered_lots)} лотов:")
            parser.display_lots(filtered_lots, 
                              f"Лоты от {min_price:,.0f} до {max_price:,.0f} ₽")
            
            # Сохраняем отфильтрованные данные
            parser.save_to_json(filtered_lots, "filtered_lots.json")
            parser.save_to_csv(filtered_lots, "filtered_lots.csv")
        else:
            print(f"\n Лотов в указанном диапазоне не найдено")
            
    except ValueError:
        print("Ошибка! Вводите только цифры")
    
    print("\n ПРОГРАММА ЗАВЕРШЕНА!")
    print("Созданные файлы:")
    print("lots.json - все лоты (JSON)")
    print("lots.csv - все лоты (CSV)")
    print("filtered_lots.json - отфильтрованные лоты")
    print("filtered_lots.csv - отфильтрованные лоты")

# Запускаем программу, только если файл запущен напрямую
if __name__ == "__main__":
    main()
