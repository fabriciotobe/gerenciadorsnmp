#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# O programa realiza coleta a informacao de todos os hosts cadastrados na tabela Hosts do Banco de Dados.
# A coleta pode ser feita manualmente ou atraves de agendamento no cron

import subprocess
from dbmanager import query_hosts_db
from settings import DB, INSTALL_PATH
from logs import logcollector
from datetime import datetime


def collector():
    '''O programa coleta a informacao de todos os hosts cadastrados na tabela Hosts e armazena no Banco de Dados. A coleta pode ser realizada diretamente ou via agendamento no cron.
       Para toda a atividade de coleta sao geradas entradas de log, que ficam armazenadas no subdiretorio log (padrao alteravel via settings.
           **Execucao**:
           Ao iniciar e feito uma query no Banco de Dados na tabela Hosts, obtendo todos os hosts cadastrados e seus respectivos IDs e IPs.
           Os hosts sao passado um a um para o programa snmpget que ira enviar gets, tratar os retornos e armazenar as informacoes no Banco de Dados.
           Todas as operacoes do collector sao armazenadas no log log_collector.log. '''
    # Chama uma query que listara todos os hosts cadastrados no Banco de Dados na tabela Hosts. E retornado uma lista de tuplas [(id, ip), (id, ip), ...]
    l = query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB))

    # Inicia a execucao do coletor se for retornada uma lista de Hosts
    if len(l) > 0:

        # Vai passando hosts a hosts e chamando o programa snmpget, que recolhe as informacoes de host
        for i in l:
            subprocess.call(['{0}snmpget.py'.format(INSTALL_PATH), str(i[0]), str(i[1])])
            print '\n'

            # Insere informacao de sucesso no log
            logcollector('SUCESSO, hosts coletados.')
    else:
        # Insere informacao de falha no log
        logcollector('FALHA, nenhum host para ser coletado.')
        print 'FALHA, Nenhum host para coletar.'

if __name__ == '__main__':
    collector()
