document.addEventListener("DOMContentLoaded", () => {
    const statusText = document.getElementById("status");
    const listaContainer = document.getElementById("lista-academias");
    const erroContainer = document.getElementById("container-erro");

    if (!navigator.geolocation) {
        statusText.innerText = "Geolocalização não é suportada pelo seu navegador.";
        return;
    }

    // Lê a URL do endpoint configurada no dataset do elemento HTML
    const endpointUrl = statusText.dataset.url;

    navigator.geolocation.getCurrentPosition(
        (position) => {
            statusText.innerText = "Localização obtida! Buscando academias...";

            fetch(endpointUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    statusText.innerText = "";
                    erroContainer.innerText = data.erro;
                    erroContainer.style.display = "block";
                    return;
                }

                statusText.innerText = "Exibindo academias próximas à sua posição exata.";
                listaContainer.innerHTML = ""; // Limpa a lista

                // Renderiza cada academia recebida no JSON
                data.academias.forEach(academia => {
                    const card = document.createElement("div");
                    card.className = "academia";

                    let conteudo = `<h2>${academia.nome}</h2>`;
                    if (academia.endereco) conteudo += `<p>${academia.endereco}</p>`;
                    if (academia.telefone) conteudo += `<p>Telefone: ${academia.telefone}</p>`;
                    if (academia.site) conteudo += `<p>Site: <a href="${academia.site}" target="_blank">${academia.site}</a></p>`;
                    if (academia.distancia) conteudo += `<p>Distância: ${Math.round(academia.distancia)} m</p>`;

                    card.innerHTML = conteudo;
                    listaContainer.appendChild(card);
                });
            })
            .catch(err => {
                console.error(err);
                statusText.innerText = "Erro ao se comunicar com o servidor.";
            });
        },
        (error) => {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    statusText.innerText = "Você precisa permitir o acesso à localização no navegador para ver as academias.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    statusText.innerText = "Informações de localização indisponíveis.";
                    break;
                case error.TIMEOUT:
                    statusText.innerText = "A requisição para obter a localização expirou.";
                    break;
                default:
                    statusText.innerText = "Erro ao obter localização.";
                    break;
            }
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
});