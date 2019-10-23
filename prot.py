from Crypto.PublicKey import RSA #Importando do pycrypto
from Crypto.Util.randpool import RandomPool
import sys

texto = "renan"
# fonte de dados randomica
pool = RandomPool(384)
pool.stir()
#randfunc(n) deve retornar uma string de dados aleatórios
randfunc = pool.get_bytes

#Definindo o tamanho da chave em bits
N = 256

K = ""

#Gerando as chaves
key = RSA.generate(N, randfunc)

#Pegando o valor da chave publica
pub_key = key.publickey()

#Criptografando
enc = pub_key.encrypt(texto, K)

#Descriptografando
dec = key.decrypt(enc)

print(enc)
print(dec)

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
    print("3 - Consultar as pessoas cadastradas;".center(98))
    print("4 - Sair.".center(70))
    print(dec)
    escolha = int(input("Opção:"))

    if (escolha == 1):
        patente = input("Digite sua patente:")
        senha = input("Digite sua senha:")
        # chamar a função de criptografar, e conferir se bate com os dados cadastrado no txt
    elif (escolha == 2):
        cad_pat = input("Digite sua patente:")
        cad_senha = input("Digite sua senha:")
        # se a patente for valida cadastrar o usuario no txt
    elif (escolha == 3):
        #verifica se a pessoa é autorizada a consultar
        patente = input("Digite sua patente:")
        senha = input("Digite sua senha:")
        # se for apresentara os cadastrados
    else:
        if escolha != 4:
            cont += 1
            res = 3 - cont
            print(dec)
            print("Opção inválida, tente novamente, te restam mais {} tentativas.".format(res))
            print(dec)

            if cont == 3:
                exit()
            
