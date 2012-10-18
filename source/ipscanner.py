#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# Para ser executador, ipscanner exige um range de IPs.
# E feito uma varredura no range de IPs e exibido quais estao online (atraves de ping).
# Com os Hosts online, e disparado um comando SNMP para obter o nome do Host e apresentado quais estao com SNMP ativo.

import argparse
import threading
from re import findall
from subprocess import check_output
import socket
from pysnmp.entity.rfc3413.oneliner import cmdgen
from time import sleep
from logs import logipscanner
import settings
from dbmanager import reg_hosts_db, reg_query_db

parser = argparse.ArgumentParser(description='Executar a varredura de um range de IPs, verifica disponibilidade do Servico SNMP e fornece a opcao de cadastra-los.')
parser.add_argument('IPi', help='Initial IP.')
parser.add_argument('IPf', help='Final IP.')
args = parser.parse_args()


def iplist(ip_ini, ip_fin):
    ''' Gera a lista de IPs do range fornecido. '''
    x = ip_ini.split('.')
    y = ip_fin.split('.')
    l = []

    # Faz a validacao dos ips
    if len(x) != 4 or len(y) != 4:
        print 'Erro na sequencia de IPs fornecidos.'
    try:
        if x[3] > y[3]:
            ip_ini, ip_fin = ip_fin, ip_ini
            x, y = y, x
        s = x[0:3]
        for i in xrange(int(x[3]), int(y[3]) + 1):
            l.append('.'.join(['.'.join(s), str(i)]))
    except:
        print 'Erro!'
    return l


def checkhostonline(ip):
    ''' Envia um ping para um Host e retorna verdadeiro ou falso. '''
    try:
        ping = check_output(['ping', '-c', '4', ip])
        pingstats = findall(r'.*bytes from.*: icmp_req=(.*) ttl=(.*) time=(.*) ms.*', ping)
        chk = 0
        for i in xrange(4):
            if pingstats[i][1] > 0:
                chk += 1
        if chk > 1:
            return True
        else:
            return False
    except:
        return False


def checksnmpservice_old(target, port, timeout):
    ''' Verifica se um Host de um porta UDP aberta e retorna verdadeiro ou falso. '''
    chk = 10
    for i in xrange(10):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(timeout)
            s.gettimeout()
            s.connect((target, int(port)))
            s.close()
        except:
            chk -= 1
            sleep(5)
    if chk:
        return True
    else:
        return False


def checksnmpservice(target):
    ''' Verifica se o Host responde a um SNMP Get e retorna verdadeiro ou falso seguido do nome do Host '''
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(settings.DEFAULT_COMMUNITY),
        cmdgen.UdpTransportTarget((target, settings.DEFAULT_PORT)),
        cmdgen.MibVariable(settings.SNMP_VERSION, settings.DEFAULT_FIELD, 0)
    )
    if errorIndication is None:
        return True, varBinds[0][1]
    else:
        return False, ''


def ctrl(lip=[]):
    ''' Gerencia as listas de sucesso e falha '''
    lsucess = []
    lfail = []
    lsnmpsucess = []
    lsnmpfail = []
    print '\n'
    if len(lip) == 0:
        lip = iplist(args.IPi, args.IPf)  # Generate the IP list
    print 'Aguarde, o processo pode demorar dependendo do numero de Hosts...'
    print 'HOST\t\t\tSTATUS'
    for ip in lip:  # Checking ping agains the IPs
        if checkhostonline(ip):
            lsucess.append(ip)
            print '{0}\t\t\033[32mOnline\033[0;0m'.format(ip)
        else:
            lfail.append(ip)
            print '{0}\t\t\033[31mOffline\033[0;0m'.format(ip)
    print '\n'

    ## Loggins Ping Sucess and Ping Fails
    if len(lfail) > 0:
        logipscanner(lfail, 0)
    if len(lsucess) > 0:
        logipscanner(lsucess, 1)

    ## Checking SNMP Service on the IPs with Ping Sucess
    print 'HOST\t\t\tHOST NAME\t\t\tSNMP'
    for ip in lsucess:
        snmpserv = checksnmpservice(ip)
        if snmpserv[0]:
            lsnmpsucess.append((ip, snmpserv[1]))
            print '{0}\t\t{1}\t\t\t\033[32mOk\033[0;0m'.format(ip, snmpserv[1])
        else:
            lsnmpfail.append(ip)
            print '{0}\t\t\t\t\t\t\033[31mFail\033[0;0m'.format(ip)

    ## Loggins SNMP Sucess and SNMP Fails
    if len(lsnmpfail) > 0:
        logipscanner(lsnmpfail, 2)
    if len(lsnmpsucess) > 0:
        logipscanner(lsnmpsucess, 3)
    return lsnmpsucess, lfail, lsnmpfail


def reg_hosts(l):
    laux = reg_query_db('{0}{1}'.format(settings.INSTALL_PATH, settings.DB), l)
    reg_hosts_db('{0}{1}'.format(settings.INSTALL_PATH, settings.DB), laux)


def options():
    ''' Desenha o menu de opcoes do ipscanner '''
    print '\n------------------------------------------------------------\n1) Cadastrar Hosts com Servico SNMP ativo no Banco de Dados?\n2) Tentar novamente Hosts com falha no Ping?\n3) Tentar novamente Hosts com falha no SNMP?\n4) Cancelar.'
    return raw_input('Escolher: ')


if __name__ == '__main__':
    mainlist = ctrl()
    op = '0'
    while op != '1':
        op = options()
        if op == '1':
            if len(mainlist[0]) > 0:
                print '\n'
                reg_hosts(mainlist[0])
            else:
                print 'Nenhum Host para ser salvo.'
        elif op == '2':
            if len(mainlist[1]) > 0:
                secondarylist = ctrl(mainlist[1])
            else:
                print 'Nenhum Host com falha de ping.'
        elif op == '3':
            if len(mainlist[2]) > 0:
                secondarylist = ctrl(mainlist[2])
            else:
                print 'Nenhum Host com falha de SNMP.'
        elif op == '4':
            break
        else:
            print '\nEscolher uma das opcoes disponiveis.'
        try:
            if secondarylist[0] > 0:
                for ip in secondarylist[0]:
                    mainlist[0].append(ip)
        except:
            pass
    print '\n'
