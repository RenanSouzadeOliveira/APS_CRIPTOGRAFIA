from Crypto.PublicKey import RSA #IMPORTANDO DA BIBLIOTECA O ALGORITMO RSA
from Crypto.Cipher import PKCS1_OAEP #O PKCS1_OAEP permite criar um 'recipiente' para as chaves
import pygame #importando o pygame
from pygame import mixer
import time
def Chaves():
    #essa função gera as chaves e a coloca no seu 'recipiente'
    chave_gerada = RSA.generate(2048) #isso gera a chave e faz com que os números usados sejam de 2048 bits
    key = PKCS1_OAEP.new(chave_gerada) # cria um recipiente para as chaves geradas
    return key #retorna o recipiente das chaves


def Criptografar(senha):
    s_codificada = senha.encode('utf-8') #Essa linha codifica o texto para ele poder ser criptografado
    key = Chaves() #chama a função Chaves() para gerar as chaves
    s_criptografada = key.encrypt(s_codificada) #criptografando a mensagem
    return s_criptografada, key #retorna a mensagem criptogradafa, e a chave


def Decodificar(senha_criptograda, key):
    s_descriptografada = key.decrypt(senha_criptograda)
    s_decodificada = s_descriptografada.decode('utf-8')
    return s_decodificada # retornado a mensagem descriptografada e decodificada

def main():
    dec = "-" * 80
    # Desenhando o menu
    print(dec)
    print("MARINHA DO BRASIL".center(80))
    print("Marinha do Brasil, protegendo nossas riquezas, cuidando da nossa gente.".center(80))
    print(dec)
    print("CONTROLE DE ACESSO.".center(80))
    print(dec)
    escolha = 0
    cont = 0
    while escolha != 4: #enquanto a escolha do usuario for diferente de 4(que é a opçao para sair) o algoritmo irá rodar
        print("Escolha o número correspondente ao que você quer realizar no sistema:".center(80))
        print("1 - Entrar no navio;".center(80))
        print("2 - Cadastrar;".center(74))
        print("3 - Sair.".center(70))
        print(dec)
        escolha = int(input("Opção:"))

        patentes_validas = ["capitãodecorveta", "capitãodefragata", "capitãodemareguerra", "contra-almirante", "vice-almirante", "almirantedeesquadra", "almirante"]

        if (escolha == 1):
            patente = input("Digite sua patente:")
            senha = input("Digite sua senha:")

        elif (escolha == 2):
            cad_pat = input("Digite sua patente:".lower())
            cad_pat = cad_pat.replace(" ","")
            cad_senha = input("Digite sua senha:")
            # se a patente for valida cadastrar o usuario no txt
            situacao = False
            for patentes in patentes_validas:
                if cad_pat == patentes:
                    print("Cadastrado com sucesso !!!")
                    situacao = True
                    print(dec)
            if situacao == False:
                # Usuário só pode tentar 3 vezes
                print("Sua patente não é autorizada a entrar no navio, tente novamente.")
                print(dec)
                cont +=1
                tentativas = 3 - cont
                print("Você pode tentar cadastrar mais {} vezes.".format(tentativas))
                print(dec)
                if cont == 3:
                    print("O programa irá encerrar por motivos de segurança")
                    print("Invasor!!!")
                    # Toca o alarme
                    mixer.init()
                    mixer.music.load('alarme.mp3')
                    mixer.music.play()
                    time.sleep(10)

                    print(dec)
                    exit()

        else:
            if escolha != 3:
                cont += 1
                res = 3 - cont
                print(dec)
                print("Opção inválida, tente novamente, te restam mais {} tentativas.".format(res))
                print(dec)

                if cont == 3:
                    print("Você tentou mais de 3 vezes, por motivo de segurança o programa irá encerrar.")
                    exit()
            
main()