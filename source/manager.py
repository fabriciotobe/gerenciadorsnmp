#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# Arquivo que exibe um menu de tarefas, executa tarefas simples e convoca programas externos.

import subprocess
import tarfile
from datetime import datetime
import re
from settings import DB, INSTALL_PATH, TEMP_FOLDER
import dbmanager
import collector
import dbquery

def opt1():
    ''' Cadastro manual de Hosts. '''
    sair = 1
    subprocess.call('clear')
    while sair:
        l = []
        ip = raw_input('Endereco IP: ')
        host = raw_input('Nome do Host: ')
        if (ip != '') and (host != ''):
            l.append((ip, host))
            laux = dbmanager.reg_query_db('{0}{1}'.format(INSTALL_PATH, DB), l)
            dbmanager.reg_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), laux)
        else:
            print 'IP ou Host vazio nao sao validos'
        print '\n0) Sair'
        print '1) Continuar cadastrando'
        try:
            sair = input('Escolher: ')
        except:
            'Opcao invalida!'
            sair = 0

def opt2():
    ''' Inicia o scanner de IPs que verifica a disponibilidade do servico SNMP e fornece a opcao de cadastra-los '''
    subprocess.call('clear')
    ip_ini = raw_input('Endereco IP inicial: ')
    ip_fin = raw_input('Encereco IP final: ')
    subprocess.call(['./ipscanner.py', ip_ini, ip_fin])

def opt3():
    ''' Alteracao manual de Hosts. '''
    subprocess.call('clear')
    sair = 1
    while sair:
        l = []
        ip = raw_input('Endereco IP: ')
        host = raw_input('Nome do Host: ')
        if (ip != '') and (host != ''):
            dbmanager.alter_host_db('{0}{1}'.format(INSTALL_PATH, DB), (ip, host))
        else:
            print 'IP ou Host vazio nao sao validos'
        print '\n0) Sair'
        print '1) Continuar alterando'
        try:
            sair = input('Escolher: ')
        except:
            'Opcao invalida!'
            sair = 0

def opt4():
    ''' Realiza a Exclusao de Hosts '''
    sair = 1
    subprocess.call('clear')
    while sair:
        l = []
        ip = raw_input('Endereco IP: ')
        host = raw_input('Nome do Host: ')
        if (ip != '') and (host != ''):
            l.append((ip, host))
            dbmanager.del_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), l)
        else:
            print 'IP ou Host vazio nao sao validos'
        print '\n0) Sair'
        print '1) Continuar excluindo'
        try:
            sair = input('Escolher: ')
        except:
            'Opcao invalida!'
            sair = 0

def opt5():
    ''' Exibe o menu de Consultas '''
    subprocess.call('clear')
    while True:
        print '\nCONSULTAS\n0) Listas simples de Hosts\n1) Hosts\n2) Gerencial de usuarios e processos\n3) Memoria e Armazenamento\n4) Interfaces de Rede\n5) Voltar'
        op = raw_input('Escolher: ')
        print '\n'
        
        if op == '0': # Lista simples de Hosts
            subprocess.call('clear')
            subprocess.call('./dbmanager.py')
            
        elif op == '1': # Hosts 
            tipo = raw_input('Tipo de arquivo de saida: CSV ou TXT\nDigite c para CSV ou t para TXT: ')
            if tipo == 'c':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dest = raw_input('Digite o destino do arquivo CSV ou ENTER para padrao: ')
                if dest == '': dest = '{0}{1}'.format(INSTALL_PATH, TEMP_FOLDER)
                nome = raw_input('Digite o nome do arquivo CSV ou ENTER para padrao : ')
                if nome == '': nome = 'hostslists'
                if len(dest):
                    if dest[-1] != '/': dest = dest + '/'
                dbquery.hostlist_csv(dest, nome, idx)
            elif tipo == 't':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dbquery.hostlist_txt(idx)
            else:
                print 'Tipo inexistente. Digite c ou t como tipo de arquivo de saida'
                
        elif op == '2': # Gerencial de usuarios e processos
            tipo = raw_input('Tipo de arquivo de saida: CSV ou TXT\nDigite c para CSV ou t para TXT: ')
            if tipo == 'c':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dest = raw_input('Digite o destino do arquivo CSV ou ENTER para padrao: ')
                if dest == '': dest = '{0}{1}'.format(INSTALL_PATH, TEMP_FOLDER)
                nome = raw_input('Digite o nome do arquivo CSV ou ENTER para padrao : ')
                if nome == '': nome = 'sysusers_process'
                if len(dest):
                    if dest[-1] != '/': dest = dest + '/'
                dbquery.sysusers_process_csv(dest, nome, idx)
            elif tipo == 't':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dbquery.sysusers_process_txt(idx)
            else:
                print 'Tipo inexistente. Digite c ou t como tipo de arquivo de saida'
                
        elif op == '3':
            tipo = raw_input('Tipo de arquivo de saida: CSV ou TXT\nDigite c para CSV ou t para TXT: ')
            if tipo == 'c': # Memoria e Armazenamento
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dest = raw_input('Digite o destino do arquivo CSV ou ENTER para padrao: ')
                if dest == '': dest = '{0}{1}'.format(INSTALL_PATH, TEMP_FOLDER)
                nome = raw_input('Digite o nome do arquivo CSV ou ENTER para padrao : ')
                if nome == '': nome = 'memory_storage'
                if len(dest):
                    if dest[-1] != '/': dest = dest + '/'
                dbquery.memory_storage_csv(dest, nome, idx)
            elif tipo == 't':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dbquery.memory_storage_txt(idx)
            else:
                print 'Tipo inexistente. Digite c ou t como tipo de arquivo de saida'
                
        elif op == '4': # Interfaces de rede
            tipo = raw_input('Tipo de arquivo de saida: CSV ou TXT\nDigite c para CSV ou t para TXT: ')
            if tipo == 'c':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dest = raw_input('Digite o destino do arquivo CSV ou ENTER para padrao: ')
                if dest == '': dest = '{0}{1}'.format(INSTALL_PATH, TEMP_FOLDER)
                nome = raw_input('Digite o nome do arquivo CSV ou ENTER para padrao : ')
                if nome == '': nome = 'ifs'
                if len(dest):
                    if dest[-1] != '/': dest = dest + '/'
                dbquery.ifs_csv(dest, nome, idx)
            elif tipo == 't':
                idx = raw_input('Digite ID do Host ou ENTER para todos: ')
                dbquery.ifs_txt(idx)
            else:
                print 'Tipo inexistente. Digite c ou t como tipo de arquivo de saida'
                
        elif op == '5':
            break
        else:
            subprocess.call('clear')
            print 'Opcao inexistente. Escolha uma opcao de 0 a 5'

def opt6():
    ''' Executa o agendamento do collector, que ira coletar informacoes de gerenciamento dos hosts cadastrados. '''
    op = raw_input('Este processo podera solicitar a senha do root para alterar o arquivo de agendamento (/etc/crontab)\nDeseja continuar? s para sim ou n para nao: ')
    if op == 's':
        while True:
            op2 = raw_input('Deseja alterar ou remover agendamento? a para alterar ou r para remover: ')
            if op2 == 'a':
                t = raw_input('Informar em minutos (1 a 59) a frequencia da coletar de informacoes:  ')
                break
            elif op2 == 'r':
                t = '1'
                break
            else:
                print 'Escolha a ou r'
        try:
            if (int(t) > 0) and (int(t) < 60):
                y = 1
                content = []
                content_aux = []
                subprocess.call(['sudo', 'cp', '/etc/crontab', '{0}{1}crontab.bak'.format(INSTALL_PATH, TEMP_FOLDER)])
                u = subprocess.check_output('whoami').strip('\n')
                subprocess.call(['sudo', 'chown', u, '{0}{1}/crontab.bak'.format(INSTALL_PATH, TEMP_FOLDER)])
                with open('{0}{1}crontab.bak'.format(INSTALL_PATH, TEMP_FOLDER), 'r') as arq:
                    for i in arq.readlines():
                        content.append(i)
                subprocess.call(['sudo', 'chown', 'root', '{0}{1}crontab.bak'.format(INSTALL_PATH, TEMP_FOLDER)])
                for i in content:
                    c = i.find('collector.py')
                    if c > -1:
                        if op2 == 'a':
                            content_aux.append('*/{0} * * * * root {1}collector.py\n'.format(t, INSTALL_PATH))
                        elif op2 == 'r':
                            pass
                    else:
                        content_aux.append(i)
                if (op2 == 'a') and (y):
                    content_aux.append('*/{0} * * * * root {1}collector.py\n'.format(t, INSTALL_PATH))
                    y = 0
                with open('{0}{1}crontab'.format(INSTALL_PATH, TEMP_FOLDER), 'w') as arq:
                    for i in content_aux:
                        arq.writelines(i)
                subprocess.call(['sudo', 'cp', '{0}{1}crontab'.format(INSTALL_PATH, TEMP_FOLDER), '/etc/crontab'])
            else:
                print 'Forneca um valor entre 1 e 59.'
        except:
            print 'Erro! Fornecer um valor numerico.'
    elif op == 'n':
        pass
    else:
        'Escolha sim ou nao, operacao abortada.'
    
def opt7():
    ''' Faz uma chamada no coletor manual de informacoes que ira coletar as informacoes dos Hosts cadastrados. '''
    print '\n'
    subprocess.call('./collector.py')

def opt8():
    ''' Realiza o backup do Banco de Dados '''
    subprocess.call('clear')
    name = raw_input('Nome do arquivo de Backup: ')
    dest = raw_input('Salvar em: ')
    try:
        if dest[-1] != '/': dest = dest + '/'
        bckfile = ''.join([dest, name, '-', datetime.today().strftime('%d-%m-%Y-%H-%M-%S'), '.tar'])
        with tarfile.open(bckfile, 'a') as tf:
            tf.add('{0}{1}'.format(INSTALL_PATH, DB), DB.split('/')[-1])
            print 'Backup realizado com sucesso.\n{0}'.format(bckfile)
    except:
        print 'Falha ao gerar arquivo de backup.'

def opt9():
    ''' Realiza a limpeza do Banco de Dados
        E feito um drop de todas as tabelas de depois um create novamente '''
    while True:
        subprocess.call('clear')
        op = raw_input('Deseja realmente apagar todos os dados?\nDigite s para Sim e n para Nao. ')
        if op == 's':
            dbmanager.drop_tables_db('{0}{1}'.format(INSTALL_PATH, DB))
            dbmanager.create_tables_db('{0}{1}'.format(INSTALL_PATH, DB))
            break
        elif op == 'n':
            print 'Operacao cancelada.'
            break
        else:
            print 'Digite s ou n.'

def options():
    ''' Desenha o menu de opcoes '''
    print '\n------------------------------------------------------------\n1) Cadastro manual de Hosts\n2) Escanear range de IP\n3) Alterar cadastros de Hosts\n4) Excluir host cadastrado\n5) Consultar informacoes\n6) Agendar a coleta de informacoes\n7) Coletar manual de informacoes\n8) Backup da Base de Dados\n9) Limpar a Base de Dados\ns) Sair'    
    return raw_input('Escolher: ')

if __name__ == '__main__':
    subprocess.call('clear')
    sair = 1
    while sair:
        op = options()
        if op == '1': # Cadastro Manual de Hosts
            opt1()
        if op == '2': # Escanear range de IP
            opt2()
        if op == '3': # Alterar cadastros de Hosts
            opt3()
        if op == '4': # Excluir hosts cadastrados
            opt4()
        if op == '5': # Consultar Informacoes
            opt5()
        if op == '6': # Agendar coletar de informacoes
            opt6()
        if op == '7': # Coleta manual de informacoes
            opt7()
        if op == '8': # Backup da Base de Dados
            opt8()
        if op == '9': # Limpar Base de Dados
            opt9()
        elif op == 's': # Sair
            sair = 0
    print '\n'
