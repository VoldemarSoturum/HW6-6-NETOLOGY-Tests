# Для запуска теста находясь в одной дирректории с ним 
# pytest EX1-3_PyTest_test.py -v --tb=line

import pytest
from ex13 import get_courses_list, analyze_courses

@pytest.fixture
def courses_data():
    """Фикстура с тестовыми данными курсов"""
    return get_courses_list()

def test_data_preparation(courses_data):
    """Тест подготовки данных"""
    # Проверяем, что получили список из 4 курсов
    assert len(courses_data) == 4
    
    # Проверяем структуру данных первого курса
    assert isinstance(courses_data[0], dict)
    assert "title" in courses_data[0]
    assert "mentors" in courses_data[0]
    assert "duration" in courses_data[0]
    
    # Проверяем конкретные значения первого курса
    assert courses_data[0]["title"] == "Java-разработчик с нуля"
    assert courses_data[0]["duration"] == 14
    assert len(courses_data[0]["mentors"]) == 21

def test_analysis_results(courses_data):
    """Тест анализа корреляции между продолжительностью и количеством преподавателей"""
    result = analyze_courses(courses_data)
    
    # Проверяем правильность сортировки по длительности
    assert result["duration_order"] == [2, 0, 1, 3], (
        f"Ожидался порядок [2, 0, 1, 3], получено {result['duration_order']}"
    )
    
    # Проверяем правильность сортировки по количеству преподавателей
    assert result["mentors_order"] == [2, 3, 1, 0], (
        f"Ожидался порядок [2, 3, 1, 0], получено {result['mentors_order']}"
    )
    
    # Проверяем вывод о наличии корреляции
    assert result["has_correlation"] is False, (
        "Ожидалось отсутствие корреляции между продолжительностью и количеством преподавателей"
    )

@pytest.mark.parametrize("index, expected_duration, expected_mentors_count", [
    (0, 14, 21),  # Java-разработчик
    (1, 20, 16),  # Fullstack-разработчик
    (2, 12, 12),  # Python-разработчик
    (3, 20, 12)   # Frontend-разработчик
])
def test_course_details(courses_data, index, expected_duration, expected_mentors_count):
    """Параметризованный тест для проверки деталей каждого курса"""
    course = courses_data[index]
    assert course["duration"] == expected_duration, (
        f"Для курса {course['title']} ожидалась продолжительность {expected_duration}, получено {course['duration']}"
    )
    assert len(course["mentors"]) == expected_mentors_count, (
        f"Для курса {course['title']} ожидалось {expected_mentors_count} преподавателей, получено {len(course['mentors'])}"
    )