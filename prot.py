#NECESSÁRIO INSTALAR A BIBLIOTECA PYCRYPTODOME POIS ELA NÃO VEM PADRÃO COM O PYTHON
from Crypto.PublicKey import RSA #IMPORTANDO DA BIBLIOTECA O ALGORITMO RSA
from Crypto.Cipher import PKCS1_OAEP #O PKCS1_OAEP permite criar um 'recipiente' para as chaves

import pickle #Importado para conservar a estrutura da senha criptografa na hora de gravar

#NECESSÁRIO INSTALAR A BIBLIOTECA PYGAME POIS ELA NÃO VEM PADRÃO COM O PYTHON
from pygame import mixer #Necessário importar para a função Alarme()
import time #Necessário importar para usar na função Alarme()
from datetime import datetime
#FOI NECESSÁRIO RODAR O CÓDIGO ABAIXO UMA VEZ PARA GERAR O PAR DE CHAVES RSA E GUARDAR ELE

#chave_gerada = RSA.generate(2048)
#c = open('chave.pem','wb')
#c.write(chave_gerada.export_key('PEM'))
#c.close()


#FUNÇÃO RESPONSÁVEL POR CRIPTOGRAFAR A SENHA DO USUÁRIO
def Criptografar(senha):
    chave = open('chave.pem', 'r')
    ch = RSA.import_key(chave.read()) #essa linha importa a chave armazanada no arquivo 'chave.pem'

    encapsulada = PKCS1_OAEP.new(ch) #Passando as chaves para a cifra PKCS1_OAEP, para poder usar o metodo encrypt

    s_crip = encapsulada.encrypt(senha.encode('utf-8')) #criptografando a senha, necessário transformala em bytes, pois o PKCS1 não criptografa texto
    return s_crip #retorna a senha criptografada


#FUNÇÃO RESPONSÁVEL POR DESCRIPTOGRAFAR A SENHA DO USUÁRIO
def Decodificar(s_crip):
    chave = open('chave.pem', 'r')
    ch = RSA.import_key(chave.read())  #essa linha importa a chave armazanada no arquivo 'chave.pem'

    encapsulada = PKCS1_OAEP.new(ch)    #Passando as chaves para a cifra PKCS1_OAEP para poder usar o metodo decrypt

    senha_dec = encapsulada.decrypt(s_crip) #Descriptografando
    s_decodificada = senha_dec.decode('utf-8') # decodificando
    return s_decodificada # retornado a senha descriptografada e decodificada


#FUNÇÃO RESPONSÁVEL POR DISPARAR O ALARME
def Alarme():
    # Toca o alarme
    mixer.init() #INICIANDO O MIXER DA BIBLIOTECA PYGAME
    mixer.music.load('alarme.mp3') #CARREGANDOA  MÚSICA
    mixer.music.play() #tocando
    time.sleep(8) #TEMPO EM QUE A MÚSICA TOCA


#FUNÇÃO RESPONSÁVEL POR CADASTRAR A SENHA DO USUÁRIO
def Cadastrar(s, contador_cad, login, p):
    #Módulo de cadastro, o parametro s = senha, contador_cad = quantidade de usuários cadastrados, p = patente do usuario
    senha = Criptografar(s) #criptografando a senha do usuário
    dados = open('senha_usu.dat', 'ab') # Abrindo arquivo que recebera as senhas criptografadas
    pickle.dump(senha, dados) #gravando no arquivo 'senha_usu.dat', foi usado o metodo dump, pois ele conserva a estrutura do dado
    dados.close()  #fechando o arquivo

    qnt_cad = open('qnt_cad.txt','a') #Abrindo arquivo que armazena a quantidade de usuários cadastrados
    contador_cad += 1 # incrementando o contador
    grav_cont = str(contador_cad)
    qnt_cad.write(grav_cont + "\n") #adicionando o contador ao arquivo que controla a quantidade de usuários cadastrados
    qnt_cad.close()

    pt = open('log_cad.txt', 'a') #Abrindo o arquivo que vai receber o login e a patente
    pt.write(login + "," + p + "\n") #Gravando login a patente
    pt.close()


#FUNÇÃO RESPONSÁVEL POR REALIZAR O CONTROLE DE ACESSO DO NAVIO
def Acessar(login, s, p):
    #patente = p.replace(" ","")
    cont = 0 #recebe quantos usuários estão cadastrados no arquivo
    qnt_cad = open('qnt_cad.txt', 'r') #Abrindo arquivo com a quantidade de usuários cadastrados
    linhas = qnt_cad.readlines()#pegando todas a linhas do arquivo e tranformando em lista
    lista=[] #lista criada para fazer o controle da quantidade de usuários
    for i in linhas:
        lista.append(i) #a cada termo da lista linhas ele adiciona a lista 'lista'
    qnt_cad.close()
    for i in lista:
        cont += 1 #para cada termo na lista 'lista' ele incrementa o contador
    t_senha = [] #irá receber todas as senhas criptografadas
    senha = open('senha_usu.dat','rb') # Abrindo o arquivo que armazena as senhas criptografadas
    for i in range(cont):
        t_senha.append(pickle.load(senha)) #atribuindo as senhas a lista
    senha.close()
    cont_test = 0
    for senha in t_senha:
        senhas = Decodificar(senha) #para cada senha da lista o algoritmo descriptografa e armazena na variavel
        if senhas == s:
            #verifica se alguma das senhas bate com a do usuário
            status = True #atribuindo a variavel o valor true para sinalizar que a senha está cadastrada
            cont_test += 1 #Se a senha estiver cadastrada incrementa o contador
    if cont_test == 0:
        # Se nenhuma senha bateu com a entrada do usuário atribui o valor false pra variavel, sinalizando que a senha não está cadastrada
        status = False
    pt = open('log_cad.txt', 'r') #Abrindo o arquivo que recebe os logins/patentes cadastrados
    log_cadastrados = pt.readlines() # pegando todos os dados e atribuindo os mesmo a lista
    pt.close()
    status_final = False # iniciando a variavel que irá definir se o acesso é liberado ou não
    for log in log_cadastrados:
        #para cada linha na lista são executadas as linhas abaixo
        log = log.replace("\n","")
        log = log.split(",")
        if log[0] == login and status == True and log[1] == p.replace(" ",""):
            #verifica se o login, a patente, e a senha são validas, se sim o acesso é liberado
            print("Acesso liberado!!!")
            print("Bem-vindo {}".format(p))
            status_final = True
            dh = datetime.now()
            dht = dh.strftime('%d/%m/%y %H:%M')
            acessos = open('acessos.txt','a')
            acessos.write(p + " - " + dht + "\n")
            acessos.close()
            exit()
    return status_final


def Consultar(login, s, p):
    dec = "-" * 80
    #patente = p.replace(" ","")
    cont = 0 #recebe quantos usuários estão cadastrados no arquivo
    qnt_cad = open('qnt_cad.txt', 'r') #Abrindo arquivo com a quantidade de usuários cadastrados
    linhas = qnt_cad.readlines()#pegando todas a linhas do arquivo e tranformando em lista
    lista=[] #lista criada para fazer o controle da quantidade de usuários
    for i in linhas:
        lista.append(i) #a cada termo da lista linhas ele adiciona a lista 'lista'
    qnt_cad.close()
    for i in lista:
        cont += 1 #para cada termo na lista 'lista' ele incrementa o contador
    t_senha = [] #irá receber todas as senhas criptografadas
    senha = open('senha_usu.dat','rb') # Abrindo o arquivo que armazena as senhas criptografadas
    for i in range(cont):
        t_senha.append(pickle.load(senha)) #atribuindo as senhas a lista
    senha.close()
    cont_test = 0
    for senha in t_senha:
        senhas = Decodificar(senha) #para cada senha da lista o algoritmo descriptografa e armazena na variavel
        if senhas == s:
            #verifica se alguma das senhas bate com a do usuário
            status = True #atribuindo a variavel o valor true para sinalizar que a senha está cadastrada
            cont_test += 1 #Se a senha estiver cadastrada incrementa o contador
    if cont_test == 0:
        # Se nenhuma senha bateu com a entrada do usuário atribui o valor false pra variavel, sinalizando que a senha não está cadastrada
        status = False
    pt = open('log_cad.txt', 'r') #Abrindo o arquivo que recebe os logins/patentes cadastrados
    log_cadastrados = pt.readlines() # pegando todos os dados e atribuindo os mesmo a lista
    pt.close()
    status_final = False # iniciando a variavel que irá definir se o acesso é liberado ou não
    for log in log_cadastrados:
        #para cada linha na lista são executadas as linhas abaixo
        log = log.replace("\n","")
        log = log.split(",")
        if log[0] == login and status == True and log[1] == p.replace(" ",""):
            acessos = open('acessos.txt','r')
            log = acessos.readlines()
            acessos.close()
            print("Acessos ao navio:")
            print(dec)
            for linha in log:
                print(linha.replace("\n",""))
            print(dec)
            status_final = True
    return status_final
        

#FUNÇÃO PRINCIPAL
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
    while escolha != 4: #enquanto a escolha do usuario for diferente de 3(que é a opçao para sair) o algoritmo irá rodar
        print("Escolha o número correspondente ao que você quer realizar no sistema:".center(80))
        print("1 - Entrar no navio;".center(80))
        print("2 - Cadastrar;".center(74))
        print("3 - Consultar acessos;".center(82))
        print("4 - Sair.".center(70))
        print(dec)
        escolha = int(input("Opção:"))

        #a LISTA ABAIXO ARMAZENA AS PATENTES QUE SÃO AUTORIZADAS A SE CADASTRAR
        patentes_validas = ["capitãodecorveta", "capitãodefragata", "capitãodemareguerra", "contra-almirante", "vice-almirante", "almirantedeesquadra", "almirante"]
        #Verificando qual a funcionalidade do sistema
        if (escolha == 1):
            #Funcionalidade de acesso
            cont_ten = 0
            while cont_ten < 3:
                #o while acima faz o controle das tentativas de acesso ao navio
                patentee = input("Digite sua patente:")
                login = input("Digite seu login:")
                senha = input("Digite sua senha:")
                s = Acessar(login, senha, patentee) # chamando a função acessar e passando os parametros para ela
                if s == False:
                    #verificando se o login é valido ou não
                    print("Acesso negado!!!")
                    cont_ten += 1
                    vezes = 3 - cont_ten
                    if cont_ten == 3:
                        print("INVASOR DETECTADO!!!")
                        Alarme()                        
                        exit()
                    print("Você pode tentar fazer login só mais {} vezes".format(vezes))
            
        elif (escolha == 2):
            #funcionalidade de cadastro
            cont_tent = 0
            situacao = False
            while cont_tent < 3:
                if situacao == False:
                    cad_pat = input("Digite sua patente:".lower())
                    cad_pat = cad_pat.replace(" ","")
                    login = input("Digite seu login:")
                    cad_senha = input("Digite sua senha:")
                    # se a patente for valida cadastrar o usuario no txt

                    for patentes in patentes_validas:
                        if cad_pat == patentes:
                            cont_cad = 0
                            qnt_cad = open('qnt_cad.txt', 'r')
                            for i in qnt_cad:
                                cont_cad += 1

                            Cadastrar(cad_senha, cont_cad, login, cad_pat)
                            print("Cadastrado com sucesso !!!")
                            situacao = True
                            print(dec)
                            main()
                if situacao == False:
                    # Usuário só pode tentar 3 vezes
                    print("Sua patente não tem autorização para se cadastrar.")
                    print(dec)
                    cont_tent +=1
                    tentativas = 3 - cont_tent
                    if cont_tent == 3:
                        #Se o usuário tentar se cadastrar mais de 3 vezes o alarme dispara
                        print("INVASOR DETECTADO!!!")
                        Alarme()
                        print(dec)
                        exit()
                    print("Você pode tentar cadastrar mais {} vezes.".format(tentativas))
                    print(dec)
        elif escolha == 3:
            cont_tent = 0
            c = False
            while cont_tent < 3 and c == False:
                patentee = input("Digite sua patente:")
                login = input("Digite seu login:")
                senha = input("Digite sua senha:")
                print(dec)
                c = Consultar(login, senha, patentee) # chamando a função acessar e passando os parametros para ela
                if c == False:
                    #verificando se o login é valido ou não
                    print("Acesso negado!!!")
                    cont_tent += 1
                    vezes = 3 - cont_tent
                    if cont_ten == 3:
                        print("INVASOR DETECTADO!!!")
                        Alarme()                        
                        exit()
                    print("Você pode tentar fazer login só mais {} vezes".format(vezes))
        else:
            #controle de tentativas das funcionalidades
            if escolha != 4:
                cont += 1
                res = 3 - cont
                print(dec)
                print("Opção inválida, tente novamente, te restam mais {} tentativas.".format(res))
                print(dec)

                if cont == 3:
                    print("Você errou a escolha da funcionalidade mais de 3 vezes, por motivo de segurança o programa irá encerrar.")
                    Alarme()
                    exit()
            
main()
