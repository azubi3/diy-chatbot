echo "Installing ollama docker"
docker run -d -v ollama:/root/.ollama -p 127.0.0.1:11434:11434 --name ollama ollama/ollama

echo "Pulling model file"
docker exec ollama ollama pull hf.co/bartowski/gemma-2-2b-it-GGUF:Q6_K

echo "Start ollama"
docker exec -it ollama ollama serve

echo "Build docker image"
docker build -t fastapi-chat .

echo "Starting webserver under 127.0.0.1:8000"
docker run -d --restart unless-stopped -p 8000:8000 fastapi-chat