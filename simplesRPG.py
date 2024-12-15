import random
import os

nome_item_aleatorios = ["Resto de corpos", "Olhos de carmesim", "Lixo", "Cauda de centauro"]

# Função para limpar a tela, dependendo do sistema operacional
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
def item_sem_efeito():
    return lambda alvo: print(Color.WARNING + "Este item não tem nenhum efeito especial." + Color.END)
class Color:
    HEADER = '\033[95m'       # Magenta
    OKBLUE = '\033[94m'       # Blue
    OKGREEN = '\033[92m'      # Green
    WARNING = '\033[93m'      # Yellow
    FAIL = '\033[91m'         # Red
    END = '\033[0m'    

def usar_item(jogador):
    if jogador.inventario:
        jogador.mostrar_inventario()
        print("Digite 99 para sair.")
        try:
            item_escolhido = int(input(Color.OKBLUE + "Escolha um item para usar: " + Color.END)) - 1
            if 0 <= item_escolhido < len(jogador.inventario):
                item = jogador.inventario[item_escolhido]
                if item.nome in nome_item_aleatorios:
                    if item.quantidade > 0:
                        print(Color.FAIL + "Não teve nenhum efeito!" + Color.END)
                        item.quantidade -= 1
                        if item.quantidade == 0:
                            jogador.inventario.pop(item_escolhido)
                    else:
                        print("Você não tem mais esse item")
                elif item.tipo == "arma":
                    jogador.equipar(item)
                    print("Arma equipada!")
                    jogador.inventario.pop(item_escolhido)
                    input()
                else:
                    item.usar(jogador)
                    if item.quantidade == 0:
                        jogador.inventario.pop(item_escolhido)
            elif item_escolhido == 98:  # 99 - 1
                print("Saindo...")   
            else:
                print(Color.FAIL + "Item inválido." + Color.END)
        except ValueError:
            print(Color.FAIL + "Entrada inválida. Tente novamente!" + Color.END)
    else:
        print(Color.FAIL + "Você não tem itens no inventário." + Color.END)
    input("\nPressione Enter para voltar ao menu...")

# Função para criar monstros aleatórios com nome, HP e MP
def criar_monstro():
    nomes_monstros = ["Goblin", "Ogro", "Chefão", "Lobo Selvagem", "Dragão Bebê", "Gnomo", "Dragão de komodo"]
    nome = random.choice(nomes_monstros)
    hp = random.randint(80, 200)
    mp = 0
    return Monstro(nome, hp, mp)
def item_aleatorio():
    nome = random.choice(nome_item_aleatorios)
    efeito = item_sem_efeito()
    quantidade = random.randint(1,6)
    return Item(nome, efeito, quantidade)
# Classe para representar itens
class Item:
    def __init__(self, nome, efeito, quantidade, tipo=None):
        self.nome = nome  # Nome do item
        self.efeito = efeito  # Função que define o efeito do item
        self.quantidade = quantidade  # Quantidade disponível do item
        self.tipo = tipo

    def usar(self, alvo):
        if self.quantidade > 0:
            self.efeito(alvo)  # Aplica o efeito ao alvo (geralmente o jogador)
            self.quantidade -= 1
            print(Color.OKGREEN + f"Você usou {self.nome}!" + Color.END)
        else:
            print(Color.FAIL + f"Você não tem mais {self.nome}." + Color.END)

# Classe base para personagens
class Personagem:
    def __init__(self, nome, hp, mp):
        self.nome = nome
        self.hp = hp
        self.mp = mp
        self.hp_max = hp
        self.mp_max = mp
        self.atq = 20
        self.nivel = 1
        self.exp = 0
        self.exp_proximo_nivel = 100

    def ganhar_exp(self, exp_ganha):
        print(Color.OKGREEN + f"Você ganhou {exp_ganha} de experiência!" + Color.END)
        self.exp += exp_ganha
        while self.exp >= self.exp_proximo_nivel:
            self.subir_de_nivel()

    def subir_de_nivel(self):
        self.exp -= self.exp_proximo_nivel
        self.nivel += 1
        self.exp_proximo_nivel = int(self.exp_proximo_nivel * 1.5)  # Aumenta a dificuldade para subir de nível
        aumento_hp = random.randint(10, 20)
        aumento_mp = random.randint(5, 10)
        self.hp_max += aumento_hp
        self.mp_max += aumento_mp
        self.hp = self.hp_max
        self.mp = self.mp_max
        self.atq += random.randint(10,15)
        print(Color.OKGREEN + f"Parabéns! Você subiu para o nível {self.nivel}!" + Color.END)
        print(f"Seu HP máximo aumentou para {self.hp_max}.")
        print(f"Seu MP máximo aumentou para {self.mp_max}.")
        
    # Métodos para gerenciar dano, cura e mana
    def receber_dano(self, dano):
        self.hp -= dano
        self.hp = max(self.hp, 0)

    def recuperar_hp(self, cura):
        self.hp += cura
        self.hp = min(self.hp, self.hp_max)

    def recuperar_mp(self, quantidade):
        self.mp += quantidade
        self.mp = min(self.mp, self.mp_max)

    def esta_vivo(self):
        return self.hp > 0

    # Representação do personagem em texto
    def __str__(self):
        return (f"{self.nome}: Nível {self.nivel}\n"
                f"HP = {self.hp}/{self.hp_max}, MP = {self.mp}/{self.mp_max}\n"
                f"Experiência = {self.exp}/{self.exp_proximo_nivel}")


# Classe para o jogador, herda de Personagem
class Jogador(Personagem):
    def __init__(self, nome, hp, mp):
        super().__init__(nome, hp, mp)
        self.ouro = 0
        self.inventario = []  # Inventário do jogador para armazenar itens
        self.arma = None

    # Adiciona um item ao inventário
    def adicionar_item(self, item):
        self.inventario.append(item)
    def equipar(self, item):
        self.arma = item
        self.atq += 15
    def desequipar(self):
        self.arma = None


    # Mostra o inventário com a quantidade de cada item
    def mostrar_inventario(self):
        print(Color.OKBLUE + "Seu inventário:" + Color.END)
        for i, item in enumerate(self.inventario, 1):
            print(f"[{i}] {item.nome} (Quantidade: {item.quantidade})")
    def equipar_item(self, item):
        if item in self.inventario:
            self.inventario.remove(item)
            self.equipado = item
            print(f"{self.nome} equipou {item}.")
        else:
            print(f"{item} não está no inventário!")

    # Métodos para ataque e cura
    def ataque_padrao(self):
        return random.randint(20,50) + self.atq

    def ataque_especial(self, inimigo):
        if self.mp >= 50:
            dano = random.randint(35, 50)
            self.mp -= 50
            inimigo.receber_dano(dano)
            print(Color.OKBLUE + f"Você usou Bola de Fogo e causou {dano} de dano!" + Color.END)
        else:
            print(Color.FAIL + "Mana insuficiente para usar Bola de Fogo!" + Color.END)

    def curar(self):
        if self.mp >= 80:
            cura = self.hp_max - self.hp
            self.recuperar_hp(cura)
            self.mp -= 100
        else:   
            print(Color.FAIL + "Mana insuficiente para curar!" + Color.END)

# Classe para monstros, herda de Personagem
class Monstro(Personagem):
    def __init__(self, nome, hp, mp):
        super().__init__(nome, hp, mp)

    def ataque(self):
        return random.randint(20,40)

    def recuperar_vida(self):
        if random.random() > 0.9:
            cura = random.randint(15, 25)
            self.recuperar_hp(cura)
            print(Color.OKGREEN + f"O monstro se curou e recuperou {cura} de HP!" + Color.END)
# Função para gerenciar a batalha

def batalha(jogador, monstro):
    while jogador.esta_vivo() and monstro.esta_vivo():
        fugir = False
        limpar_tela()
        print(jogador)
        print(monstro)
        print("-=" * 20)
        print("Você vai: ")
        print("[1] Atacar ")
        print("[2] Defender ")
        print("[3] Fugir")
        print("[4] Ataque Especial")
        print("[5] Usar Item")  # Nova opção para usar itens
        print("-=" * 20)

        try:
            escolha = int(input(Color.OKBLUE + "Digite sua escolha: " + Color.END))
        except ValueError:
            print(Color.FAIL + "Entrada inválida. Tente novamente!" + Color.END)
            continue

        if escolha == 1:
            dano = jogador.ataque_padrao()
            monstro.receber_dano(dano)
            print(Color.OKGREEN + f"Você atacou e causou {dano} de dano!" + Color.END)
        elif escolha == 2:
            if random.random() > 0.7:
                print("Você conseguiu se defender com sucesso!")
                continue
            else:
                print(Color.WARNING + "Você defendeu o próximo ataque do monstro!" + Color.END)
        elif escolha == 3:
            if random.random() > 0.8:
                fugir = True
                print(Color.WARNING + "Fugindo da batalha..." + Color.END)
                break
            else:
                dano = monstro.ataque()
                jogador.receber_dano(dano)
                print(Color.FAIL + f"Você falhou em fugir e tomou {dano} de dano!" + Color.END)
        elif escolha == 4:
            jogador.ataque_especial(monstro)
        elif escolha == 5:
            usar_item(jogador)
        else:
            print("Escolha inválida!")

        if monstro.esta_vivo():
            monstro.recuperar_vida()
            dano = monstro.ataque()
            jogador.receber_dano(dano)
            print(Color.FAIL + f"O monstro atacou e causou {dano} de dano!" + Color.END)

        # Corrigir a recuperação de MP para ser proporcional aos pontos máximos de MP do jogador
        jogador.recuperar_mp(jogador.mp_max // 10)  # Recupera 10% dos MP máximos

        input("\nPressione Enter para continuar...")

    if jogador.esta_vivo() and fugir == False:
        print(Color.OKGREEN + "Você venceu a batalha!" + Color.END)
        aumento_hp = random.randint(5, 10)
        aumento_mp = random.randint(5, 10)
        ouro_ganhado = random.randint(10,30)
        jogador.ouro += ouro_ganhado
        print(f"Você ganhou {ouro_ganhado} de ouro!")

        exp_ganha = random.randint(20, 50)  # Experiência ganha ao derrotar o monstro
        jogador.ganhar_exp(exp_ganha)
        if random.random() > 0.7:  # 30% de chance de encontrar um item
            item = item_aleatorio()
            encontrado = False
            for itens in jogador.inventario:
                if itens.nome == item.nome:
                    itens.quantidade +=1
                    encontrado = True
                    break
            if not encontrado:
                jogador.adicionar_item(item)

        input("Aperte para continuar")
    elif jogador.esta_vivo() and fugir:
        print("Você Escapou com sucesso")
        input("Aperte enter para continuar")
    else:
        print(Color.FAIL + "Você foi derrotado na batalha!" + Color.END)


# Menu principal do jogo
def menu_principal(jogador):
    while True:
        limpar_tela()
        print(Color.HEADER + "Bem-vindo ao RPG de Texto!" + Color.END)
        print("-=" * 20)
        print("[1] Ver Status")
        print("[2] Procurar Monstros")
        print("[3] Se curar")
        print("[4] Usar Item")  # Nova opção para usar itens fora da batalha
        print("[5] Loja")
        print("[0] Sair do Jogo")
        print("-=" * 20)

        try:
            escolha = int(input("Digite sua escolha: "))
        except ValueError:
            print("Escolha inválida. Tente novamente!")
            input("Pressione Enter para continuar...")
            continue

        if escolha == 1:
            limpar_tela()
            print(jogador)
            input("\nPressione Enter para voltar ao menu...")
        elif escolha == 2:
            monstro = criar_monstro()
            batalha(jogador, monstro)
            if not jogador.esta_vivo():
                print("Você morreu! Fim de jogo.")
                break
        elif escolha == 3:
            jogador.curar()
            print(f"Você curou-se. Agora seu HP é {jogador.hp}/{jogador.hp_max}.")
            input("\nPressione Enter para voltar ao menu...")
        elif escolha == 4:
            usar_item(jogador)
        elif escolha == 5:
            loja(jogador)
        elif escolha == 0:
            print("Até logo, aventureiro!")
            break
        else:
            print("Escolha inválida.")
            input("\nPressione Enter para continuar...")
def loja(jogador):
    itens_loja = [
        Item("Poção de Vida", lambda alvo: alvo.recuperar_hp(50), 1),
        Item("Poção de Mana", lambda alvo: alvo.recuperar_mp(50), 1),
        Item("Espada de Madeira", lambda alvo: print(Color.OKGREEN + "Você agora tem uma arma melhor!" + Color.END), 1, tipo="arma"),
    ]
    precos = [50, 50, 20]  # Preços correspondentes aos itens

    while True:
        limpar_tela()
        print(Color.HEADER + "Bem-vindo à Loja!" + Color.END)
        print(f"Ouro disponível: {jogador.ouro}")
        print("-=" * 20)

        for i, item in enumerate(itens_loja, 1):
            print(f"[{i}] {item.nome} - {precos[i-1]} ouro")
        print("[0] Sair da Loja")
        print("-=" * 20)

        try:
            escolha = int(input(Color.OKBLUE + "Digite o número do item que deseja comprar: " + Color.END))
            if escolha == 0:
                print("Saindo da loja...")
                break
            elif 1 <= escolha <= len(itens_loja):
                preco = precos[escolha - 1]
                if jogador.ouro >= preco:
                    jogador.ouro -= preco
                    item_comprado = itens_loja[escolha - 1]
                    encontrado = False
                    for item in jogador.inventario:
                        if item.nome == item_comprado.nome:
                            item.quantidade += item_comprado.quantidade
                            encontrado = True
                            break
                    if not encontrado:
                        jogador.adicionar_item(item_comprado)
                    print(Color.OKGREEN + f"Você comprou {item_comprado.nome}!" + Color.END)
                else:
                    print(Color.FAIL + "Ouro insuficiente!" + Color.END)
            else:
                print(Color.FAIL + "Opção inválida!" + Color.END)
        except ValueError:
            print(Color.FAIL + "Entrada inválida. Tente novamente!" + Color.END)

        input("\nPressione Enter para continuar...")



# Função principal para iniciar o jogo
def main():
    limpar_tela()
    print("Bem-vindo ao RPG!")
    nome = input("Digite o nome do seu personagem: ")
    jogador = Jogador(nome, 200, 100)

    # Criando itens iniciais
    pocao_hp = Item("Poção de Vida", lambda alvo: alvo.recuperar_hp(50), 3)
    pocao_mp = Item("Poção de Mana", lambda alvo: alvo.recuperar_mp(50), 2)
    jogador.adicionar_item(pocao_hp)
    jogador.adicionar_item(pocao_mp)

    menu_principal(jogador)

if __name__ == "__main__":
    main()  
