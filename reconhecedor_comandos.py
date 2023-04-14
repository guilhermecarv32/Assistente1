import speech_recognition as sr
from nltk import word_tokenize, corpus
from unidecode import unidecode
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "D:\\Users\\User\\Desktop\\Guilherme\\python vscode\\ReconhecimentoVoz\\config.json"



def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes
    
    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))
    
    with open(CAMINHO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)
        
        nome_assistente = configuracao["nome"]
        acoes = configuracao["acoes"]
        
        arquivo_configuracao.close()
    
def escutar_comando():
    global reconhecedor
    
    comando = None
    
    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)
        
        print("Diga o comando...")
        fala = reconhecedor.listen(fonte_audio)
        
        try:
            comando = reconhecedor.recognize_google(fala, language = IDIOMA_FALA)
            print(comando)
        except sr.UnknownValueError:
            pass
    
    return comando

def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada
    
    tokens_filtrados = []
    for token in tokens:
        token_sem_acento = unidecode(token) 
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)
    
    return tokens_filtrados

# função para eliminar as palavras de parada e acentos
def eliminar_palavras_de_parada(tokens):
    palavras_de_parada = ['o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas']
    tokens_sem_acentos = [unidecode(palavra) for palavra in tokens]
    return [palavra for palavra in tokens_sem_acentos if palavra.lower() not in palavras_de_parada]

# função para reconhecer o comando
def reconhecer_comando(tokens):
    with open('comandos.json', 'r') as arquivo:
        comandos = json.load(arquivo)
    for palavra in tokens:
        for comando in comandos:
            if unidecode.unidecode(palavra) in comando['sinonimos']:
                return {'nome': comando['nome'], 'objeto': comando['objeto']}
    return None

def tokenizar_comando(comando):
    global nome_assistente
    
    acao = None
    objeto = None
    
    tokens = word_tokenize(comando, IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras_de_parada(tokens)
        
        if len(tokens) >= 3:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                objeto = tokens[2].lower()
    
    return acao, objeto

def validar_comando(acao, objeto):
    global acoes
    
    valido = False
    
    if acao and objeto:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if objeto in acaoCadastrada["objeto"]:
                    valido = True
    
    return valido

def executar_comando(acao, objeto):
    print("Executando comando: ", acao, objeto)

if __name__ == '__main__':
    iniciar()
    
    continuar = True
    while continuar:
        try:
            comando = escutar_comando()
            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido = validar_comando(acao, objeto)
                if valido:
                    print("Comando válido")
                    executar_comando(acao, objeto)
                else:
                    print("Não entendi o comando. Diga novamente...")
        except KeyboardInterrupt:
            print("Tchau!")
            
            continuar = False