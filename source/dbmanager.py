#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# O dbmanager manuseia todo do o Banco de Dados.
# Se o dbmanager for chamado diretamente ele imprime a lista de todos os Hosts cadastrados na tabela Hosts.

import sqlite3
from settings import DB, INSTALL_PATH
from logs import logdbmanager


def create_db(db):
    ''' Cria o arquivo do Banco de Dados vazio (sem tabelas).
        E utilizado por padrao o caminho do Banco de Dados definidos no settings.py
        As operacaoes de sucesso e falha sao inseridas no arquivo de log log_dbmanager '''
    try:
        # Apenas cria o arquivo do Banco de Dados vazio (sem tabelas)
        with open(db, 'a') as arq:
            pass

        # Insere sucesso no log
        logdbmanager('SUCESSO, arquivo {0} do Banco de Dados criado.'.format(db))
    except:
        #Insere falha no log
        logdbmanager('FALHA, nao e possivel criar o arquivo {0} do Banco de Dados.'.format(db))
        print 'Erro ao criar o arquivo do Banco de Dados.'


def create_tables_db(db):
    ''' Cria as tabelas no Banco de dados.
        O Banco de Dados utilizando e o definido no settings.py

        - Tabelas:

          - Hosts - Tabela que contem os Hosts cadastrados.
            Campos:
            id: identificador automatico.
            ip: ip do host.
            hostname: nome do host.

          - Group1 - Tabela que armazena as informacoes do Grupo 1.
            Campos:
            id: identificados automatico
            idhost: id do host
            sysDescr: descricao do sistema, contem sistema operacional, distribuicao, processador, arquitetura, data e hora.
            sysUpTime: tempo que o sistema esta ligado.
            sysContact: contato do sistema.
            sysLocation: local do sistema.
            sysServices: servicos do sistema.
            data: Data da coleta.
            hora: Hora da coleta.

          -Group2 - Tabela que armazena as informacoes do Grupo 2
            Campos:
            id: identificador automatico.
            idhost: id do host.
            hrSystemUsers: usuarios logados.
            hrSystemProcess: total de processos rodando.
            data: data da coleta.
            hora: horario da coleta.

          - Group3 - Tabela que armazena as informacoes do Grupo 3
            Campos:
            id: identificador automatico.
            idhost: id do host.
            Memory: memoria do sistema.
            hrStorageDescr: descricao da unidade de armazenamento.
            hrStorageSize: tamanho da unidade de armazenamento.
            hrStorageUsed: espaco usado na unidade de armazenamento.
            data: Data da coleta.
            hora: horario da coleta.

          - Group6 - Tabela que armazena as informacoes do Grupo 6
            Campos:
            id: identificador automatico.
            idhost: id do host.
            ipAdEntAddr: enderecos de ip separados por "|".
            ipAdEntifIndex: identificador da interface de rede do host separados por "|".
            ipAdEndNetMask: mascara de rede separados por "|"
          '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Inicia a criacao das tabelas no Banco de Dados.
        c.execute("CREATE TABLE Hosts(id INTEGER PRIMARY KEY, ip TEXT, hostname TEXT)")
        c.execute("CREATE TABLE Group1(id INTEGER PRIMARY KEY, idhost INTEGER, sysDescr TEXT, sysUpTime TEXT, sysContact TEXT, sysLocation TEXT, sysServices TEXT, data DATETIME, hora TEXT)")
        c.execute("CREATE TABLE Group2(id INTEGER PRIMARY KEY, idhost INTEGER, hrSystemUsers TEXT, hrSystemProcess TEXT, data DATETIME, hora TEXT)")
        c.execute("CREATE TABLE Group3(id INTEGER PRIMARY KEY, idhost INTEGER, Memory TEXT, hrStorageDescr TEXT, hrStorageSize TEXT, hrStorageUsed TEXT, data DATETIME, hora TEXT)")
        c.execute("CREATE TABLE Group6(id INTEGER PRIMARY KEY, idhost INTEGER, ipAdEntAddr TEXT, ipAdEntifIndex TEXT, ipAdEntNetMask TEXT, data DATETIME, hora TEXT)")
        print 'Tabelas criadas com sucesso.'
        con.commit()
        c.close
        con.close

        # Insere sucesso no log
        logdbmanager('SUCESSO, Tabelas criadas no Banco de Dados {0}.'.format(db))
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel criar as tabelas no Banco de Dados {0}.'.format(db))
        print 'Erro ao criar tabelas no Banco de Dados.'


def drop_tables_db(db):
    ''' Exclui as tabelas do Banco de Dados.
        O Banco de Dados utilizando e o definido no settings.py.
         '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Comandos de exclusao de tabela
        c.execute("DROP TABLE Hosts")
        c.execute("DROP TABLE Group1")
        c.execute("DROP TABLE Group2")
        c.execute("DROP TABLE Group3")
        c.execute("DROP TABLE Group6")
        con.commit()
        print 'Tabelas do Banco de dados deletadas com sucesso.'
        c.close
        con.close

        # Insere sucesso no log
        logdbmanager('SUCESSO, Tabelas excluidas do Banco de Dados {0}.'.format(db))
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel excluir tabelas do Banco de Dados {0}.'.format(db))
        print 'Erro ao deletar tabelas do Banco de Dados.'


def reg_hosts_db(db, hosts_list):
    ''' Insere informacoes no Banco de Dados na tabela Hosts.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list contem uma lista de tuplas com ips e nomes de host no formato [(ip, nomedohost), (ip, nomedohost), ...]
        '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa no comando INSERT para cada host da lista.
        for data in hosts_list:
            c.execute("INSERT INTO Hosts VALUES(NULL, '{0}', '{1}')".format(data[0], data[1]))

            # Insere sucesso no log
            logdbmanager('SUCESSO ao inserir Host {0} - {1} no Banco de Dados {2}.'.format(data[1], data[0], db))
            print 'Host {0} - {1} inserido no Banco de Dados com sucesso.'.format(data[1], data[0])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel inserir Hosts no Banco de Dados {0}.'.format(db))
        print 'Erro ao inserir hosts no Banco de Dados.'


def del_hosts_db(db, hosts_list):
    ''' Exclui hosts do Banco de Dados na tabela Hosts.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list contem uma lista de tuplas com ips e nomes de host no formato [(ip, nomedohost), (ip, nomedohost), ...]. Pode ser passado uma lista, mas na chamada interna do programa manager e passado uma lista com uma tupla apenas.
        '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa o comando DELETE para cada host da lista
        for data in hosts_list:
            c.execute("DELETE FROM Hosts WHERE ip = '{0}'".format(data[0]))

            # Insere sucesso no log
            logdbmanager('SUCESSO ao excluir Host {0} - {1} do Banco de Dados {2}.'.format(data[1], data[0], db))
            print 'Host {0} - {1} excluido do Banco de Dados com sucesso.'.format(data[1], data[0])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel excluir Hosts do Banco de Dados {0}.'.format(db))
        print 'Erro ao excluir hosts do Banco de Dados.'


def reg_query_db(db, hosts_list):
    ''' Recebe uma lista de hosts, executa um SELECT na tabela hosts e retorna uma lista com os IPs que nao existem na tabela Hosts.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list contem lista de IPs. '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()
        l = []
        ip = ''

        # Salva a lista de hosts em uma segunda lista
        # Cria uma copia da lista
        for i in hosts_list:
            l.append(i)
        try:
            # Passa um a um os hosts
            for idx in hosts_list:
                # Executa um SELECT no host para checar se ele esta cadastrado na tabela Hosts
                for row in c.execute("SELECT * FROM Hosts WHERE ip = '{0}'".format(idx[0])):

                    # Quando encontrado registro, salva o ip em uma variavel
                    ip = row[1]

                # Verifica se foi localizado um cadastro do host
                if ip:
                    # Insere uma entrada informando que o host sera ignorado para cadastro
                    logdbmanager('IGNORADO, {0} ja esta cadastrado no Banco de Dados {1}.'.format(ip, db))
                    print '{0} ja esta cadastrado, novo registro ignorado.'.format(ip)

                    # Remove o hosts localizado da lista secundaria
                    l.remove(idx)
                    del ip
        except:
            pass
        c.close
        con.close
    except:
        # Insere falha no log, caso nao seja possivel consultar
        logdbmanager('FALHA, nao e possivel verificar hosts cadastrados no Banco de Dados {0}.'.format(db))
        print 'Erro ao verificar Hosts cadastrados.'

    # Retorna a lista dos nao cadastrados
    return l


def alter_host_db(db, hosts_list):
    ''' Altera os dados de um Host fornecido.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_lists contem uma tupla com ip e nome do host no formato [(ip, nomedohost), (ip, nomedohost), ...]. E fornecido apenas um host por vez. '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um SELECT buscando o cadatro do Host
        query = c.execute("SELECT * FROM Hosts WHERE ip = '{0}'".format(hosts_list[0]))

        # for convocado apenas para pegar as informacoes contidas antigas para inserir no log
        for i in query:
            # Executa uma UPDATE no host, atualizando as informacoes
            c.execute("UPDATE Hosts SET ip = '{0}', hostname = '{1}' WHERE ip = '{0}'".format(hosts_list[0], hosts_list[1]))

            # Insere sucesso no log
            logdbmanager('SUCESSO, Host {0} - {1} alterado no Banco de Dados {2}. IP anterior: {3}, Nome anterior: {4}'.format(hosts_list[1], hosts_list[0], db, i[1], i[2]))
            print 'Host {0} - {1} alterado no Banco de Dados com sucesso.'.format(hosts_list[1], hosts_list[0])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel alterar hosts no Banco de Dados {0}.'.format(db))
        print 'Falha ao alterar dados no Banco de Dados.'


def query_hosts_db(db, idx=''):
    ''' Executa um SELECT na tabela de Hosts e retorna a lista de tupla de Hosts no formato [(id, ip, hostname), (id, ip, hostname), ...].
        O Banco de Dados utilizando e o definido no settings.py.
        idx contem um id de Host, se fornecido, executa a consulta somente daquele host. Padrao e vazio, que determina a consulta de todos os hosts. '''
    l = []
    try:
        w = ''

        # Verifica se a variavel idx tem valor, se tiver adiciona a clausula WHERE id = idx na consulta
        if idx:
            w = ' WHERE id = {0}'.format(idx)
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa a consulta
        query = c.execute("SELECT * FROM Hosts{0}".format(w))

        # Percorre o resultado da consulta inserindo o resultado em uma lista de tuplas
        for i in query:
            l.append((i[0], i[1], i[2]))
        con.commit()
        c.close
        con.close

        # Inserer sucesso no log
        logdbmanager('SUCESSO, lista de hosts gerada.')

        # Retorna a lista com hosts
        return l
    except:
        # Inserer falha no log
        logdbmanager('FALHA, nao e possivel gerar a lista de Hosts cadastrado no Banco de Dados {0}.'.format(db))
        print 'Falha ao gerar lista de Hosts cadastrados no Banco de Dados.'

        # Retorna a lista vazia
        return l


def reg_group1_db(db, hosts_list):
    ''' Grava do Dados do Grupo 1 no Banco de Dados.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list contem uma lista com idhost, sysDescr, sysUpTime, sysContact, sysLocation, sysServices, data e hora.
        '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa o INSERT na tabela Group1
        # {0}idhost, {2}sysDescr, {3}sysUpTime, {4}sysContact, {5}sysLocation, {6}sysServices, {7}data, {8}hora
        c.execute("INSERT INTO Group1 VALUES(NULL, {0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(hosts_list[0], hosts_list[2], hosts_list[3], hosts_list[4], hosts_list[5], hosts_list[6], hosts_list[7], hosts_list[8]))

        # Insere sucesso no log
        logdbmanager('SUCESSO, Grupo 1 do Host id {0}, ip {1} inserido no Banco de Dados {2}.'.format(hosts_list[0], hosts_list[1], db))
        print 'Grupo 1 do Host id {0}, ip {1} inserido no Banco de Dados com sucesso.'.format(hosts_list[0], hosts_list[1])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel inserir dados no Grupo 1 no Banco de Dados {0}.'.format(db))
        print 'Erro ao inserir hosts no Banco de Dados.'


def query_group1_db(db, idhost):
    ''' Executa um SELECT na tabela de Group1 e retorna todos os dados das consulta automatica do ID fornecido.
        O Banco de Dados utilizando e o definido no settings.py.
        idhost contem o ID do host consultado.
        '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um SELECT na tabela Group1 para o host idhost
        query = c.execute("SELECT * FROM Group1 WHERE idhost = {0} ORDER BY id DESC".format(idhost))

        # Percorre todos os resultados da consulta e armazena em uma lista no formato de tupla
        for i in query:
            l = (i[2], i[3], i[4], i[5], i[6], i[7], i[8])

            # Sai do for, para o Grupo 1, somente a ultima informacao e relevante
            break
        con.commit()
        c.close
        con.close

        # Insere sucesso no log
        logdbmanager('SUCESSO, Listagem do Grupo 1 gerada.')
        return l
    except:
       # Insere falha no log
        logdbmanager('FALHA ao gerar dados do Grupo 1 para o ID {0}.'.format(idhost))
        print 'Falha ao gerar dados do Grupo 1 para o ID {0}.'.format(idhost)


def reg_group2_db(db, hosts_list):
    ''' Grava do Dados do Grupo 2 no Banco de Dados.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list conte uma lista com idhost, hrSystemUsers, hrSystemProcess, data e hora.
        '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um INSERT na tabela Group2
        # {0}idhost, {2}hrSystemUsers, {3}hrSystemProcess, {4}data, {5}hora
        c.execute("INSERT INTO Group2 VALUES(NULL, {0}, '{1}', '{2}', '{3}', '{4}')".format(hosts_list[0], hosts_list[2], hosts_list[3], hosts_list[4], hosts_list[5]))

        # Insere sucesso no log
        logdbmanager('SUCESSO, Grupo 2 do Host id {0}, ip {1} inserido no Banco de Dados {2}.'.format(hosts_list[0], hosts_list[1], db))
        print 'Grupo 2 do Host id {0}, ip {1} inserido no Banco de Dados com sucesso.'.format(hosts_list[0], hosts_list[1])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel inserir dados no Grupo 2 no Banco de Dados {0}.'.format(db))
        print 'Erro ao inserir hosts no Banco de Dados.'


def query_group2_db(db, idhost):
    ''' Executa um SELECT na tabela de Group2 e retorna uma lista com todos os dados das consulta automatica do ID fornecido.
        O Banco de Dados utilizando e o definido no settings.py.
        idhost contem o ID do host consultado.
        '''
    try:
        l = []
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um SELECT na tabela Group2 para o host idhost
        query = c.execute("SELECT * FROM Group2 WHERE idhost = {0} ORDER BY data, hora".format(idhost))

        # Percorre todos os resultados da consulta e armazena em uma lista no formato de tupla
        for i in query:
            l.append(i)
        con.commit()
        c.close
        con.close

        # Insere sucesso no log
        logdbmanager('SUCESSO, Listagem do Grupo 2 gerada.')
        return l
    except:
       # Insere falha no log
        logdbmanager('FALHA ao gerar dados do Grupo 2 para o ID {0}.'.format(idhost))
        print 'Falha ao gerar dados do Grupo 2 para o ID {0}.'.format(idhost)


def reg_group3_db(db, hosts_list):
    ''' Grava do Dados do Grupo 3 no Banco de Dados.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list contem a lista com idhost, Memory, hrStorageDescr, hrStorageSize, hrStorageUsed, data e hora '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um INSERT na tabela Group3
        # {0}idhost, {2}Memory, {3}hrStorageDescr, {4}hrStorageSize, {5}hrStorageUsed, {6}data, {7}hora
        c.execute("INSERT INTO Group3 VALUES(NULL, {0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(hosts_list[0], hosts_list[2], hosts_list[3], hosts_list[4], hosts_list[5], hosts_list[6], hosts_list[7]))

        # Insere sucesso no log
        logdbmanager('SUCESSO, Grupo 3 do Host id {0}, ip {1} inserido no Banco de Dados {2}.'.format(hosts_list[0], hosts_list[1], db))
        print 'Grupo 3 do Host id {0}, ip {1} inserido no Banco de Dados com sucesso.'.format(hosts_list[0], hosts_list[1])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel inserir dados no Grupo 3 no Banco de Dados {0}.'.format(db))
        print 'Erro ao inserir hosts no Banco de Dados.'


def query_group3_db(db, idhost):
    ''' Executa um select na tabela de Group3 e retorna uma lista com todos os dados da consulta automatica do ID fornecido
        O Banco de Dados utilizando e o definido no settings.py.
        idhost contem o ID do host consultado. '''
    try:
        l = []
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um SELECT na tabela Group3 para o host idhost
        query = c.execute("SELECT * FROM Group3 WHERE idhost = {0} ORDER BY data, hora".format(idhost))

        # Percorre todos os resultados da consulta e armazena em uma lista no formato de tupla
        for i in query:
            l.append(i)
        con.commit()
        c.close
        con.close

        # Insere sucesso no log
        logdbmanager('SUCESSO, Listagem do Grupo 3 gerada.')
        return l
    except:
        # Insere falha no log
        logdbmanager('FALHA ao gerar dados do Grupo 3 para o ID {0}.'.format(idhost))
        print 'Falha ao gerar dados do Grupo 3 para o ID {0}.'.format(idhost)


def reg_group6_db(db, hosts_list):
    ''' Grava do Dados do Grupo 6 no Banco de Dados.
        O Banco de Dados utilizando e o definido no settings.py.
        hosts_list contem uma lista com idhost, ipAdEntAddr, ipAdEntifIndex e ipAdEndNetMask '''
    try:
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um INSERT na tabela Group3
        # {0}idhost, {2}ipAdEntAddr, {3}ipAdEntifIndex, {4}ipAdEndNetMask
        c.execute("INSERT INTO Group6 VALUES(NULL, {0}, '{1}', '{2}', '{3}', '{4}', '{5}')".format(hosts_list[0], hosts_list[2], hosts_list[3], hosts_list[4], hosts_list[5], hosts_list[6]))

        # Insere sucesso no log
        logdbmanager('SUCESSO, Grupo 6 do Host id {0}, ip {1} inserido no Banco de Dados {2}.'.format(hosts_list[0], hosts_list[1], db))
        print 'Grupo 6 do Host id {0}, ip {1} inserido no Banco de Dados com sucesso.'.format(hosts_list[0], hosts_list[1])
        con.commit()
        c.close
        con.close
    except:
        # Insere falha no log
        logdbmanager('FALHA, nao e possivel inserir dados no Grupo 6 no Banco de Dados {0}.'.format(db))
        print 'Erro ao inserir hosts no Banco de Dados.'


def query_group6_db(db, idhost):
    ''' Executa um select na tabela de Group6 e retorna uma lista com todos os dados da consulta automatica do ID fornecido.
        O Banco de Dados utilizando e o definido no settings.py.
        idhost = ID do host consultado '''
    try:
        l = []
        con = sqlite3.connect(db)
        c = con.cursor()

        # Executa um SELECT na tabela Group6 para o host idhost
        query = c.execute("SELECT * FROM Group6 WHERE idhost = {0} ORDER BY data, hora".format(idhost))

        # Percorre todos os resultados da consulta e armazena em uma lista no formato de tupla
        for i in query:
            l.append(i)
        con.commit()
        c.close
        con.close

        # Insere sucesso no log
        logdbmanager('SUCESSO, Listagem do Grupo 6 gerada.')
        return l
    except:
        # Insere falha no log
        logdbmanager('FALHA ao gerar dados do Grupo 6 para o ID {0}.'.format(idhost))
        print 'Falha ao gerar dados do Grupo 6 para o ID {0}.'.format(idhost)

if __name__ == '__main__':
    l = query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB))
    if len(l) > 0:
        print 'ID\tIP\tHOST'
        for i in l:
            print '{0}\t{1}\t{2}'.format(i[0], i[1], i[2])
