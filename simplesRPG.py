import random
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def recuperaçãoHPMonstro(monstroHP):
    if probabilidade() > 0.9:
        curaMonstro = random.randint(15, 25)
        monstroHP += curaMonstro
        monstroHP = min(monstroHP, 100)  # Evita que o monstro ultrapasse 100 de HP
        print(f"O monstro se curou e recuperou {curaMonstro} de HP!")
    return monstroHP

def probabilidade():
    return random.random()

def ataqueEspecial(mp, hp, monstroHp):
    bolaDeFogo = random.randint(35, 50)
    cura = 100 - hp  # Corrigido para calcular cura corretamente
    print("[1] Bola de Fogo")
    print("[2] Cura")
    escolha = int(input("Digite sua habilidade: "))

    if escolha == 1 and mp >= 50:
        print(f"Você atacou uma bola de fogo e deu {bolaDeFogo} de dano")
        monstroHp -= bolaDeFogo
        mp -= 50
        hp, dano = receberDano(hp)
        print(f"O monstro atacou e você tomou {dano} de dano. HP atual: {hp}", flush=True)
        return monstroHp, mp, hp  # Corrigido retorno
    elif escolha == 1 and mp < 50:
        print("Mana insuficiente para lançar Bola de Fogo!")  # Mensagem corrigida
    elif escolha == 2 and mp >= 100:  # Corrigido para >= 100
        hp += cura
        mp -= 100
        print("Recuperou toda sua vida!")
    else:
        print("Mana insuficiente")
    return monstroHp, mp, hp  # Corrigido retorno

def ataquePadrao():
    return random.randint(15, 30)

def checarFimDeJogo(hp):
    if hp <= 0:
        print("Você morreu.")
        return True
    return False

def receberDano(hp):
    ataque = ataquePadrao()
    hp -= ataque
    return hp, ataque

def main():
    hp = 100
    mp = 100
    monstroHP = 100

    while True:
        limpar_tela()
        chance = probabilidade()
        print(f"Seu HP: {hp} | HP do Monstro: {monstroHP}", flush=True)
        print("-=" * 20)
        print("Você vai: ")
        print("[1] Atacar ")
        print("[2] Defender ")
        print("[3] Fugir")
        print("[4] Ataque Especial")
        print("-=" * 20)

        try:
            escolha = int(input("Digite sua escolha: "))
        except ValueError:
            print("Entrada inválida. Digite um número entre 1 e 4.")  # Ajustado número
            continue

        if escolha == 1 and chance > 0.3:
            ataque = ataquePadrao()
            print(f"Você atacou e causou {ataque} de dano.", flush=True)
            monstroHP -= ataque
            if monstroHP <= 0:  # Monstro derrotado antes da cura
                print("O monstro foi derrotado com sucesso!")
                break
            monstroHP = recuperaçãoHPMonstro(monstroHP)
            if probabilidade() > 0.7:
                print("Você esquivou do ataque do monstro!", flush=True)
            else:
                hp, dano = receberDano(hp)
                print(f"O monstro atacou e você tomou {dano} de dano. HP atual: {max(hp, 0)}", flush=True)
                if checarFimDeJogo(hp):
                    break
        elif escolha == 1 and chance <= 0.3:
            print("Você errou o ataque!", flush=True)
            hp, dano = receberDano(hp)
            print(f"Você tomou {dano} de dano. HP atual: {hp}", flush=True)
            if checarFimDeJogo(hp):
                break
        elif escolha == 2 and chance > 0.7:
            print("Você conseguiu se defender com sucesso!", flush=True)
        elif escolha == 2 and chance <= 0.7:
            hp, dano = receberDano(hp)
            print(f"Você falhou na defesa e tomou {dano} de dano. HP atual: {max(hp, 0)}", flush=True)
            monstroHP = recuperaçãoHPMonstro(monstroHP)
            if checarFimDeJogo(hp):
                break
        elif escolha == 3 and chance <= 0.8:
            hp, dano = receberDano(hp)
            print(f"Você falhou em fugir e tomou {dano} de dano. HP atual: {max(hp, 0)}", flush=True)
            monstroHP = recuperaçãoHPMonstro(monstroHP)
            if checarFimDeJogo(hp):
                break
        elif escolha == 3 and chance > 0.8:
            print("Você fugiu com sucesso!", flush=True)
            break
        elif escolha == 4:
            monstroHP, mp, hp = ataqueEspecial(mp, hp, monstroHP)
            if checarFimDeJogo(hp):
                break

        else:
            print("Escolha inválida. Tente novamente.", flush=True)

        if mp < 100:
            mp += 10
        hp = min(hp, 100)  # Evita ultrapassar o máximo
        mp = min(mp, 100)  # Evita ultrapassar o máximo

        input("\nPressione Enter para continuar...")


main()
