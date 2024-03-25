import requests
import json


session = requests.Session()
url = None
is_logged_in = False

def input_with_prompt(prompt):
    user_input = input(prompt).strip()
    while not user_input:
        print("Input cannot be empty. Please try again.")
        user_input = input(prompt).strip()
    return user_input

def login():
    global url, session, is_logged_in
    username = input_with_prompt("Enter username: ")
    password = input_with_prompt("Enter password: ")
    response = session.post(f"{url}/api/login", data={"username": username, "password": password})
    if response.status_code == 200:
        print("Login successful.")
        is_logged_in = True 
    else:
        print(f"Login failed with status code: {response.status_code}")
        is_logged_in = False

def logout():
    global session, is_logged_in

    if not is_logged_in:
        print("Please login first.")
        return
    session = requests.Session()
    is_logged_in = False
    print("Logged out successfully.")

def post_story():
    global url, session, is_logged_in

    if not is_logged_in:
        print("Please login first.")
        return

    headline = input_with_prompt("Enter headline: ")
    category = input_with_prompt("Enter category: ")
    region = input_with_prompt("Enter region: ")
    details = input_with_prompt("Enter details: ")

    story_data = {
        "headline": headline,
        "category": category,
        "region": region,
        "details": details
    }

    response = session.post(f"{url}/api/stories", json=story_data)
    if response.status_code == 201:
        print("Story posted successfully.")
    else:
        print(f"Failed to post story with status code: {response.status_code}")

def delete_story():
    global url, session, is_logged_in

    if not is_logged_in:
        print("Please login first.")
        return

    story_key = input_with_prompt("Enter story key to delete: ")
    response = session.delete(f"{url}/api/stories/{story_key}")

    if response.status_code == 200:
        print("Story deleted successfully.")
    else:
        print(f"Failed to delete story with status code: {response.status_code}")

def list():
    try:    
        response = requests.get("https://newssites.pythonanywhere.com/api/directory/")
        result = response.json()
        result = "\n".join(
            [f"{i['agency_name']:50} - {i['agency_code']:20} - {i['url']}" for i in result]
        )

        print(result)
    except Exception as e:
        print("Get agencies error: ", e)

def fetch_news():
    global url, session
    response = session.get(f"{url}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        for story in stories:
            print(f"Headline: {story.get('headline')}")
            print(f"Category: {story.get('category')}")
            print(f"Region: {story.get('region')}")
            print(f"Details: {story.get('details')}\n")
    else:
        print(f"Failed to fetch news with status code: {response.status_code}")


def main():
    global url
    url = input_with_prompt("Enter the base URL of the news service: ")

    while True:
        command = input("\nEnter command (login, logout, post, news, list, delete, exit): ").strip().lower()
        if command in ["login", "logout", "post", "news", "list", "delete", "exit"]:
            if command == "login":
                login()
            elif command == "logout":
                logout()
            elif command == "post":
                post_story()
            elif command == "news":
                fetch_news()
            elif command == "list":
                list()
            elif command == "delete":
                delete_story()
            elif command == "exit":
                break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
