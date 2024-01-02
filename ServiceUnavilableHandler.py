import random
import requests
import vars as v

def make_request(url, headers):
    max_retries = 5  # You can adjust the maximum number of retries
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=v.HEADERS, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503:
                # Handle 503 error (Service Unavailable) by retrying
                retry_count += 1
                print(f"Retrying... Retry count: {retry_count}")
                headers['User-Agent'] = random.choice(v.user_agents)
            else:
                # Handle other HTTP errors
                print(f"HTTPError: {e}")
                break
        except requests.exceptions.RequestException as e:
            # Handle other request exceptions
            print(f"RequestException: {e}")
            break

    # Handle the case when all retries are exhausted
    print("Maximum retries reached. Request failed.")
    return None



