import requests
import json

# 全局变量
token = None
url = None

def get_token(base_url, username, password):
    response = requests.post(f"{base_url}/api/login", data={"username": username, "password": password})
    if response.status_code == 200:
        try:
            json_response = response.json()
            return json_response.get('token')
        except ValueError:
            print("Error: Unable to decode JSON from login response.")
            return None
    else:
        print(f"Login failed with status code: {response.status_code}")
        return None

def handle_list(base_url, token):
    """处理并显示新闻服务列表"""
    headers = {"Authorization": f"Token {token}"} if token else {}
    response = requests.get(f"{base_url}/api/directory", headers=headers)
    
    try:
        if response.status_code == 200:
            services = response.json()
            formatted_result = "\n".join([
                f"{service['agency_name']:50} - {service['agency_code']:20} - {service['url']}"
                for service in services
            ])
            print(formatted_result)
        else:
            print(f"Failed to fetch services with status code: {response.status_code}")
    except Exception as e:
        print("Get agencies error: ", e)

def logout():
    global token
    token = None
    print("Logged out successfully.")

def post_story():
    global token, url
    if not token:
        print("Please login first.")
        return

    headline = input("Enter headline: ")
    category = input("Enter category: ")
    region = input("Enter region: ")
    details = input("Enter details: ")

    story_data = {
        "headline": headline,
        "category": category,
        "region": region,
        "details": details
    }

    headers = {"Authorization": f"Token {token}"}
    response = requests.post(f"{url}/api/stories", headers=headers, json=story_data)
    if response.status_code == 201:
        print("Story posted successfully.")
    else:
        print(f"Failed to post story with status code: {response.status_code}")

def list_services():
    global url
    response = requests.get(f"{url}/api/directory")
    if response.status_code == 200:
        services = response.json()
        for service in services:
            print(service) 
    else:
        print(f"Failed to list services with status code: {response.status_code}")

def delete_story(story_key):
    global token, url
    if not token:
        print("Please login first.")
        return

    response = requests.delete(f"{url}/api/stories/{story_key}", headers={"Authorization": f"Token {token}"})
    if response.status_code == 200:
        print("Story deleted successfully.")
    else:
        print(f"Failed to delete story with status code: {response.status_code}")


def fetch_news():
    global token, url
    response = requests.get(f"{url}/api/stories", headers={"Authorization": f"Token {token}"} if token else {})
    if response.status_code == 200:
        stories = response.json()
        for story in stories:
            print(story)
    else:
        print(f"Failed to fetch news with status code: {response.status_code}")


def list():
    try:    
        response = requests.get("https://newssites.pythonanywhere.com/api/directory/")
        if response.status_code != 200:
            print(f"Failed to fetch agencies with status code: {response.status_code}")
        agencies = response.json()
    
        if agencies:
            agency = "\n".join(
                [f"Agency Name: {i['agency_name']}\nAgency Code: {i['agency_code']}\nURL: {i['url']}\n" for i in agencies]
            )
            print(agency)
        else:
            print("No agencies found.")
    except Exception as e:
        print("Get agencies error: ", e)

def main():
    global token, url
    url = input("Enter the base URL of the news service: ")

    while True:
        command = input("Enter command (login, logout, post, news, list, delete, exit): ").strip().lower()
        if command == "login":
            username = input("Enter username: ")
            password = input("Enter password: ")
            token = get_token(url, username, password)
        elif command == "logout":
            logout()
        elif command == "post":
            post_story()
        elif command == "news":
            fetch_news()
        elif command == "list":
            list()
        elif command.startswith("delete"):
            story_key = command.split()[-1]
            delete_story(story_key)
        elif command == "exit":
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
