import requests

URL = "https://www.googleapis.com/youtube/v3/playlistItems"


def buscar_videos_playlist(playlist_id, api_key):
    """Retorna (lista_de_videos, erro)."""
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key,
    }

    try:
        resp = requests.get(URL, params=params, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None, "Erro de conexão com o YouTube."

    if resp.status_code != 200:
        print(f"Erro: {resp.status_code} - {resp.text}")
        if resp.status_code == 404:
            return None, "Playlist não encontrada. Confira o ID e se ela é pública."
        if resp.status_code == 403:
            return None, "Chave inválida, API não ativada ou cota esgotada."
        return None, f"Erro do YouTube ({resp.status_code})."

    videos = []
    for item in resp.json().get("items", []):
        snippet = item.get("snippet", {})
        titulo = snippet.get("title")
        # vídeos apagados ou privados aparecem assim, então pulamos
        if titulo in ("Deleted video", "Private video"):
            continue
        thumbs = snippet.get("thumbnails", {})
        videos.append({
            "titulo": titulo,
            "canal": snippet.get("videoOwnerChannelTitle", ""),
            "video_id": snippet.get("resourceId", {}).get("videoId"),
            "imagem": (thumbs.get("medium") or thumbs.get("default") or {}).get("url"),
        })
    return videos, None