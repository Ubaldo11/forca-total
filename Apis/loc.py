import requests

# ===== SUA API KEY DO GEOAPIFY =====
GEOAPIFY_KEY = "f32fac84e53d4bd38835ba1dbb4b095f"


def localizacao_por_ip():
    """
    Descobre a localização aproximada do usuário pelo IP.
    Usa a API ip-api.com (gratuita, sem chave).
    """
    try:
        # ip-api.com/json/ sem argumento usa o IP de quem faz a requisição
        resposta = requests.get("http://ip-api.com/json/", timeout=10)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            
            # A API retorna status "success" se deu certo
            if dados.get("status") == "success":
                return {
                    "cidade": dados.get("city"),
                    "regiao": dados.get("regionName"),
                    "pais": dados.get("country"),
                    "lat": dados.get("lat"),
                    "lon": dados.get("lon")
                }
    except requests.exceptions.RequestException as erro:
        print(f"Erro ao obter localização por IP: {erro}")
    
    return None


def buscar_academias(latitude, longitude, raio_metros=5000):
    """
    Busca academias próximas usando Geoapify Places API.
    """
    url = "https://api.geoapify.com/v2/places"
    
    params = {
        "categories": "sport.fitness",
        "limit": 20,
        "apiKey": GEOAPIFY_KEY,
        "lat": latitude,
        "lon": longitude
    }
    
    try:
        print(f"Buscando academias em lat={latitude}, lon={longitude}, raio={raio_metros}m")
        
        resposta = requests.get(url, params=params, timeout=15)
        print(f"Status: {resposta.status_code}")
        
        if resposta.status_code == 200:
            dados = resposta.json()
            features = dados.get("features", [])
            print(f"Encontrados: {len(features)} elementos")
            
            academias = []
            for f in features:
                props = f.get("properties", {})
                coords = f.get("geometry", {}).get("coordinates", [None, None])
                
                academias.append({
                    "nome": props.get("name", "Academia sem nome"),
                    "endereco": props.get("formatted", ""),
                    "telefone": props.get("phone", ""),
                    "site": props.get("website", ""),
                    "distancia": props.get("distance", 0),
                    "latitude": coords[1],
                    "longitude": coords[0]
                })
            
            return academias
        else:
            print(f"Erro: {resposta.text}")
            return None
            
    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexão: {erro}")
        return None