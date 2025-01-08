# command to move to dir in wsl 
cd "/mnt/c/Users/z004x5km/OneDrive - Siemens AG/Desktop/Prompting tests"

# command to create a venv 
python -m nameOfEnv pathOfEnv
source .pathTovenv/bin/activate
python -m pip install packageName

# models to test
## open source
llama3.2
qwen2.5
phi3.5
mistral
deepseek-coder-v2
codegemma
gemma

# proprietary 
gpt4
gemini (if possible)
claude

ollama pull phi3.5; ollama pull mistral; ollama pull deepseek-coder-v2; ollama pull codegemma; ollama pull gemma

ollama pull codegemma:7b; ollama pull codegemma:2b;
ollama pull gemma:7b; ollama pull gemma:2b;
ollama pull gemma2:2b; ollama pull gemma2:9b; ollama pull gemma2:27b;
ollama pull mistral:7b;
ollama pull phi3.5:3.8b;
ollama pull llama3.1:70b; ollama pull llama3.1:8b; 
ollama pull llama3.2:3b; ollama pull llama3.2:1b; 

ollama pull qwen2.5:32b; ollama pull qwen2.5:14b; ollama pull qwen2.5:7b; ollama pull qwen2.5:3b; ollama pull qwen2.5:72b