import requests

# Defina sua chave de API
api_key = 'EmyYSe_cQOUPGTzmIV4slJ39Q3RZ3HyTmkPYGhPLH_9Uq-OAJ6Y'

# URL para obter os torneios
url = 'https://api.pandascore.co/csgo/tournaments'

# Headers com o token de autenticação
headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json',
}

# Requisição para a API
response = requests.get(url, headers=headers)

# Verifique a resposta
if response.status_code == 200:
    tournaments = response.json()  # Converte a resposta para JSON
    
    # Exibe informações sobre cada torneio
    for tournament in tournaments:
        print(f"Tournament Name: {tournament['name']}")
        print(f"Tournament Slug: {tournament['slug']}")
        print(f"Tournament ID: {tournament['id']}")
        print(f"Tournament Start: {tournament['begin_at']}")
        print(f"Tournament End: {tournament['end_at']}")
        
        # Verifica se a chave 'status' existe antes de acessá-la
        if 'status' in tournament:
            print(f"Tournament Status: {tournament['status']}")
        else:
            print("Tournament Status: N/A")
        
        print(f"Prize Pool: {tournament.get('prizepool', 'N/A')}")
        
        # Exibe informações sobre as partidas, se existirem
        if 'matches' in tournament:
            for match in tournament['matches']:
                # Verifica se o time da FURIA está no match
                if 'FURIA' in match['name']:  # Supondo que o nome do time esteja na chave 'name'
                    print(f"  Match Name: {match['name']}")
                    print(f"  Match Status: {match['status']}")
                    print(f"  Match Scheduled At: {match['scheduled_at']}")
                    print(f"  Match Slug: {match['slug']}")
                    print(f"  Stream URL: {match['streams_list'][0]['raw_url'] if match['streams_list'] else 'No stream'}")
                    print("-----------")
else:
    print(f"Erro ao acessar a API: {response.status_code}")
    print(response.text)  # Exibe o conteúdo da resposta em formato de texto
