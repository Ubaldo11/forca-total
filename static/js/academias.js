document.addEventListener("DOMContentLoaded", () => {
    const statusText = document.getElementById("status");
    const listaContainer = document.getElementById("lista-academias");
    const erroContainer = document.getElementById("container-erro");

    // 1. Verifica se a API é suportada pelo navegador
    if (!navigator.geolocation) {
        statusText.innerText = "Geolocalização não é suportada pelo seu navegador.";
        return;
    }

    // 2. Alerta caso o ambiente não seja seguro (HTTPS ou Localhost)
    if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        statusText.innerText = "A geolocalização exige uma conexão segura (HTTPS ou localhost).";
        return;
    }

    const endpointUrl = statusText.dataset.url;

    const opcoes = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
    };

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
                listaContainer.innerHTML = "";

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
                console.error("Erro na requisição Fetch:", err);
                statusText.innerText = "Erro ao se comunicar com o servidor.";
            });
        },
        (error) => {
            console.warn("Erro no getCurrentPosition:", error);
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    statusText.innerText = "Permissão negada. Verifique os bloqueios de localização na barra de endereço do navegador.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    statusText.innerText = "Sinal de localização indisponível no momento.";
                    break;
                case error.TIMEOUT:
                    statusText.innerText = "Tempo limite esgotado ao tentar obter a localização.";
                    break;
                default:
                    statusText.innerText = "Erro ao obter localização.";
                    break;
            }
        },
        opcoes
    );
});