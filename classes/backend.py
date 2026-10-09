import requests
moedas = { # Dicionário chave-valor para os tipos de moeda
    'USD': 'Dolár Americano',
    'EUR': 'Euro',
    'GBP': 'Libra Eterlina',
    'ARS': 'Peso Argentino'
}

def converter_moeda(valor_reais, cotacao):
    if cotacao > 0:
        resultado = valor_reais / cotacao

        return resultado
    else: 
        return 'Cotação Inválida'

def validar_valor(valor):
    try: # Tente isso
        valor_convertido = float(valor)

        if valor_convertido > 0:
            return valor_convertido
        else:
            return 'O Valor Deve Ser Maior Que Zero'
        
    except: # Se acontecer um erro, faça isso
        return 'Valor Inválido'

def validar_moeda(codigo): # Função para verificar se uma moeda é aceita
    codigo = normalizar_moeda(codigo)
    
    if codigo in moedas: # Vai receber o código e verificar se existe em moedas
        return True
    else:
        return False

def obter_cotacao(codigo):
    codigo = normalizar_moeda(codigo)

    par_moeda = codigo + '-BRL' # Para montar o par que vem na lista da API

    url = f"https://economia.awesomeapi.com.br/json/last/{par_moeda}" # Usamos a varíavel para montar URL e passar qual tipo de moeda queremos
    
    dados = consultar_api(url)

    if dados is None:
        return None

    chave = par_moeda.replace('-','')

    if chave not in dados:
        return None

    dados_moeda = dados[chave]

    if 'bid' not in dados_moeda:
        return None

    if 'create_date' not in dados_moeda:
        return None

    try:
        cotacao = float(dados[chave]['bid'])
    except ValueError:
        return None
    
    data_hora = dados[chave]['create_date']

    return cotacao, data_hora

def processar_conversao(valor_em_reais, moeda_escolhida):

    valor_validado = validar_valor(valor_em_reais)

    if not isinstance(valor_validado, float): # Se caso o valor não esitver como float, ele retorna pra função
        return {
            'sucesso': False,
            'erro': valor_validado
        }

    moeda_normalizada = normalizar_moeda(moeda_escolhida)    

    if not validar_moeda(moeda_normalizada):
        return {
            'sucesso': False,
            'erro': 'Moeda Inválida'
        }

    dados_cotacao = obter_cotacao(moeda_normalizada) # Recebendo os dados da Tupla moeda e data
    
    if dados_cotacao is None:
        return {
            'sucesso': False,
            'erro': 'Cotação Não Encontrada'
        }

    cotacao, data_hora = dados_cotacao

    resultado = converter_moeda(valor_validado, cotacao)

    resultado = round(resultado, 2) # Para salvar somente as 2 casas decimais depois da ,

    return {
        'sucesso': True,
        'moeda': moeda_normalizada,
        'cotacao': cotacao,
        'resultado': resultado
    }

def normalizar_moeda(codigo): # Função para 'normalizar' a moeda e não precisar ficar repetindo o strip e o upper
    codigo = codigo.strip()
    codigo = codigo.upper()
    return codigo

def consultar_api(url):
    try:
        resposta = requests.get(url, timeout=5)
    
        if resposta.status_code == 200:
            try:
                dados = resposta.json()
                return dados
            except ValueError:
                return None

    except requests.exceptions.RequestException: # capturar apenas erros da biblioteca requests
        print("Não foi possível conectar à API")
        return None

