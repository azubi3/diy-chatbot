echo "Creating custom Docker network 'ollama_network'"
docker network create ollama_network

echo "Installing ollama docker"
docker run -d --restart=always --name ollama --network ollama_network -p 11434:11434 ollama/ollama serve

echo "Pulling model file"
docker exec ollama ollama pull hf.co/bartowski/gemma-2-2b-it-GGUF:Q6_K

echo "Build docker image"
docker build -t fastapi-chat app

echo "Starting webserver at port 80"
docker run -d --restart unless-stopped --name fastapi_chat --network ollama_network -p 80:80 fastapi-chat
