# Assistente Virtual Clotilde

Assistente de voz em Python que escuta comandos em português, responde por síntese de fala e executa tarefas como lembretes, pesquisa no Google, informar hora/data e ler eventos de uma agenda em Excel.

## Requisitos

- Python 3.8 ou superior
- Recomendação: usar Python 3.11 (melhor compatibilidade com `PyAudio` e `playsound` no Windows)
- Microfone
- Conexão com a internet (reconhecimento de voz via Google)
- Google Chrome instalado (pesquisas no navegador; o caminho é configurável no código)
- Windows: vozes SAPI disponíveis no sistema para o `pyttsx3`

## Instalação

Clone o repositório e, na pasta do projeto, crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Instalação manual (alternativa)

```bash
pip install pyttsx3 SpeechRecognition playsound numpy librosa matplotlib seaborn pandas openpyxl PyAudio gTTS
```

### Nota sobre o PyAudio no Windows

Se `pip install PyAudio` falhar, tente instalar um wheel compatível com sua versão do Python ou use ferramentas como `pipwin`:

```bash
pip install pipwin
pipwin install pyaudio
```

## Testar a instalação

```bash
python teste_instalacao.py
```

O script verifica se as bibliotecas principais importam corretamente e testa recursos de áudio.

## Executar a assistente

```bash
python Clotilde_assistente.py
```

Acione dizendo **"Clotilde"** seguido do comando, por exemplo: *"Clotilde, que horas são"*.

## Estrutura do projeto

| Arquivo / pasta | Descrição |
|-----------------|-----------|
| `Clotilde_assistente.py` | Loop principal: escuta, reconhecimento de voz e comandos |
| `teste_instalacao.py` | Verificação das bibliotecas instaladas |
| `modules/comandos_respostas.py` | Listas de comandos de voz e respostas da assistente |
| `modules/carrega_agenda.py` | Leitura de eventos do dia a partir de `agenda.xlsx` |

## Configuração

1. **Chrome** — Em `Clotilde_assistente.py`, ajuste `chrome_path` se não estiver no Windows ou se o Chrome estiver em outro diretório.
2. **Agenda** — Coloque o arquivo `agenda.xlsx` na raiz do projeto. A planilha deve conter as colunas: `data`, `hora`, `descricao`, `responsavel`.
3. **Gravações** — Crie a pasta `recordings/` na raiz do projeto (o assistente grava `speech.wav` ao ouvir o microfone).
4. **Áudios** — Mantenha os arquivos de som referenciados no código (por exemplo `n2.mp3`) na pasta do projeto.

## Funcionalidades

- Listar o que a assistente sabe fazer
- Gravar e ler lembretes em `anotacao.txt`
- Pesquisar no Google
- Informar hora e data atuais
- Ler compromissos do dia na agenda (Excel)
- Modo de análise de emoção: planejado no código (`librosa`, etc.), ainda não finalizado

## Dependências (resumo)

| Biblioteca | Uso |
|------------|-----|
| `pyttsx3` | Síntese de voz |
| `SpeechRecognition` | Captura e reconhecimento de fala |
| `playsound` | Reprodução de arquivos de áudio |
| `pandas` + `openpyxl` | Leitura da agenda em Excel |
| `PyAudio` | Acesso ao microfone |
| `gTTS` | Testes de texto para fala (`teste_instalacao.py`) |
| `numpy`, `librosa`, `matplotlib`, `seaborn` | Análise de áudio / modo emoção (em desenvolvimento) |

Módulos da biblioteca padrão do Python (`datetime`, `random`, `webbrowser`) não precisam ser instalados via pip.
