from abc import ABC, abstractmethod
import random
import os
import json
from datetime import datetime

MARCAS_CARRO = [
    "Chevrolet", "Fiat", "Volkswagen", "Ford", "Toyota",
    "Honda", "Hyundai", "Renault", "Jeep", "Nissan",
    "Peugeot", "Citroën", "BMW", "Mercedes-Benz", "Audi"
]

MARCAS_MOTO = [
    "Honda", "Yamaha", "Suzuki", "Kawasaki", "BMW",
    "Triumph", "Ducati", "Harley-Davidson", "Royal Enfield", "Dafra"
]

MARCAS_CAMINHAO = [
    "Mercedes-Benz", "Scania", "Volvo", "DAF", "MAN",
    "Iveco", "Ford", "Volkswagen", "Randon", "Cargo"
]

CORES = [
    "Branca", "Prata", "Preta", "Cinza", "Azul",
    "Vermelha", "Verde", "Bege", "Amarela", "Laranja", "Marrom", "Vinho"
]

ANOS = [str(ano) for ano in range(2025, 1994, -1)]


def digitar_quilometragem():
    while True:
        separador("Quilometragem")
        print("  Digite a quilometragem exata do veículo.")
        print("  (Apenas números, sem pontos ou vírgulas. Ex: 45320)")
        print()
        entrada = input("  Quilometragem (km): ").strip()
        try:
            km = int(entrada)
            if km < 0:
                print("  ⚠  A quilometragem não pode ser negativa.")
            else:
                return f"{km:,.0f} km".replace(",", ".")
        except ValueError:
            print("  ⚠  Digite apenas números inteiros. Ex: 45320")

def digitar_valor():
    while True:
        separador("Valor do Veículo")
        print("  Digite o valor exato de venda.")
        print("  (Use ponto para centavos se necessário. Ex: 45000 ou 45000.50)")
        print()
        entrada = input("  Valor (R$): ").strip()
        entrada = entrada.replace("R$", "").replace(" ", "").replace(",", ".")
        try:
            valor = float(entrada)
            if valor <= 0:
                print("  ⚠  O valor deve ser maior que zero.")
            else:
                valor_fmt = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                return f"R$ {valor_fmt}"
        except ValueError:
            print("  ⚠  Valor inválido. Use apenas números. Ex: 45000 ou 45000.50")

OPCIONAIS_CARRO = [
    "Ar-condicionado",
    "Vidros elétricos",
    "Travas elétricas",
    "Direção hidráulica",
    "Direção elétrica",
    "Multimídia",
    "Câmera de ré",
    "Sensor de estacionamento",
    "Airbag",
    "ABS",
    "Teto solar",
    "Rodas de liga leve",
    "Bancos de couro",
    "Alarme",
    "Chave presencial",
    "Controle de cruzeiro"
]

MOTORES = ["1.0", "1.3", "1.4", "1.6", "1.8", "2.0", "2.5", "3.0", "Elétrico"]

TIPOS_MOTO = ["Naked", "Sport", "Scooter", "Trail", "Custom", "Touring", "Off-road"]

TIPOS_CAMINHAO = ["Leve", "Médio", "Semipesado", "Pesado", "Extrapesado"]

VENDEDORES = ["Carlos Andrade", "Fernanda Lima", "Ricardo Souza", "Patrícia Mendes"]

#CLASSES
class Veiculo(ABC):

    def __init__(self):
        self.codigo      = random.randint(1000, 9999)
        self.modelo      = ""
        self.marca       = ""
        self.ano         = ""
        self.cor         = ""
        self.quilometros = ""
        self.valor       = ""
        self.vendido     = False  # controla se o veículo está disponível

    @abstractmethod
    def tipo(self):
        """Cada subclasse deve retornar seu tipo como string."""
        pass

    @abstractmethod
    def detalhes(self):
        """Cada subclasse retorna uma string com seus detalhes específicos."""
        pass

    def resumo(self):
        """Retorna as informações comuns a todos os veículos."""
        status = "VENDIDO" if self.vendido else "Disponível"
        return (
            f"  Código      : #{self.codigo}\n"
            f"  Tipo        : {self.tipo()}\n"
            f"  Marca       : {self.marca}\n"
            f"  Modelo      : {self.modelo}\n"
            f"  Ano         : {self.ano}\n"
            f"  Cor         : {self.cor}\n"
            f"  Quilometros : {self.quilometros}\n"
            f"  Valor       : {self.valor}\n"
            f"  Status      : {status}"
        )

    def to_dict(self):
        """Converte o veículo para dicionário (para salvar em arquivo)."""
        return {
            "codigo":      self.codigo,
            "tipo_classe": self.tipo(),
            "modelo":      self.modelo,
            "marca":       self.marca,
            "ano":         self.ano,
            "cor":         self.cor,
            "quilometros": self.quilometros,
            "valor":       self.valor,
            "vendido":     self.vendido,
        }

    def iniciar(self, atrs):
        """Recebe os valores em um dict para iniciar os seus atributos"""
        self.codigo = atrs["codigo"]
        self.modelo = atrs["modelo"]
        self.marca = atrs["marca"]
        self.ano = atrs["ano"]
        self.cor = atrs["cor"]
        self.quilometros = atrs["quilometros"]
        self.valor = atrs["valor"]
        self.vendido = atrs["vendido"]

class Carro(Veiculo):
    """Herda de Veiculo e adiciona atributos exclusivos de carros."""

    def __init__(self):
        super().__init__()
        self.portas    = ""
        self.motor     = ""
        self.opcionais = []

    def tipo(self):
        return "Carro"

    def detalhes(self):
        op = ", ".join(self.opcionais) if self.opcionais else "Nenhum"
        return (
            f"  Portas      : {self.portas}\n"
            f"  Motor       : {self.motor}\n"
            f"  Opcionais   : {op}"
        )

    def to_dict(self):
        d = super().to_dict()
        d.update({"portas": self.portas, "motor": self.motor, "opcionais": self.opcionais})
        return d

    def iniciar(self, atrs):
        super().iniciar(atrs)
        self.portas = atrs["portas"]
        self.motor = atrs["motor"]
        self.opcionais = atrs["opcionais"]

class Moto(Veiculo):
    """Herda de Veiculo e adiciona atributos exclusivos de motos."""

    def __init__(self):
        super().__init__()
        self.cilindrada   = ""
        self.tipo_moto    = ""

    def tipo(self):
        return "Moto"

    def detalhes(self):
        return (
            f"  Cilindrada  : {self.cilindrada}\n"
            f"  Tipo        : {self.tipo_moto}"
        )

    def to_dict(self):
        d = super().to_dict()
        d.update({"cilindrada": self.cilindrada, "tipo_moto": self.tipo_moto})
        return d

    def iniciar(self, atrs):
        super().iniciar(atrs)
        self.cilindrada = atrs["cilindrada"]
        self.tipo_moto = atrs["tipo_moto"]

class Caminhao(Veiculo):
    """Herda de Veiculo e adiciona atributos exclusivos de caminhões."""

    def __init__(self):
        super().__init__()
        self.eixos        = ""
        self.tipo_caminhao = ""

    def tipo(self):
        return "Caminhão"

    def detalhes(self):
        return (
            f"  Eixos       : {self.eixos}\n"
            f"  Tipo        : {self.tipo_caminhao}"
        )

    def to_dict(self):
        d = super().to_dict()
        d.update({"eixos": self.eixos, "tipo_caminhao": self.tipo_caminhao})
        return d

    def iniciar(self, atrs):
        super().iniciar(atrs)
        self.eixos = atrs["eixos"]
        self.tipo_caminhao = atrs["tipo_caminhao"]

class Vendedor:
    def __init__(self, nome):
        self.nome = nome

class Cliente:
    def __init__(self, nome, doc):
        self.nome = nome
        self.doc  = doc

class Venda:
    def __init__(self, veiculo=None, cliente=None, vendedor=None):
        self.veiculo  = veiculo
        self.cliente  = cliente
        self.vendedor = vendedor
        self.data     = datetime.now().strftime("%d/%m/%Y %H:%M")

    def resumo(self):
        return (
            f"  Data        : {self.data}\n"
            f"  Veículo     : {self.veiculo.marca} {self.veiculo.modelo} "
            f"(#{self.veiculo.codigo})\n"
            f"  Valor       : {self.veiculo.valor}\n"
            f"  Cliente     : {self.cliente.nome} — Doc: {self.cliente.doc}\n"
            f"  Vendedor    : {self.vendedor.nome}"
        )

    def to_dict(self):
        return {
            "veiculo":  self.veiculo.codigo,
            "cliente_nome":  self.cliente.nome,
            "cliente_doc": self.cliente.doc,
            "vendedor": self.vendedor.nome,
            "data":     self.data
        }

    def iniciar(self, atrs):
        for v in estoque:
            if v.codigo == atrs["veiculo"]:
                self.veiculo = v
                break
        
        self.cliente = Cliente(atrs["cliente_nome"], atrs["cliente_doc"])
        self.vendedor = Vendedor(atrs["vendedor"])
        self.data = atrs["data"]

#Variáveis de banco
estoque = []
with open("estoque.txt") as est:
    for linha in est:
        if linha == "": continue
        
        linha = json.loads(linha)
        veic = None

        if linha["tipo_classe"] == "Carro": veic = Carro()
        elif linha["tipo_classe"] == "Moto": veic = Moto()
        else: veic = Caminhao()
        veic.iniciar(linha)

        estoque.append(veic)

vendas  = []
with open("vendas.txt") as hist:
    for linha in hist:
        if linha == "": continue

        linha = json.loads(linha)
        venda = Venda()
        venda.iniciar(linha)
        vendas.append(venda)


def atualiza_banco(est=True):
    if est:
        novEst = ""
        for veic in estoque:
            novEst += (json.dumps(veic.to_dict()) + "\n")
        
        with open("estoque.txt", "w") as esto:
            esto.write(novEst)
    else:
        novVen = ""
        for ven in vendas:
            novVen += (json.dumps(ven.to_dict()) + "\n")
        
        with open("vendas.txt", "w") as v:
            v.write(novVen)

def limpar_tela():
    """Limpa o terminal para deixar a interface mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def separador(titulo=""):
    """Imprime uma linha separadora com título opcional."""
    print()
    if titulo:
        print(f"{'─' * 10} {titulo.upper()} {'─' * 10}")
    else:
        print("─" * 40)

def pausar():
    """Pausa a execução até o usuário pressionar Enter."""
    print()
    input("  Pressione Enter para continuar...")

def selecionar(titulo, opcoes, permite_multiplo=False):

    while True:
        separador(titulo)
        for i, opcao in enumerate(opcoes, start=1):
            print(f"  {i:2}. {opcao}")
        print()

        if permite_multiplo:
            entrada = input("  Digite os números separados por vírgula (ex: 1,3,5): ").strip()
            if not entrada:
                return []  # nenhum opcional selecionado é válido
            try:
                indices = [int(x.strip()) for x in entrada.split(",")]
                # Verifica se todos os índices são válidos
                if all(1 <= idx <= len(opcoes) for idx in indices):
                    return [opcoes[idx - 1] for idx in indices]
                else:
                    print("  ⚠  Número inválido. Tente novamente.")
            except ValueError:
                print("  ⚠  Digite apenas números separados por vírgula.")
        else:
            entrada = input("  Escolha uma opção: ").strip()
            try:
                idx = int(entrada)
                if 1 <= idx <= len(opcoes):
                    return opcoes[idx - 1]
                else:
                    print(f"  ⚠  Digite um número entre 1 e {len(opcoes)}.")
            except ValueError:
                print("  ⚠  Digite apenas o número da opção.")

def gerar_codigo():
    """Gera um código numérico aleatório de 4 dígitos para o veículo."""
    return random.randint(1000, 9999)

#Funções do menu:
def alterar_deletar_veiculo():

    limpar_tela()
    separador("Alterar / Deletar Veículo")

    disponiveis = [v for v in estoque if not v.vendido]

    if not disponiveis:
        print("  Nenhum veículo disponível no estoque.")
        pausar()
        return

    opcoes = [
        f"#{v.codigo} — {v.marca} {v.modelo} ({v.ano}) — {v.valor}"
        for v in disponiveis
    ]

    escolha_str = selecionar("Selecione o veículo", opcoes)
    idx = opcoes.index(escolha_str)
    veic = disponiveis[idx]

    limpar_tela()
    separador(f"Veículo #{veic.codigo}")
    print(veic.resumo())
    print()
    print(veic.detalhes())

    acao = selecionar("O que deseja fazer?", ["Alterar dados", "Deletar veículo"])

    # DELETAR
    if acao == "Deletar veículo":
        separador("Confirmar exclusão")
        print("  Tem certeza que deseja deletar o veículo abaixo?")
        print(f"  {veic.marca} {veic.modelo} (#{veic.codigo})")
        print()
        confirmacao = input("  Digite SIM para confirmar: ").strip().upper()
        if confirmacao == "SIM":
            estoque.remove(veic)
            print()
            print("  ✅  Veículo removido do estoque com sucesso!")
        else:
            print()
            print("  ❌  Operação cancelada.")
        pausar()
        return

    # ALTERAR
    separador("O que deseja alterar?")
    campos = ["Modelo", "Cor", "Quilometragem", "Valor", "Cancelar"]
    campo = selecionar("Campo para alterar", campos)

    if campo == "Cancelar":
        return

    if campo == "Modelo":
        print()
        novo = input("  Novo modelo: ").strip()
        if novo:
            veic.modelo = novo

    elif campo == "Cor":
        veic.cor = selecionar("Nova cor", CORES)

    elif campo == "Quilometragem":
        veic.quilometros = digitar_quilometragem()

    elif campo == "Valor":
        veic.valor = digitar_valor()

    print()
    print("  ✅  Dado alterado com sucesso!")
    separador(f"Veículo #{veic.codigo} atualizado")
    print(veic.resumo())
    pausar()
    atualiza_banco()

def cadastrar_veiculo():
    
    limpar_tela()
    separador("Cadastro de Veículo")

    # 1. Escolher o tipo de veículo
    tipo_escolhido = selecionar("Tipo de veículo", ["Carro", "Moto", "Caminhão"])

    # 2. Criar o objeto correto dependendo do tipo escolhido
    if tipo_escolhido == "Carro":
        veic = Carro()
        marcas = MARCAS_CARRO
    elif tipo_escolhido == "Moto":
        veic = Moto()
        marcas = MARCAS_MOTO
    else:
        veic = Caminhao()
        marcas = MARCAS_CAMINHAO
    # 3. Preencher os atributos comuns (todos os veículos têm esses)
    veic.marca       = selecionar("Marca", marcas)
    veic.modelo      = input("\n  Modelo (ex: Onix, CG 160): ").strip()
    veic.ano         = selecionar("Ano", ANOS)
    veic.cor         = selecionar("Cor", CORES)
    veic.quilometros = digitar_quilometragem()
    veic.valor       = digitar_valor()

    if isinstance(veic, Carro):
        veic.portas    = selecionar("Número de portas", ["2 portas", "4 portas"])
        veic.motor     = selecionar("Motor", MOTORES)
        print("\n  Selecione os OPCIONAIS disponíveis no veículo.")
        print("  (Digite os números separados por vírgula, ou Enter para nenhum)")
        veic.opcionais = selecionar("Opcionais", OPCIONAIS_CARRO, permite_multiplo=True)

    elif isinstance(veic, Moto):
        veic.cilindrada = selecionar("Cilindrada", [
            "50cc", "125cc", "150cc", "160cc", "200cc",
            "250cc", "300cc", "400cc", "600cc", "1000cc ou mais"
        ])
        veic.tipo_moto = selecionar("Tipo de moto", TIPOS_MOTO)

    elif isinstance(veic, Caminhao):
        veic.eixos = selecionar("Número de eixos", [
            "2 eixos", "3 eixos", "4 eixos", "5 eixos", "6 eixos"
        ])
        veic.tipo_caminhao = selecionar("Tipo de caminhão", TIPOS_CAMINHAO)

    estoque.append(veic)

    limpar_tela()
    separador("Veículo Cadastrado com Sucesso!")
    print(veic.resumo())
    separador()
    print(veic.detalhes())
    separador()
    print(f"  ✅  Código gerado: #{veic.codigo}")
    print(json.dumps(veic.to_dict()))
    pausar()

def consultar_estoque():
    
    limpar_tela()
    separador("Estoque de Veículos")

    disponiveis = [v for v in estoque if not v.vendido]
    vendidos    = [v for v in estoque if v.vendido]

    if not estoque:
        print("  Nenhum veículo cadastrado no sistema.")
        pausar()
        return

    print(f"  Total cadastrado : {len(estoque)} veículo(s)")
    print(f"  Disponíveis      : {len(disponiveis)}")
    print(f"  Vendidos         : {len(vendidos)}")

    for v in estoque:
        separador(f"#{v.codigo} — {v.marca} {v.modelo}")
        print(v.resumo())
        print()
        print(v.detalhes())

    pausar()

def registrar_venda():
    
    limpar_tela()
    separador("Registrar Venda")

    disponiveis = [v for v in estoque if not v.vendido]

    if not disponiveis:
        print("  Nenhum veículo disponível para venda no momento.")
        pausar()
        return

    opcoes_veiculos = [
        f"{v.marca} {v.modelo} ({v.ano}) — {v.valor} — #{v.codigo}"
        for v in disponiveis
    ]

    escolha_str = selecionar("Veículos disponíveis", opcoes_veiculos)

    idx = opcoes_veiculos.index(escolha_str)
    veic_escolhido = disponiveis[idx]

    separador("Dados do Cliente")
    nome_cliente = input("  Nome do cliente : ").strip()
    doc_cliente  = input("  Documento (CPF) : ").strip()

    nome_vendedor = selecionar("Vendedor responsável", VENDEDORES)

    cliente  = Cliente(nome_cliente, doc_cliente)
    vendedor = Vendedor(nome_vendedor)
    venda    = Venda(veic_escolhido, cliente, vendedor)

    veic_escolhido.vendido = True  # marca como vendido no estoque
    vendas.append(venda)
    print(json.dumps(venda.to_dict()))

    limpar_tela()
    separador("Venda Registrada com Sucesso!")
    print(venda.resumo())
    pausar()

def consultar_vendas():
    """Exibe o histórico de todas as vendas realizadas."""
    limpar_tela()
    separador("Histórico de Vendas")

    if not vendas:
        print("  Nenhuma venda registrada ainda.")
        pausar()
        return

    print(f"  Total de vendas: {len(vendas)}")
    for i, v in enumerate(vendas, start=1):
        separador(f"Venda #{i}")
        print(v.resumo())

    pausar()

def main():
    
    while True:
        limpar_tela()
        separador("Sistema de Revenda de Veículos")

        disponiveis = len([v for v in estoque if not v.vendido])
        print(f"  Estoque disponível : {disponiveis} veículo(s)")
        print(f"  Vendas realizadas  : {len(vendas)}")
        separador()

        print("  1. Cadastrar veículo")
        print("  2. Consultar estoque")
        print("  3. Registrar venda")
        print("  4. Histórico de vendas")
        print("  5. Alterar / Deletar veículo")
        print("  0. Sair")
        separador()

        opcao = input("  Escolha uma opção: ").strip()

        match opcao:
            case "1":
                cadastrar_veiculo()
            case "2":
                consultar_estoque()
            case "3":
                registrar_venda()
            case "4":
                consultar_vendas()
            case "5":
                alterar_deletar_veiculo()
            case "0":
                limpar_tela()
                print("  Até logo!")
                break
            case _:
                print("  ⚠  Opção inválida. Tente novamente.")
                pausar()

if __name__ == "__main__":
    main()
