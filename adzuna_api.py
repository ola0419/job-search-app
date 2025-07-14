import requests

APP_ID =  "156c72e7"
APP_KEY = "28684d5f8f8137a03814727afbba1edd"

def fetch_jobs(keyword, location):
    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": keyword,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        jobs = []

        for item in data.get("results", []):
            jobs.append({
                "title": item.get("title", "N/A"),
                "company": item.get("company", {}).get("display_name", "N/A"),
                "location": item.get("location", {}).get("display_name", "N/A"),
                "salary": f"£{item.get('salary_min', 0):,.0f} - £{item.get('salary_max', 0):,.0f}"
                          if item.get("salary_min") and item.get("salary_max") else "Not listed"
            })

        return jobs
    else:
        return []
