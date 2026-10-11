import urllib.request
import urllib.error
import json
import sys

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5173"
API_URL = BASE_URL + "/api"

def login(role):
    req = urllib.request.Request(f"{API_URL}/demo/login", data=json.dumps({"role": role}).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as response:
        return response.headers.get('Set-Cookie'), json.loads(response.read().decode('utf-8')).get('csrf')

def get_ticket(cookie, ticket_id):
    req = urllib.request.Request(f"{API_URL}/tickets/{ticket_id}", headers={"Cookie": cookie}, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode('utf-8')}

def update_source(cookie, csrf, ticket_id, source_id):
    req = urllib.request.Request(f"{API_URL}/tickets/{ticket_id}/source", data=json.dumps({"source_id": source_id}).encode('utf-8'), headers={"Cookie": cookie, "Content-Type": "application/json", "X-CSRF-Token": csrf}, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode('utf-8')}

def main():
    print("1. Проверка: просмотрщик не может изменить источник (ожидается 403)...")
    cookie_viewer, csrf_viewer = login("viewer")
    res = update_source(cookie_viewer, csrf_viewer, 101, 2)
    assert res.get("error") == 403, f"FAILED: Ожидался 403, получено {res}"
    print("   PASSED")

    print("2. Проверка: заявка без источника (id=103) возвращает source: null...")
    cookie_editor, csrf_editor = login("editor")
    res = get_ticket(cookie_editor, 103)
    assert "error" not in res, f"FAILED: Получена ошибка {res}"
    assert res.get("ticket", {}).get("source") is None, f"FAILED: Ожидался null, получено {res['ticket']['source']}"
    print("   PASSED")

    print("3. Проверка: строковое значение источника отклоняется (ожидается 400)...")
    res = update_source(cookie_editor, csrf_editor, 101, "2")
    assert res.get("error") == 400, f"FAILED: Ожидался 400 для строки, получено {res}"
    print("   PASSED")

    print("4. Проверка: архивная заявка (id=104) недоступна для изменения (ожидается 403)...")
    res = update_source(cookie_editor, csrf_editor, 104, 2)
    assert res.get("error") == 403, f"FAILED: Ожидался 403 для архива, получено {res}"
    print("   PASSED")

    print("\n✅ Все автоматические проверки пройдены успешно!")

if __name__ == "__main__":
    main()