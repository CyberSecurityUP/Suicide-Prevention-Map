import folium
import googlemaps
from googleapiclient.discovery import build

# Substitua YOUR_API_KEY pela sua chave de API do Google Cloud Platform
gmaps = googlemaps.Client(key="API KEY")

# Substitua YOUR_CSE_API_KEY pela sua chave de API da Pesquisa Personalizada e YOUR_CSE_ID pelo seu ID do mecanismo de pesquisa personalizado
google_search = build("customsearch", "v1", developerKey="api key")
cse_id = "CSE ID"

# Lista de consultas para buscar instituições de prevenção ao suicídio
queries = [
    "suicide prevention organizations",
    "suicide prevention centers",
    "suicide prevention help",
    "instituição de prevenção ao suicidio",
    "Suicide Prevention helpline",
    "Brazilian Suicide Prevention",
    "Nippon Foudation Suicide",
    "Suicide Prevention Foudation",
    "SPRC",
    "Mental Health Foudation",
    "Mental Health Organizations",
    "Mental Health Centers",
    "Russian Federation helplines",
    "asian suicide prevention organization",
    "suicide prevention japan",
    "suicide prevention brazilian",
    "instituição de saude mental",
    "saude mental brasil",
    "prevenção ao suicidio brasil",
]

instituicoes = []

for query in queries:
    # Busque informações usando a API de Pesquisa Personalizada do Google
    search_results = google_search.cse().list(q=query, cx=cse_id, num=10).execute()

    for item in search_results.get("items", []):
        name = item["title"]
        url = item["link"]

        # Tente obter informações de geolocalização usando a API do Google Places
        place_results = gmaps.places(query=f"{name} {url}")

        if place_results["results"]:
            place = place_results["results"][0]
            instituicoes.append(
                {
                    "nome": name,
                    "endereco": place["formatted_address"],
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"],
                    "telefone": place.get("formatted_phone_number", "Não disponível"),
                }
            )

# Crie um mapa com coordenadas iniciais e defina o nível de zoom
mapa = folium.Map(location=[0, 0], zoom_start=2)

# Adicione marcadores para cada instituição
for instituicao in instituicoes:
    folium.Marker(
        location=[instituicao["latitude"], instituicao["longitude"]],
        popup=f"{instituicao['nome']}<br>{instituicao['endereco']}<br>{instituicao['telefone']}",
        icon=folium.Icon(icon="university", prefix="fa"),
    ).add_to(mapa)

# Salve o mapa em um arquivo HTML
mapa.save("mapa_instituicoes_prevencao_suicidio.html")
