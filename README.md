# SSD Settings Clean

Um aplicativo Python moderno para monitoramento de desempenho do sistema em tempo real, com foco em SSDs e recursos do sistema.

## Funcionalidades

- Monitoramento em tempo real de CPU, RAM e Disco
- Gráficos dinâmicos de uso dos recursos
- Interface moderna e intuitiva
- Análise detalhada do sistema
- Monitoramento de processos
- Limpeza de arquivos temporários
- Detecção de programas inativos
- Otimização do sistema

## Requisitos do Sistema

- Windows 10/11
- Python 3.8 ou superior (apenas para desenvolvimento)
- Acesso de administrador (para algumas funcionalidades)

## Download e Instalação

### Usuários
1. Baixe a última versão do executável na [página de releases](https://github.com/JoaoSantosCodes/SSD-Settings-Clean/releases)
2. Execute o arquivo `SSD Settings Clean.exe`
3. Se necessário, conceda permissões de administrador

### Desenvolvedores

1. Clone o repositório:
```bash
git clone https://github.com/JoaoSantosCodes/SSD-Settings-Clean.git
cd SSD-Settings-Clean
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

### Executável
Simplesmente execute o arquivo `SSD Settings Clean.exe` na pasta onde você o baixou.

### Código Fonte
1. Ative o ambiente virtual (se estiver usando):
```bash
venv\Scripts\activate  # Windows
```

2. Execute o aplicativo:
```bash
python src/main.py
```

## Criando o Executável

Para criar seu próprio executável:

1. Execute o script de build:
```bash
build.bat
```

2. O executável será criado na pasta `release`

## Estrutura do Projeto

```
SSD-Settings-Clean/
├── src/
│   ├── main.py       # Arquivo principal do aplicativo
│   ├── utils.py      # Funções utilitárias
│   └── cleaner.py    # Funções de limpeza e otimização
├── build_config.spec # Configuração do PyInstaller
├── build.bat        # Script de build
├── requirements.txt  # Dependências do projeto
└── README.md        # Este arquivo
```

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests.

## Licença

Este projeto está licenciado sob a MIT License. 