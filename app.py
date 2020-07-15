"""Sistema de Gestão e Monitoramento Remoto de Pacientes
"""

import csv

### DATA STRUCTURE ###

# Estutura onde se guardam os dados dos pacientes e respetivas mensagens.
data = dict()

### MAIN FUNCTION ###

def main():
    """Função onde inicia o programa"""

    # Carregar os dados da aplicação.
    loadData('Pacientes.csv', 'MonitorizacaoDados.csv')

    # Apresentar um menu com as funcionalidades.
    loop = True

    while loop:

        menu()
        resposta = input('\nInsira a sua resposta [1-9]: ')

        if resposta == '9':
            loop = False
        elif resposta == '1':
            showAllPatients()
        elif resposta == '2':
            showPacient()
        elif resposta == '3':
            menuInsertPacient()
        elif resposta == '4':
            menuRemovePacient()
        elif resposta == '5':
            menuInsertMessage()
        elif resposta == '6':
            showMessage()
        elif resposta == '7':
            pass
        elif resposta == '8':
            showAnomalies()
        else:
            print('\n> Opção desconhecida...')
            parar()

    # Armazenar os dados da aplicação.
    saveData('Pacientes.csv', 'MonitorizacaoDados.csv')

### INTERFACE ###

def parar():
    """Este procedimento apresenta uma mensagem e pausa o programa."""

    input('\nPressione a tecla ENTER para prosseguir...')



def menu():
    """Apresenta na tela o menu principal."""

    print("\n", 30 * "-" , "MENU" , 30 * "-", sep='')
    print("1. Listar todos os pacientes")
    print("2. Ver um paciente")
    print("3. Inserir um novo paciente")
    print("4. Remover um paciente")
    print("5. Inserir uma nova mensagem")
    print("6. Ver uma mensagem")
    print("7. Remover uma mensagem")
    print("8. Listar situações anómalas")
    print("9. Exit")
    print(65 * "-")



def showAnomalies():
    """Procedimento que apresenta as situações anómalas na tela."""

    # Pesquisar em todos os pacientes.
    for phone in data:

        pacient = data[phone]

        showPacientInfo = True

        # Verificar cada mensagem armazenada em cada paciente.
        for sms in pacient['SMS']:

            pas = int( sms['PAS'] )
            pad = int( sms['PAD'] )
            o2  = int( sms['O2'] )

            # Caso os dados biológicos não se enquadrem num quadro de normalidade,
            # serão apresentados na tela.
            if pas <= 90 or pas >= 140 or pad <= 60 or pad >= 90 or o2 <= 95 or o2 >= 99:

                # A informação do paciente só deve ser apresentada um vez.
                if showPacientInfo == True:
                    print('\tID: ' + pacient['ID'], end=', ')
                    print('\tNOME: ' + pacient['NOME'], end=', ')
                    print('\tTELEFONE: ' + pacient['NUM_TEL'], end='\n')
                    print('\n\tPROBLEMA DE SAÚDE: ' + pacient['PROB_SAUDE'], end='\n')
                    showPacientInfo = False

                # A informação da mensagem é apresentada.
                print('\n\tSMS: ' + sms['DATA_ENVIO'] + ' ' + sms['HORA_ENVIO'])
                print('\tRD: ' + sms['RD'], end=', ')
                print('\tPAS: ' + sms['PAS'] + 'MMHG', end=', ')
                print('\tPAD: ' + sms['PAD'] + 'MMHG', end=', ')
                print('\tO2: ' + sms['O2'] + '%')

        print('-'*80)

    parar()



def showAllPatients():
    """ Este procedimento coloca na tela a lista com todos os pacientes."""

    # Pesquisa a informação de todos os pacientes.
    for phone in data:
        paciente = data[phone]

        # Apresentar a informação do paciente na tela.
        print('ID: {:>3}, NOME: {:25}, TELEFONE: {:9}, MORADA: {:40}, PROBLEMA DE SAÚDE: {}'\
            .format(paciente['ID'], paciente['NOME'], paciente['NUM_TEL'], paciente['MORADA'], paciente['PROB_SAUDE']))

    parar()



def showPacient():
    """Este procedimento apresenta na tela a informação armazenada para um paciente. """

    # Obter o número de telefone do paciente, data e hora de envio.
    numero = input('N.º telemóvel do paciente (<0 para voltar): ')
    while not numero.isnumeric() or not verifyPacientPhoneNumber(numero):
        if int(numero) < 0:
            return
        print('> O número de telefone {} não foi encontrado!'.format(numero))
        numero = input('N.º telemóvel do paciente: ')

    # Extrair a informação pessoal do paciente.
    paciente = data[numero]

    # Apresentar a informação do paciente na tela.
    print('ID: ' + paciente['ID'])
    print('NOME: ' + paciente['NOME'])
    print('TELEFONE: ' + paciente['NUM_TEL'])
    print('MORADA: ' + paciente['MORADA'])
    print('PROBLEMA DE SAÚDE: ' + paciente['PROB_SAUDE'])

    # Apresentar as informações das mensagens geradas a partir do número de
    # contacto do paciente.
    for sms in paciente['SMS']:
        print('\n\tSMS: ' + sms['DATA_ENVIO'] + ' ' + sms['HORA_ENVIO'])
        print('\tRD: ' + sms['RD'], end=', ')
        print('\tPAS: ' + sms['PAS'] + 'MMHG', end=', ')
        print('\tPAD: ' + sms['PAD'] + 'MMHG', end=', ')
        print('\tO2: ' + sms['O2'] + '%')

    parar()



def showMessage():
    """Este procedimento mostra a informação de uma dada mensagem na tela."""

    # Obter o número de telefone do paciente, data e hora de envio.
    numero = input('N.º telemóvel do paciente (<0 para voltar): ')
    while not numero.isnumeric() or not verifyPacientPhoneNumber(numero):
        if int(numero) < 0:
            return
        print('> O número de telefone {} não foi encontrado!'.format(numero))
        numero = input('N.º telemóvel do paciente: ')

    # Obter a data e hora de envio da mensagem.
    data_envio = input('Data de envio dos dados biológicos (dd/mm/aaaa): ')
    hora = input('Hora de envio dos dados biológicos (hh:mm): ')

    # Extrair a informação do paciente.
    paciente = data[numero]
    mensagem = {}

    # Pesquisar nas mensagens do paciente, aquela que foi enviada na data e hora
    # especificadas.
    for sms in paciente['SMS']:

        # Apresentar a informaçãod o paciente e da mensagem especificada na tela.
        if sms['DATA_ENVIO']==data_envio and sms['HORA_ENVIO']==hora:
            print('--- PACIENTE ---')
            print('ID: ' + paciente['ID'])
            print('NOME: ' + paciente['NOME'])
            print('TELEFONE: ' + paciente['NUM_TEL'])
            print('MORADA: ' + paciente['MORADA'])
            print('PROBLEMA DE SAÚDE: ' + paciente['PROB_SAUDE'])
            print('\n--- MENSAGEM (DATA: {} HORA: {}) ---'.format(sms['DATA_ENVIO'], sms['HORA_ENVIO']))
            print('Ritmo cardíaco: ' + sms['RD'])
            print('Pressão Arterial Sistólica: ' + sms['PAS'])
            print('Pressão Arterial Diastólica: ' + sms['PAD'])
            print('Oxigénio no sangue: ' + sms['O2'])

    parar()



def menuInsertMessage():
    """Menu para inserir uma nova mensagem na aplicação.

    Neste procedimento, são solicitados ao utilizador os dados da mensagem nova
    a inserir (número telemóvel do paciente, número do serviço de apoio, data de
    envio dos dados biométricos, hora de envio dos dados biométricos, do ritmo
    cardíaco, pressão arterial diastólica, pressão arterial diastólica, oxigénio
    no sangue) e depois é feita a inserção da mensagem.
    """

    # Obter dados do utlizador.
    numero = input('N.º telemóvel do paciente (<0 para voltar): ')
    while not numero.isnumeric() or not verifyPacientPhoneNumber(numero):
        if int(numero) < 0:
            return
        print('> O número de telefone {} não foi encontrado!'.format(numero))
        numero = input('N.º telemóvel do paciente: ')

    destino = input('N.º de serviço de apoio: ')
    while not destino.isnumeric():
        print('> Insira um valor numérico.')
        destino = input('N.º de serviço de apoio: ')

    data_envio = input('Data de envio dos dados biológicos (dd/mm/aaaa): ')
    hora = input('Hora de envio dos dados biológicos (hh:mm): ')

    rd = input('Ritmo cardíaco: ')
    while not rd.isnumeric():
        print('> Insira um valor numérico')
        rd = input('Ritmo cardíaco: ')

    pas = input('Pressão Arterial Sistólica: ')
    while not pas.isnumeric():
        print('> Insira um valor numérico')
        pas = input('Pressão Arterial Sistólica: ')

    pad = input('Pressão Arterial Diastólica: ')
    while not pad.isnumeric():
        print('> Insira um valor numérico')
        pad = input('Pressão Arterial Diastólica: ')

    o2 = input('Oxigénio no sangue: ')
    while not o2.isnumeric():
        print('> Insira um valor numérico')
        o2 = input('Oxigénio no sangue: ')

    # Inserir a mensagem no respetivo paciente.
    data[numero]['SMS'].append({'NUM_ORIGEM':numero, 'NUM_DESTINO':destino, \
        'DATA_ENVIO':data_envio, 'HORA_ENVIO':hora, 'RD':rd, 'PAS':pas, \
            'PAD':pad, 'O2':o2})



def menuRemoveMessage():
    """Menu para remover uma mensagem."""

    # Obter o número de telefone do paciente, data e hora de envio.
    numero = input('N.º telemóvel do paciente (<0 para voltar): ')
    while not numero.isnumeric() or not verifyPacientPhoneNumber(numero):
        if int(numero) < 0:
            return
        print('> O número de telefone {} não foi encontrado!'.format(numero))
        numero = input('N.º telemóvel do paciente: ')

    data_envio = input('Data de envio dos dados biológicos (dd/mm/aaaa): ')
    hora = input('Hora de envio dos dados biológicos (hh:mm): ')

    # Procurar a mensagem e eliminá-la.
    for mensagem in data[numero]['SMS']:
        if data_envio==mensagem['DATA_ENVIO'] and hora==mensagem['HORA_ENVIO']:
            data[numero]['SMS'].remove(mensagem)



def menuInsertPacient():
    """Menu para inserir um novo paciente na aplicação.

    Neste procedimento, é calculado o novo id de paciente e depois o utilizador
    é questionado sobre os novos dados do paciente. São feitas algumas verificações
    dos novos dados inseridos e por fim, o novo paciente é inserido na estrutura
    de dados.
    """

    # Obter um novo id de paciente.
    id = getNewId()

    # Obter os novos dados de paciente (Telefone, Nome, Morada e Problema de Saúde).
    telefone = input('Telefone (<0 para voltar): ')
    while not telefone.isnumeric():
        if int(telefone) < 0:
            return
        print('> Insira um valor numérico...')
        telefone = input('Telefone: ')

    nome = input('Nome: ')
    while not nome.isalpha() or len(nome) < 4:
        print('> Insira um nome com mais de 4 carateres (apenas carateres alfabéticos).')
        nome = input('Nome: ')

    morada = input('Morada: ')
    while len(morada) < 4:
        print('> Insira uma morada com mais de 4 carateres.')
        morada = input('Morada: ')

    saude = input('Problema de Saúde: ')
    while len(saude) < 4:
        print('> Insira uma expressão com mais de 4 carateres.')
        saude = input('Morada: ')

    # Inserir um novo paciente.
    data[telefone] = {'ID':id, 'NUM_TEL':telefone, 'NOME':nome, 'MORADA':morada, \
        'PROB_SAUDE':saude, 'SMS':list()}



def menuRemovePacient():
    """Menu para remover um paciente."""

    numero = input('N.º telemóvel do paciente (<0 para voltar): ')
    while not numero.isnumeric() or not verifyPacientPhoneNumber(numero):
        if int(numero) < 0:
            return
        print('> O número de telefone {} não foi encontrado!'.format(numero))
        numero = input('N.º telemóvel do paciente: ')

    if len(data[numero]['SMS']) > 0:

        print('\nAtenção: As mensagens seguintes também serão eliminadas:\n')

        for mensagem in data[numero]['SMS']:
            print('Para: {:9} Data: {:10} Hora: {:5} RD: {:3} PAS: {:3} PAD: {:3} O2: {:3}'\
                .format(mensagem['NUM_DESTINO'], mensagem['DATA_ENVIO'], mensagem['HORA_ENVIO'], \
                    mensagem['RD'], mensagem['PAS'], mensagem['PAD'], mensagem['O2']))

    resposta = input('\nDeseja eliminar o paciente com o número {} e as suas respetivas mensagens? (s/N): '.format(numero))

    if resposta=='s' or resposta=='S':
        del data[numero]



### DATA MANIPULATION ###

def verifyPacientPhoneNumber(number:str):
    """Verifica a existência de um número de telefone.

    Esta função verifica se o número de telefone passado como parâmetro existe na
    estrutura de dados. Caso o número exista a função devolve True, caso contrário
    devolve False.

    :param number: Número de telefone do paciente a verificar.
    :type id: str

    :returns: Caso o número exista devolve True. Senão devolve False.
    :rtype: bool
    """

    return number in data.keys()



def getNewId() -> str:
    """Obter o próximo ID de paciente disponível.

    Devolve o primeio ID de paciente disponível a partir da informação armazanedas
    na aplicação.

    :returns: Um novo id de paciente.
    :rtype: str
    """

    max = 0

    for key in data:
        id = int(data[key]['ID'])

        if id > max:
            max = id

    return str(max + 1)



def loadData(patients: str, messages: str) -> dict:
    """Carrega os dados dos pacientes e as suas mensagens de dois ficheiros.

    Abre o ficheiro com os dados dos pacientes e armazena-os num dicionário,
    utilizando o número de telefone como chave. Depois abre o ficheiro das
    mensagens e armazena-as junto das informações do respetivo cliente.

    :param patients: O nome do ficheiro com os dados dos pacientes.
    :type patients: str

    :param messages: O nome do ficheiro com os dados das mensagens.
    :type messages: str
    """

    # Carregar os dados dos pacientes.
    with open(patients, 'r', newline='', encoding='utf-8-sig') as filestream:
        datastream = csv.DictReader(filestream, delimiter=';')

        for patient in datastream:
            patient.update( {'SMS' : list() } )
            data[patient['NUM_TEL']] = patient

    # Carregar os dados das mensagens.
    with open(messages, 'r', newline='', encoding='utf-8-sig') as filestream:
        datastream = csv.DictReader(filestream, delimiter=';')

        for message in datastream:
            data[message['NUM_ORIGEM']]['SMS'].append(message)



def saveData(patients: str, messages: str):
    """Armazena os dados dos pacientes e as suas mensagens em dois ficheiros.

    Armazena os dados dos pacientes e as suas mensagens nos respetivos ficheiros.

    :param patients: O nome do ficheiro onde serão armazenados os dados dos pacientes.
    :type patients: str

    :param messages: O nome do ficheiro onde serão armazenados os dados das mensagens.
    :type messages: str
    """

    # Armazenar os dados dos pacientes.
    with open(patients, 'w', newline='', encoding='utf-8-sig') as patientsStream, \
        open(messages, 'w', newline='', encoding='utf-8-sig') as messagesStream:

        patientsWriter = csv.DictWriter(patientsStream, delimiter=";", \
            fieldnames=['ID', 'NUM_TEL', 'NOME', 'MORADA', 'PROB_SAUDE'])
        messagesWriter = csv.DictWriter(messagesStream, delimiter=";", \
            fieldnames=['NUM_ORIGEM', 'NUM_DESTINO', 'DATA_ENVIO', 'HORA_ENVIO',\
                 'RD', 'PAS', 'PAD', 'O2'])

        patientsWriter.writeheader()
        messagesWriter.writeheader()

        # Prepara para armazenar os dados dos pacientes (sem o campo SMS).
        for key in data:
            patientsWriter.writerow( { k:v for (k, v) in data[key].items() if k != 'SMS'} )

            for message in data[key]['SMS']:
                messagesWriter.writerow(message)


### PROGRAM ENTRY POINT ###

# Iniciar a execução do programa pela função main()
if __name__ == "__main__":
    main()

### END CODE ###