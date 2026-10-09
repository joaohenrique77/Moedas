import customtkinter as ctk
from classes import backend # Importa o seu backend existente

# Configuração do tema visual (Escuro, estilo Google Finance)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# Variável para rastrear qual caixa foi editada por último ("real" ou "estrangeira")
ultima_caixa_editada = "real"
# Criação da janela principal
janela = ctk.CTk()
janela.title("Conversor de Moedas")
janela.geometry("750x450")
janela.resizable(False, False)

def converter_de_real_para_estrangeira(*args):
    global ultima_caixa_editada
    ultima_caixa_editada = "real"

    # Obtém o código da moeda selecionada na guia (USD, EUR, GBP, ARS)
    texto_aba = guia_moedas.get()
    moeda = texto_aba[-4:-1] # Pega exatamente as 3 letras antes do último parêntese (ex: USD)
    
    # --- NOVIDADE AQUI: O dicionário para traduzir o código para o nome bonito ---
    nomes_moedas = {
        'USD': 'Dólar americano',
        'EUR': 'Euro',
        'GBP': 'Libra esterlina',
        'ARS': 'Peso argentino'
    }
    nome_moeda = nomes_moedas.get(moeda, moeda)
    
    # Atualiza o texto da etiqueta na segunda caixa para o nome da moeda selecionada
    label_moeda_destino.configure(text=nome_moeda)
    
    # Pega o valor digitado no campo de Reais
    valor_str = entry_reais.get()
    
    # Se a caixa estiver vazia, não faz a conta, mas atualiza o título na mesma (assumindo '1')
    if not valor_str:
        label_titulo_superior.configure(text=f"1 {nome_moeda} igual a")
        return
        
    # Chama o backend para obter cotação e converter
    resposta = backend.processar_conversao(valor_str, moeda)
    
    if resposta['sucesso']:
        cotacao = resposta['cotacao']
        resultado = resposta['resultado']
        
        # Atualiza a caixa da moeda estrangeira sem acionar loops de eventos
        entry_resultado.delete(0, 'end')
        entry_resultado.insert(0, str(resultado).replace('.', ','))
        
        # --- NOVIDADE AQUI: Atualiza o título superior e o valor principal ---
        # Se eu digitei "1" no Real, ou qualquer outro valor, o título vai mostrar a equivalência correta
        # Nota: O Google Finance mostra sempre "1 Dólar igual a", independente do valor digitado em baixo,
        # mas como a conversão principal aqui é do Real, vamos colocar "1 {Moeda} igual a"
        label_titulo_superior.configure(text=f"1 {nome_moeda} igual a")
        
        # Atualiza o texto da cotação no topo
        texto_cotacao = f"{cotacao:.4f}" if cotacao < 0.1 else f"{cotacao:.2f}"
        label_valor_destaque.configure(text=f"{texto_cotacao} Real brasileiro".replace('.', ','))
        
        label_data_hora.configure(text="Cotação atualizada com sucesso.")


def converter_de_estrangeira_para_real(*args):
    global ultima_caixa_editada
    ultima_caixa_editada = "estrangeira"
    # ... resto do código continua igual
    # Obtém o código da moeda selecionada
    texto_aba = guia_moedas.get()
    moeda = texto_aba[-4:-1] # Pega exatamente as 3 letras antes do último parêntese (ex: USD)
    
    # Pega o valor digitado no campo da moeda estrangeira
    valor_str = entry_resultado.get().replace(',', '.')
    if not valor_str:
        return
        
    # Valida o valor usando a função do backend
    valor_validado = backend.validar_valor(valor_str)
    if not isinstance(valor_validado, float):
        return
        
    # Busca a cotação no backend
    dados_cotacao = backend.obter_cotacao(moeda)
    if dados_cotacao is None:
        return
        
    cotacao, _ = dados_cotacao
    
    # Cálculo inverso: Valor Estrangeiro x Cotação = Valor em Reais
    valor_bruto_reais = valor_validado * cotacao
    
    # Se o valor calculado for muito pequeno (ex: 1 Peso = 0,0053 Reais), mostramos 4 casas decimais
    # Caso contrário, mostramos as normais 2 casas
    if valor_bruto_reais > 0 and valor_bruto_reais < 0.1:
        texto_valor_reais = f"{valor_bruto_reais:.4f}"
    else:
        texto_valor_reais = f"{valor_bruto_reais:.2f}"
    
    # Atualiza a caixa de Reais
    entry_reais.delete(0, 'end')
    entry_reais.insert(0, texto_valor_reais.replace('.', ','))
    
    # Atualiza o texto da cotação no topo
    texto_cotacao = f"{cotacao:.4f}" if cotacao < 0.1 else f"{cotacao:.2f}"
    label_valor_destaque.configure(text=f"{texto_cotacao} Real brasileiro".replace('.', ','))

def atualizar_ao_mudar_aba(*args):
    # Se a última coisa que o usuário fez foi digitar na caixa de moeda estrangeira
    if ultima_caixa_editada == "estrangeira":
        # Então nós recalculamos a partir da caixa estrangeira (ex: 1 Dólar -> Euro -> recálculo)
        converter_de_estrangeira_para_real()
        
        # Como a função acima altera a caixa de reais, precisamos forçar a atualização 
        # visual do título e do nome da moeda no destino, pois ela não faz isso sozinha:
        moeda = guia_moedas.get()
        nomes_moedas = {'USD': 'Dólar americano', 'EUR': 'Euro', 'GBP': 'Libra esterlina', 'ARS': 'Peso argentino'}
        nome_moeda = nomes_moedas.get(moeda, moeda)
        
        label_moeda_destino.configure(text=nome_moeda)
        label_titulo_superior.configure(text=f"1 {nome_moeda} igual a")

    # Se a última coisa que o usuário fez foi digitar em Reais (ou é a primeira vez)
    else:
        # A função de Real -> Estrangeira já faz tudo (calcula e atualiza os textos)
        converter_de_real_para_estrangeira()

# --- AQUI VAMOS ADICIONAR OS COMPONENTES NOS PRÓXIMOS PASSOS ---
# --- Título Superior ---
label_titulo_superior = ctk.CTkLabel(janela, text="Selecione a moeda para iniciar", font=("Arial", 20), text_color="#A0AAB4")
label_titulo_superior.pack(pady=(30, 0), anchor="w", padx=40)

# --- Valor em Destaque (Estilo Google) ---
label_valor_destaque = ctk.CTkLabel(janela, text="0,00 Real brasileiro", font=("Arial", 46, "bold"))
label_valor_destaque.pack(anchor="w", padx=40, pady=(5, 5))

# --- Subtítulo (Data/Hora da cotação) ---
label_data_hora = ctk.CTkLabel(janela, text="Aguardando atualização...", font=("Arial", 12), text_color="#A0AAB4")
label_data_hora.pack(anchor="w", padx=40, pady=(0, 20))

# --- Guias de Moedas (Segmented Button) ---
# Usamos os códigos da API (USD, EUR, GBP, ARS) conforme seu backend
guia_moedas = ctk.CTkSegmentedButton(
    janela,
    values=["Dólar americano (USD)", "Euro (EUR)", "Libra esterlina (GBP)", "Peso argentino (ARS)"],
    font=("Arial", 14),
    width=670,
    height=40,
    selected_color="#4285F4",
    selected_hover_color="#3367D6",
    unselected_color="#202124",
    unselected_hover_color="#3C4043",
    command=atualizar_ao_mudar_aba
)
guia_moedas.pack(pady=20, padx=40)
guia_moedas.set("Dólar americano (USD)") # Define o Dólar como padrão

# --- Container para as Caixas de Valor (Estilo Google Finance) ---
frame_campos = ctk.CTkFrame(janela, fg_color="transparent")
frame_campos.pack(fill="x", padx=40, pady=10)

# --- Caixa 1: Entrada do Valor em Reais (BRL) ---
frame_real = ctk.CTkFrame(frame_campos, fg_color="#202124", corner_radius=8, height=50)
frame_real.pack(fill="x", pady=5)
frame_real.pack_propagate(False)

entry_reais = ctk.CTkEntry(
    frame_real, 
    placeholder_text="0.00", 
    font=("Arial", 18), 
    fg_color="transparent", 
    border_width=0
)
entry_reais.bind("<KeyRelease>", converter_de_real_para_estrangeira)
entry_reais.pack(side="left", padx=15, expand=True, fill="x")

label_moeda_real = ctk.CTkLabel(frame_real, text="Real brasileiro", font=("Arial", 14, "bold"), text_color="#A0AAB4")
label_moeda_real.pack(side="right", padx=15)

# --- Caixa 2: Exibição do Resultado na Moeda Destino ---
frame_destino = ctk.CTkFrame(frame_campos, fg_color="#202124", corner_radius=8, height=50)
frame_destino.pack(fill="x", pady=5)
frame_destino.pack_propagate(False)

entry_resultado = ctk.CTkEntry(
    frame_destino, 
    placeholder_text="0.00", 
    font=("Arial", 18), 
    fg_color="transparent", 
    border_width=0
)
entry_resultado.bind("<KeyRelease>", converter_de_estrangeira_para_real)
entry_resultado.pack(side="left", padx=15, expand=True, fill="x")

label_moeda_destino = ctk.CTkLabel(frame_destino, text="Dólar americano", font=("Arial", 14, "bold"), text_color="#A0AAB4")
label_moeda_destino.pack(side="right", padx=15)

# --- Botão de Atualizar / Converter ---
btn_converter = ctk.CTkButton(
    janela, 
    text="Atualizar Cotação", 
    font=("Arial", 14, "bold"), 
    fg_color="#1A73E8", 
    hover_color="#1557B0", 
    height=40,
    command=atualizar_ao_mudar_aba
)
btn_converter.pack(pady=15, padx=40, fill="x")

# Insere o valor padrão "1" na caixa de Reais ao abrir
entry_reais.insert(0, "1")

# Executa a busca da cotação do Dólar e atualiza a interface imediatamente ao iniciar
atualizar_ao_mudar_aba()












# Executa a janela
if __name__ == "__main__":
    janela.mainloop()