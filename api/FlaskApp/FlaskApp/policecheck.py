import re
import requests


def check(spz):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        '__EVENTVALIDATION': ['/wEWBQKm3cDnDwLQsb3+BgK9peeFDwLv+PyjBAL4oIjjDcu7AaG9QTibgeZspJRuAkfQh0hz'],
        '__VIEWSTATE': ['/wEPDwULLTEzNzIzMjY0MDMPZBYCZg9kFgICBw9kFgICAQ9kFgoCBA8PZBYCHgpvbmtleXByZXNzBTZyZXR1cm4gb25LZXlwcmVzcyhldmVudCwnY3RsMDBfQXBwbGljYXRpb25fY21kSGxlZGVqJylkAgYPD2QWAh8ABTZyZXR1cm4gb25LZXlwcmVzcyhldmVudCwnY3RsMDBfQXBwbGljYXRpb25fY21kSGxlZGVqJylkAhQPDxYEHgRUZXh0BRxDZWxrb3bDvSBwb8SNZXQgesOhem5hbcWvOiAxHgdWaXNpYmxlZ2RkAhUPDxYEHwEFUk5hIHrDoWtsYWTEmyB6YWRhbsO9Y2gga3JpdMOpcmnDrSA8c3Ryb25nPm5lYnlsIG5hbGV6ZW48L3N0cm9uZz4gxb7DoWRuw70gesOhem5hbS4fAmhkZAIZDw8WAh8BBUFEYXRhYsOhemUgYnlsYSBuYXBvc2xlZHkgYWt0dWFsaXpvdsOhbmEgPGI+MTUuIFNlcHRlbWJlciAyMDE3PC9iPmRkZATCu8EvglSvzIGh3pn8I8pbhq3x'],
        '__VIEWSTATEGENERATOR': ['2FEDDD51'],
        'ctl00$Application$CurrentPage': ['1'],
        'ctl00$Application$cmdHledej': ['Vyhledat'],
        'ctl00$Application$txtSPZ': spz
    }

    url = "http://aplikace.policie.cz/patrani-vozidla/default.aspx"

    r = requests.post(url, headers=headers, data=data)

    pattern = "Pořadí"
    try:
        m = re.search(pattern, r.text)
        try:
            m.group(0)
            out = {'value': 'found', 'description': 'Plate number found in policie.cz'}
        except Exception:
            out = {'value': 'ok', 'description': 'Place number not found in policie.cz'}
    except Exception:
        out = {'value': 'unknown', 'description': 'No data from policie.cz'}

    return out
