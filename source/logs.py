#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# Insere a entrada dos arquivos de logs.

from datetime import datetime
from settings import INSTALL_PATH, LOG_FOLDER

def logipscanner(l, tp):
    ''' Registra o log do ipscanner.
        l = Lista dos IPs
        tp = tipo de log '''
    with open('{0}{1}log_ipscanner.log'.format(INSTALL_PATH, LOG_FOLDER), 'a') as flog:
        if tp == 0: # Lista de Host que falharam no Ping
            for ip in l:
                flog.writelines('PING FAIL at {0}: Host {1} offline or unreachable. Host ignored for SNMP service.\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), ip))
        elif tp == 1: # Lista de Host que tiveram sucesso no Ping
            for ip in l:
                flog.writelines('PING SUCESS at {0}: Host {1} online.\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), ip))        
        elif tp == 2: # Lista de Host que falharam no Servico SNMP
            for ip in l:
                flog.writelines('SNMP FAIL at {0}: Host {1} online, but SNMP unable.\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), ip))
        elif tp == 3: # Lista de Host que tiveram sucesso no Servico SNMP
            for ip in l:
                flog.writelines('SNMP SUCESS at {0}: Host {1}-{2} online, but SNMP unable.\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), ip[0], ip[1]))

def logdbquery(msg):
    ''' Registra o log do dbquery
    msg = mensagem do log '''
    with open('{0}{1}log_dbquery.log'.format(INSTALL_PATH, LOG_FOLDER), 'a') as flog:
        flog.writelines('{0}: {1}\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), msg))

def logcollector(msg):
    ''' Registra o log do collector
        msg = mensagem do log '''
    with open('{0}{1}log_collector.log'.format(INSTALL_PATH, LOG_FOLDER), 'a') as flog:
        flog.writelines('{0}: {1}\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), msg))

def logdbmanager(msg):
    ''' Registra o log do dbmanager
        msg = mensagem do log '''
    with open('{0}{1}log_dbmanager.log'.format(INSTALL_PATH, LOG_FOLDER), 'a') as flog:
        flog.writelines('{0}: {1}\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), msg))

def logsnmpget(msg):
    ''' Registra o log do snmpget
        msg = mensagem do log '''
    with open('{0}{1}log_snmpget.log'.format(INSTALL_PATH, LOG_FOLDER), 'a') as flog:
        flog.writelines('{0}: {1}\n'.format(datetime.today().strftime('%d/%m/%Y %H:%M:%S'), msg))
