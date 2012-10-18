#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# O programa envia as solicitacoes para os hosts para obter suas informacoes.
# Para ser chamado diretamente, deve ser informado o ID do host cadastrado no Banco de Dados e o ip
#
#
# As solicitacoes sao enviadas por grupos. Em seguida estao os grupos descritos com suas informacoes que podem ser obtidas
#
# Grupo 1: system
#        oid, nome do campo, utilizado - descricao
#        1.3.6.1.2.1.1.1, sysDescr
#        1.3.6.1.2.1.1.2, sysObjectID, nao
#        1.3.6.1.2.1.1.3, sysUpTime
#        1.3.6.1.2.1.1.4, sysContact
#        1.3.6.1.2.1.1.5, sysName, nao
#        1.3.6.1.2.1.1.6, sysLocation
#        1.3.6.1.2.1.1.7, sysServices
#
# Grupo 2: hrSystem
#       oid, nome do campo, utilizado - descricao
#       1.3.6.1.2.1.25.1.1, hrSystemUptime, nao
#       1.3.6.1.2.1.25.1.2, hrSystemDate, nao
#       1.3.6.1.2.1.25.1.3, hrSystemInitialLoadDevice, nao
#       1.3.6.1.2.1.25.1.4, hrSystemInitialLoadParameters, nao
#       1.3.6.1.2.1.25.1.5, hrSystemUsers
#       1.3.6.1.2.1.25.1.6, hrSystemProcess
#       1.3.6.1.2.1.25.1.7, hrSystemMaxProcess, nao
#
# Grupo 3: hrStorage
#       oid, nome do campo, utilizado - descricao
#       1.3.6.1.2.1.25.2.2.0, hrMemorySize
#       1.3.6.1.2.1.25.2.3.1.1, hrStorageIndex
#       1.3.6.1.2.1.25.2.3.1.2, hrStorageType, nao
#       1.3.6.1.2.1.25.2.3.1.3, hrStorageDescr
#       1.3.6.1.2.1.25.2.3.1.4, hrStorageAlloc, nao
#       1.3.6.1.2.1.25.2.3.1.5, hrStorageSize
#       1.3.6.1.2.1.25.2.3.1.6, hrStorageUsed
#       1.3.6.1.2.1.25.2.3.1.7, hrStorageAllocationFailure, nao
#
# Grupo 4: hrSWRun - NAO ESTA SENDO UTILIZADO 
#        oid, nome do campo, utilizado - descricao
#        1.3.6.1.2.1.25.4.2.1.1, hrSWRunIndex
#        1.3.6.1.2.1.25.4.2.1.2, hrSWRunName - nome do processo
#        1.3.6.1.2.1.25.4.2.1.3, hrSWRunID - id do processo
#        1.3.6.1.2.1.25.4.2.1.4, hrSWRunPath - caminho do executavel/programa
#        1.3.6.1.2.1.25.4.2.1.5, hrSWRunParameters - paramentros passado para o executavel/programa
#        1.3.6.1.2.1.25.4.2.1.6, hrSWRunType
#        1.3.6.1.2.1.25.4.2.1.7, hrSWRunStauts
#
# Grupo 5: hrSWRunPerf - NAO ESTA SENDO UTILIZADO 
#        oid, nome do campo, utilizado - descricao
#        1.3.6.1.2.1.25.5.1.1.1, hrSWRunPerfCPU - Porcentagem do uso do processador
#        1.3.6.1.2.1.25.5.1.1.2, hrSWRunPerfMem - Memoria usada em Kbytes
#
# Grupo 6: ip/ipAddrTable
#        oid, nome do campo, utilizado - descricao
#        1.3.6.1.2.1.4.20.1.1, ipAdEntAddr - Ips
#        1.3.6.1.2.1.4.20.1.2, ipAdEntifIndex - ID da interface
#        1.3.6.1.2.1.4.20.1.3, ipAdEntNetMask - Submascara de rede
#        1.3.6.1.2.1.4.20.1.4, ipAdEntBcastAddr, nao
#        1.3.6.1.2.1.4.20.1.5, ipAdEntReasmMaxSize, nao

import argparse
from pysnmp.entity.rfc3413.oneliner import cmdgen
from dbmanager import reg_group1_db, reg_group2_db, reg_group3_db, reg_group6_db
from datetime import datetime
import re
from settings import DB, INSTALL_PATH
from logs import logsnmpget

parser = argparse.ArgumentParser(description='Recolher informacoes de um Host passado por argumento')
parser.add_argument('ID', help='ID do Host', type = int)
parser.add_argument('HOST', help='IP do Host')
args = parser.parse_args()

HOST = args.HOST
ID = args.ID

def time_conversion(timestr):
    ''' Converte o tempo em segundos para horas e minutos '''
    try:
        timesec = int(timestr)
        timemin = (timesec / 100) / 60
        m = timemin % 60.0
        h = (timemin - m) / 60
        return '{0} hora(s) e {1} minuto(s)'.format(int(h), int(m))
    except:
        return '0'

def group1():
    resultl = []
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((HOST, 161)),
        '1.3.6.1.2.1.1.1',
        '1.3.6.1.2.1.1.3',
        '1.3.6.1.2.1.1.4',
        '1.3.6.1.2.1.1.6',
        '1.3.6.1.2.1.1.7',
    )
    if errorIndication:
        print(errorIndication)
        logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorIndication))
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
            logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorStatus.prettyPrint()))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    if str(name) == '1.3.6.1.2.1.1.1.0':
                        resultl.append(val)
                    if str(name) == '1.3.6.1.2.1.1.3.0':
                        resultl.append(time_conversion(val))
                    if str(name) == '1.3.6.1.2.1.1.4.0':
                        resultl.append(val)
                    if str(name) == '1.3.6.1.2.1.1.6.0':
                        resultl.append(val)
                    if str(name) == '1.3.6.1.2.1.1.7.0':
                        resultl.append(val)
        if len(resultl) == 5:
            resultl.insert(0, HOST)
            resultl.insert(0, ID)
            resultl.append(datetime.today().strftime('%d/%m/%Y'))
            resultl.append(datetime.today().strftime('%H:%M:%S'))
            reg_group1_db('{0}{1}'.format(INSTALL_PATH, DB), resultl)
            logsnmpget('SUCESSO: Dados do Grupo 1 do ID {0} e Host {1} coletados.'.format(ID, HOST))

def group2():
    resultl = []
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((HOST, 161)),
        '1.3.6.1.2.1.25.1.5',
        '1.3.6.1.2.1.25.1.6',
    )
    if errorIndication:
        print(errorIndication)
        logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorIndication))
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
            logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorStatus.prettyPrint()))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    if str(name) == '1.3.6.1.2.1.25.1.5.0':
                        resultl.append(val)
                    if str(name) == '1.3.6.1.2.1.25.1.6.0':
                        resultl.append(val)
            if len(resultl) == 2:
                resultl.insert(0, HOST)
                resultl.insert(0, ID)
                resultl.append(datetime.today().strftime('%d/%m/%Y'))
                resultl.append(datetime.today().strftime('%H:%M:%S'))
                reg_group2_db('{0}{1}'.format(INSTALL_PATH, DB), resultl)
                logsnmpget('SUCESSO: Dados do Grupo 1 do ID {0} e Host {1} coletados.'.format(ID, HOST))

def group3id():
    lmount = []
    mem = ''
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((HOST, 161)),
       '1.3.6.1.2.1.25.2'
    )
    if errorIndication:
        print(errorIndication)
        logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorIndication))
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
            logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorStatus.prettyPrint()))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    if str(name) == '1.3.6.1.2.1.25.2.2.0':
                       mem = str(int(val) / 1024)
                    if str(name).find('1.3.6.1.2.1.25.2.3.1.1.') >= 0:
                       lmount.append(str(name).split('.')[-1])
    return varBindTable, lmount, mem

def group3(varBindTable, lmount, mem):
    resultl = []
    hrStorageDescr = hrStorageSize = hrStorageUsed = ''
    for i in lmount:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if str(name) == '1.3.6.1.2.1.25.2.3.1.3.{0}'.format(i):
                    hrStorageDescr = '|'.join([hrStorageDescr, str(val)])
                if str(name) == '1.3.6.1.2.1.25.2.3.1.5.{0}'.format(i):
                    hrStorageSize = '|'.join([hrStorageSize, str(int(val) * 0.004)])
                if str(name) == '1.3.6.1.2.1.25.2.3.1.6.{0}'.format(i):
                    hrStorageUsed = '|'.join([hrStorageUsed, str(int(val) * 0.004)])
    resultl.append(ID)
    resultl.append(HOST)
    if mem != '':
        resultl.append(mem)
    resultl.append(hrStorageDescr)
    resultl.append(hrStorageSize)
    resultl.append(hrStorageUsed)        
    resultl.append(datetime.today().strftime('%d/%m/%Y'))
    resultl.append(datetime.today().strftime('%H:%M:%S'))
    if len(resultl) == 8:
        reg_group3_db('{0}{1}'.format(INSTALL_PATH, DB), resultl)
        logsnmpget('SUCESSO: Dados do Grupo 1 do ID {0} e Host {1} coletados.'.format(ID, HOST))

def group4id():
    lmount = []
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((HOST, 161)),
        '1.3.6.1.2.1.25.4'
    )
    if errorIndication:
        print(errorIndication)
        logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorIndication))
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
            logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorStatus.prettyPrint()))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    if str(name).find('1.3.6.1.2.1.25.4.2.1.1.') >= 0:
                        lmount.append(str(name).split('.')[-1])
    return varBindTable, lmount

def group4(varBindTable, lmount):
    for i in lmount:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if str(name) == '1.3.6.1.2.1.25.4.2.1.1.{0}'.format(i):
                    arq.writelines('hrSWRunIndex - ID do Processo: {0}\n'.format(val))
                if str(name) == '1.3.6.1.2.1.25.4.2.1.2.{0}'.format(i):
                    arq.writelines('hrSWRunName - Processo: {0}\n'.format(val))
                if str(name) == '1.3.6.1.2.1.25.4.2.1.4.{0}'.format(i):
                    arq.writelines('hrSWRunPath - Path: {0}\n'.format(val))
                if str(name) == '1.3.6.1.2.1.25.4.2.1.5.{0}'.format(i):
                    arq.writelines('hrSWRunParameters - Parametros: {0}\n'.format(val))

def group5id():
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((HOST, 161)),
       '1.3.6.1.2.1.25.5'
    )
    if errorIndication:
        print(errorIndication)
        logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorIndication))
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
            logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorStatus.prettyPrint()))
        else:
            pass
    return varBindTable

def group5(varBindTable, lmount):
    cpuperc = 0
    for i in lmount:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if str(name) == '1.3.6.1.2.1.25.5.1.1.1.{0}'.format(i):
                    cpuperc += int(val)             
    for i in lmount:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if str(name) == '1.3.6.1.2.1.25.5.1.1.1.{0}'.format(i):
                    arq.writelines('hrSWRunPerfCPU - Uso de CPU: {0}%\n'.format(str(round((float(val) * 100) / cpuperc, 2))))
                if str(name) == '1.3.6.1.2.1.25.5.1.1.2.{0}'.format(i):
                    arq.writelines('hrSWRunPerfMem - Uso de Memoria: {0}Kb\n'.format(val))

def group6id():
    lmount = []
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((HOST, 161)),
        '1.3.6.1.2.1.4.20'
    )
    if errorIndication:
        print(errorIndication)
        logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorIndication))
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
            logsnmpget('FAIL: ID {0} - HOST {1} - {0}'.format(ID, HOST, errorStatus.prettyPrint()))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    if str(name).find('1.3.6.1.2.1.4.20.1.1.') >= 0:
                        lmount.append(re.search(r'1\.3\.6\.1\.2\.1\.4\.20\.1\.1\.(.*)', str(name)).group(1))
    return varBindTable, lmount

def group6(varBindTable, lmount):
    resultl = []
    ipAdEntAddr = ipAdEntifIndex = ipAdEndNetMask = ''
    for i in lmount:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if str(name) == '1.3.6.1.2.1.4.20.1.1.{0}'.format(i):
                    ipAdEntAddr = '|'.join([ipAdEntAddr, val.prettyPrint()])
                if str(name) == '1.3.6.1.2.1.4.20.1.2.{0}'.format(i):
                    ipAdEntifIndex = '|'.join([ipAdEntifIndex, str(val)])
                if str(name) == '1.3.6.1.2.1.4.20.1.3.{0}'.format(i):
                    ipAdEndNetMask = '|'.join([ipAdEndNetMask, val.prettyPrint()])
    resultl.append(ID)
    resultl.append(HOST)
    if ipAdEntAddr != '':
        resultl.append(ipAdEntAddr)
    resultl.append(ipAdEntifIndex)
    resultl.append(ipAdEndNetMask)
    resultl.append(datetime.today().strftime('%d/%m/%Y'))
    resultl.append(datetime.today().strftime('%H:%M:%S'))
    if len(resultl) == 7:
        reg_group6_db('{0}{1}'.format(INSTALL_PATH, DB), resultl)
        logsnmpget('SUCESSO: Dados do Grupo 1 do ID {0} e Host {1} coletados.'.format(ID, HOST))

if __name__ == '__main__':
    group1()                                # grupo1
    group2()                                # grupo2
    varBindTable, lmount, mem = group3id()  # grupo3
    group3(varBindTable, lmount, mem)       # grupo3
    del varBindTable, lmount
    
#    Removido, possui muita informacao para ser tratada
#    Fica como melhoria inserir as informacoes de processos
#    varBindTable, lmount = group4id()       # grupo4
#    group4(varBindTable, lmount)            # grupo4
#    del varBindTable
#    varBindTable = group5id()               # grupo5        
#    group5(varBindTable, lmount)            # grupo5
#    del varBindTable, lmount

    varBindTable, lmount = group6id()       # grupo6
    group6(varBindTable, lmount)            # grupo6
