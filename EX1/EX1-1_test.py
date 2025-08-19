#Задача №1 unit-tests

# Напишите тесты на любые 3 задания из модуля «Основы языка программирования Python». 
# Используйте своё решение домашнего задания.
# При написании тестов не забывайте использовать параметризацию.
# Рекомендации по тестам: если у вас в функциях информация выводилась (print), 
# то теперь её лучше возвращать (return), чтобы можно было протестировать.
#==================================================================

import unittest

#Задание «Победители конкурса»


def solve(receipts: list):
    result = receipts[2::3] # получите правильный срез списка receipts
    return result, len(result) # этот код менять не нужно
#Tест из НЕТОЛОГИИ:
if __name__ == '__main__':
    # Этот код менять не нужно
    result, count = solve([123, 145, 346, 246, 235, 166, 112, 351, 436])
    assert result == [346, 166, 436], f"Список чеков неверный: {result}"
    assert count == 3, f"Количество чеков неверное: {count}"
    print(result)
    print(count)
    result, count = solve([123, 145])
    assert result == [], f"Список чеков неверный: {result}"
    assert count == 0, f"Количество чеков неверное: {count}"
    print(result)
    print(count)

#================TEST-unittest========================================

# Создаем класс для тестирования функции solve, наследуясь от unittest.TestCase
class TestSolveFunction(unittest.TestCase):
    #Для первого примера из задания:
    #assert result == [346, 166, 436], f"Список чеков неверный: {result}"
    #assert count == 3, f"Количество чеков неверное: {count}"
    
    def test_case_from_example_1(self):
        """Проверяем что для списка чеков(или покупок) 
            срез [2::3] возвращает значения [346,166,436] в 
            количестве 3 элементов"""
        #Тестовые данные
        receipts = [123, 145, 346, 246, 235, 166, 112, 351, 436] 
        #Данные которые ожидаем получить с индексами 2-5-8 
        #(каждый третий начиная с индекса)
        expected_result = [346, 166, 436] 
        # Ожидаемое колличество элементов списка
        expected_count = 3
        
        #Вызываем тестируемую функцию solve(receipts)
        result, count = solve(receipts) 
        
        # Проверяем, что результат соответствует ожиданиям
        self.assertEqual(result, expected_result)
        # Проверяем, что количествол элементов соответствует ожиданиям
        self.assertEqual(count, expected_count)
    
# Тест для второго примера из задания:
# result, count = solve([123, 145])
#     assert result == [], f"Список чеков неверный: {result}"
#     assert count == 0, f"Количество чеков неверное: {count}"

    def test_case_from_example_2(self):
        """Проверка прохождения второго условия"""
        # Подготавливаем входные данные - список из 2 элементов
        receipts = [123, 145]
        
        # Ожидаем пустой список, так как элементов недостаточно для среза
        expected_result = []
        
        # Ожидаем 0 элементов в результате
        expected_count = 0
        
        # Вызываем тестируемую функцию
        result, count = solve(receipts)
        
        # Проверяем, что результат соответствует ожиданиям
        self.assertEqual(result, expected_result)
        # Проверяем, что количествол элементов соответствует ожиданиям
        self.assertEqual(count, expected_count)
# Тест для случая когда функция вернула бы пустой список
    def test_edge_case_empty_list(self):
        """Проверка пустого списка"""
        # Пустой список на входе
        receipts = []
        
        # Ожидаем пустой результат
        expected_result = []
        expected_count = 0
        
        # Вызываем функцию
        result, count = solve(receipts)
        
        # Проверяем результаты
        self.assertEqual(result, expected_result)
        self.assertEqual(count, expected_count)    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Тесты в которых ожидаеться намеренное падение теста, 
#то есть тесты функция НЕ ПРОЙДЁТ!!.
    def test_non_list_input(self):
        """Проверка передачи не-списка (ожидается падение)"""
        with self.assertRaises(TypeError):
            # Пытаемся передать строку вместо списка
            solve("123,145,346")
    def test_dict_input(self):
        """Проверка передачи словаря вместо списка (ожидается исключение AssertionError: TypeError not raised)"""
        with self.assertRaises(TypeError):
            solve({"a": 1, "b": 2})
    def test_none_input(self):
        """Проверка передачи None вместо списка (ожидается исключение)"""
        with self.assertRaises(TypeError):
            solve(None)    
if __name__ == '__main__':
    unittest.main()