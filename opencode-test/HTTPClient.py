import requests


def demo_get() -> None:
    print("--- GET ---")
    resp = requests.get("https://httpbin.org/get")
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}\n")


def demo_get_with_params() -> None:
    print("--- GET with query params ---")
    resp = requests.get("https://httpbin.org/get", params={"key": "value", "foo": "bar"})
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}\n")


def demo_post() -> None:
    print("--- POST ---")
    resp = requests.post("https://httpbin.org/post", data={"name": "Alice"})
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}\n")


def demo_put() -> None:
    print("--- PUT ---")
    resp = requests.put("https://httpbin.org/put", json={"key": "updated_value"})
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}\n")


def demo_delete() -> None:
    print("--- DELETE ---")
    resp = requests.delete("https://httpbin.org/delete")
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}\n")


def demo_headers() -> None:
    print("--- GET with custom headers ---")
    resp = requests.get(
        "https://httpbin.org/headers",
        headers={"User-Agent": "MyClient/1.0", "Accept": "application/json"},
    )
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.json()}\n")


def demo_conditional_get() -> None:
    print("--- GET with If-Modified-Since ---")
    headers = {"If-Modified-Since": "Mon, 01 Jan 2024 00:00:00 GMT"}
    resp = requests.get("https://httpbin.org/response-headers", headers=headers)
    print(f"Status: {resp.status_code}")
    print(f"Headers: {dict(resp.headers)}\n")


def main() -> None:
    demo_get()
    demo_get_with_params()
    demo_post()
    demo_put()
    demo_delete()
    demo_headers()
    demo_conditional_get()


if __name__ == "__main__":
    main()
