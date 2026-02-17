import urllib.request, json, ssl

def update_fpl_data():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    try:
        with urllib.request.urlopen(url, context=ctx) as response:
            data = json.loads(response.read().decode())
            with open('fpl_data.json', 'w') as f:
                json.dump(data, f)
            print("fpl_data.json updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_fpl_data()
