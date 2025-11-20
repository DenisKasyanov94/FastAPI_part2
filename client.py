import requests
import json

BASE_URL = "http://localhost:8000"


def test_create_advertisement():
    """Тест создания объявления"""
    url = f"{BASE_URL}/advertisement"
    data = {
        "title": "Продам MacBook Pro",
        "description": "2022 года, отличное состояние",
        "price": 150000,
        "author": "Анна"
    }

    response = requests.post(url, json=data)
    print("=== CREATE ADVERTISEMENT ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get("id")


def test_get_all_advertisements():
    """Тест получения всех объявлений"""
    url = f"{BASE_URL}/advertisement/"

    response = requests.get(url)
    print("\n=== GET ALL ADVERTISEMENTS ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_get_advertisement(advertisement_id):
    """Тест получения объявления по ID"""
    url = f"{BASE_URL}/advertisement/{advertisement_id}"

    response = requests.get(url)
    print(f"\n=== GET ADVERTISEMENT {advertisement_id} ===")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Error: {response.json()}")


def test_update_advertisement(advertisement_id):
    """Тест обновления объявления"""
    url = f"{BASE_URL}/advertisement/{advertisement_id}"
    data = {
        "price": 140000,
        "title": "Продам MacBook Pro (цена снижена)"
    }

    response = requests.patch(url, json=data)
    print(f"\n=== UPDATE ADVERTISEMENT {advertisement_id} ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def test_search_advertisements():
    """Тест поиска объявлений"""
    url = f"{BASE_URL}/advertisement/"
    params = {
        "title": "MacBook",
        "min_price": 100000
    }

    response = requests.get(url, params=params)
    print("\n=== SEARCH ADVERTISEMENTS ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_delete_advertisement(advertisement_id):
    """Тест удаления объявления"""
    url = f"{BASE_URL}/advertisement/{advertisement_id}"

    response = requests.delete(url)
    print(f"\n=== DELETE ADVERTISEMENT {advertisement_id} ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    print("🚀 Testing Advertisement API...")

    try:
        # 1. Создаем объявление
        ad_id = test_create_advertisement()

        # 2. Получаем все объявления
        test_get_all_advertisements()

        # 3. Получаем конкретное объявление
        test_get_advertisement(ad_id)

        # 4. Обновляем объявление
        test_update_advertisement(ad_id)

        # 5. Проверяем обновленное объявление
        test_get_advertisement(ad_id)

        # 6. Ищем объявления
        test_search_advertisements()

        # 7. Удаляем объявление (раскомментируйте если нужно)
        # test_delete_advertisement(ad_id)

        print("\n✅ All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure Docker containers are running.")
    except Exception as e:
        print(f"❌ Error: {e}")