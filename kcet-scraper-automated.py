import time
import requests
from bs4 import BeautifulSoup
import notify2

def main(old_text:list) -> list:

    page = requests.get("http://cetonline.karnataka.gov.in/kea")
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="ContentPlaceHolder1_Gridlatestannoc").find_all("a")
    text = [entry.text for entry in results]

    # For first execution
    if not old_text: return text

    # List of new posts
    diff = [entry for entry in text if entry not in old_text]

    # If no new posts, then return
    if not diff:
        print(f"No new posts at {time.strftime('%X')}")
        return text

    print(f"{len(diff)} new posts at {time.strftime('%X')}")
    print(diff[0])

    # Show notification for new posts
    notify2.init("KCET-bot")
    notification = notify2.Notification(f"{len(diff)} new posts in KEA website", diff[0])
    notification.set_timeout(notify2.EXPIRES_NEVER)
    notification.show()

    return text

if __name__ == "__main__":
    text = []
    while True:
        text = main(text)

        # Check for updates every 10 minutes
        time.sleep(10)
