import requests
import json
from datetime import date

def fetch_trending():
    # Simple GitHub search API for AI repos created today
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': 'topic:ai created:>{}'.format(date.today().isoformat()),
        'sort': 'stars',
        'order': 'desc',
        'per_page': 5
    }
    headers = {'Accept': 'application/vnd.github.v3+json'}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json().get('items', [])
    except Exception as e:
        print('Error fetching:', e)
        return []

def extract_terms(items):
    terms = set()
    for item in items:
        name = item.get('name', '')
        desc = item.get('description') or ''
        topics = item.get('topics', [])
        # Combine name, description, topics
        for text in [name, desc, ' '.join(topics)]:
            for word in text.replace('-', ' ').replace('_', ' ').split():
                if len(word) > 2 and word.isalnum():
                    terms.add(word.lower())
    return sorted(terms)

def main():
    repos = fetch_trending()
    if not repos:
        print('No repos found today.')
        return
    terms = extract_terms(repos)
    print('\nNew AI terms from today\'s trending repos:')
    for t in terms:
        print('-', t)
    # Save to file
    with open('radar_today.json', 'w') as f:
        json.dump({'date': str(date.today()), 'terms': terms}, f, indent=2)

if __name__ == '__main__':
    main()
