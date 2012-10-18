#!/usr/bin/env python
#coding: utf-8

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# dbquery gera os relatorios em formato TXT e CSV.
# Se o dbquery for chamado diretamente, ele gera a lista dos Hosts cadastrados no Banco de Dados e suas informacoes basicas e exibe em um arquivo de texto.

import subprocess
from logs import logdbquery
import dbmanager
from settings import DB, TEMP_FOLDER, INSTALL_PATH

def hostlist_txt(idx=''):
    ''' Gera a lista de Hosts e formata o resultado para ser inserido em um arquivo de texto.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
    
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            
            # Cria o arquivo do relatorio no formato TXT
            with open('{0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER), 'w') as arq:
            
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Com cada host e gerada uma lista dos dados
                    lg1 = dbmanager.query_group1_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Escreve no arquivo
                    arq.writelines('ID: {0}\nIP: {1}\nHOST: {2}\nDESCRICAO: {3}\nLIGADO: {4}\nCONTATO: {5}\nLOCAL: {6}\nNUM. SERVICOS: {7}\nDATA: {8}\nHORA: {9}\n\n'.format(i[0], i[1], i[2], lg1[0], lg1[1], lg1[2], lg1[3], lg1[4], lg1[5], lg1[6]))
            
            # Abre o gedit com o relatorio criado
            subprocess.call(['gedit', '{0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        except:
            # Insere falha no log
            logdbquery('FALHA ao criar o arquivo {0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver nenhum host para gerar o relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        print 'Nenhum Host encontrado.'
        
def hostlist_csv(dest, nome, idx=''):
    ''' Gera a lista de Hosts e exibe o resultado em arquivo separado por virgulas (CSV).
        dest contem o diretorio fornecido para salvar o relatorio. Tem que fornecer o caminho absoluto.
        nome contem o nome do arquivo que sera criado.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
    
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato CSV
            with open('{0}{1}.csv'.format(dest, nome), 'w') as arq:
                
                # Escreve no arquivo os titulos das colunas
                arq.writelines('"ID";"IP";"HOST";"DESCRICAO";"LIGADO";"CONTATO";"LOCAL";"NUM. SERVICOS";"DATA";"HORA"\n')
                
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Com cada host e gerada uma lista dos dados
                    lg1 = dbmanager.query_group1_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Escreve no arquivo
                    arq.writelines('"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";"{9}"\n'.format(i[0], i[1], i[2], lg1[0], lg1[1], lg1[2], lg1[3], lg1[4], lg1[5], lg1[6]))
            
            # Chama o gedit para exibir o arquivo
            subprocess.call(['gedit', '{0}{1}.csv'.format(dest, nome)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}.csv'.format(dest, nome))
        except:
        
            # Insere falha no log
            logdbquery('FALHA ao criar o arquivo {0}{1}.csv'.format(dest, nome))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar o relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}.csv'.format(dest, nome))
        print 'Nenhum Host encontrado.'

def sysusers_process_txt(idx=''):
    ''' Gera a lista da quantidade de usuarios logados e quantidade de processos do Host ordenado por data e hora e exibe o resultado em arquivo de texto.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato TXT
            with open('{0}{1}sysusers_process.txt'.format(INSTALL_PATH, TEMP_FOLDER), 'w') as arq:
                
                # Escreve no arquivo os titulos das colunas
                arq.writelines('ID\t\tIP\t\tHOST\t\tUSUARIO LOGADOS\t\tPROCESSOS\t\tDATA\t\tHORA\n')
                
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Com cada host e gerada uma lista dos dados
                    lg2 = dbmanager.query_group2_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Para cada dados da lista, escreve no arquivo
                    for j in lg2:
                        arq.writelines('{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\t\t{6}\n'.format(i[0], i[1], i[2], j[2], j[3], j[4], j[5]))
            
            # Chama o gedit para exibir o arquivo
            subprocess.call(['gedit', '{0}{1}sysusers_process.txt'.format(INSTALL_PATH, TEMP_FOLDER)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}sysusers_process.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        except:
            # Insere falha no log
            logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}sysusers_process.txt'.format(INSTALL_PATH, TEMP_FOLDER))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        print 'Nenhum Host encontrado.'

def sysusers_process_csv(dest, nome, idx=''):
    ''' Gera a lista da quantidade de usuarios logados e quantidade de processos do Host ordenado por data e hora e exibe o resultado em arquivo separado por virgulas (CSV).
        dest contem o diretorio fornecido para salvar o relatorio. Tem que fornecer o caminho absoluto.
        nome contem o nome do arquivo que sera criado.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
        
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato CSV
            with open('{0}{1}.csv'.format(dest, nome), 'w') as arq:
            
                # Escreve no arquivo os titulos das colunas
                arq.writelines('"ID";"IP";"HOST";"USUARIO LOGADOS";"PROCESSOS";"DATA";"HORA"\n')
                
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Com cada host e gerada uma lista dos dados
                    lg2 = dbmanager.query_group2_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Para cada dados da lista, escreve no arquivo
                    for j in lg2:
                        arq.writelines('"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}"\n'.format(i[0], i[1], i[2], j[2], j[3], j[4], j[5]))
            
            # Chama o gedit para exibir o relatorio
            subprocess.call(['gedit', '{0}{1}.csv'.format(dest, nome)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}.csv'.format(dest, nome))
        except:
        
            # Insere falha no log
            logdbquery('FALHA ao criar o arquivo {0}{1}.csv'.format(dest, nome))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar o relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}.csv'.format(dest, nome))
        print 'Nenhum Host encontrado.'

def memory_storage_txt(idx=''):
    ''' Gera a lista com a Memoria e unidades de armazenamento cadastrados no Host com seu tamanho total e usado e exibe o resultado em arquivo de texto.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
    
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato TXT
            with open ('{0}{1}memory_storage.txt'.format(INSTALL_PATH, TEMP_FOLDER), 'w') as arq:
            
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                
                    # Passa host a host inserindo os dados no arquivo.
                    lg3 = dbmanager.query_group3_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Para cada dados da lista, escreve no arquivo
                    for j in lg3:
                        # Insere as colunas no arquivo
                        arq.writelines('DATA: {0}\t\tHORA: {1}\nMEMORIA: {2}MB\nID\t\tIP\t\tUNIDADE\t\tTAMANHO TOTAL\t\tTAMANHO USADO\n'.format(j[6], j[7], j[2]))
                        
                        # Remove o separador e separa cada valor para uma variavel para ser escrito no arquivo
                        hrSD = j[3].split('|')
                        hrSS = j[4].split('|')
                        hrSU = j[5].split('|')
                        
                        # Escreve o dados no arquivo
                        for a in xrange(1, len(hrSD) - 1):
                            arq.writelines('{0}\t\t{1}\t\t{2}\t\t{3}MB\t\t{4}MB\n'.format(i[0], i[1], hrSD[a], hrSS[a], hrSU[a]))
                        arq.writelines('\n')
            
            # Chama o gedit para exibir o relatorio
            subprocess.call(['gedit', '{0}{1}memory_storage.txt'.format(INSTALL_PATH, TEMP_FOLDER)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}memory_storage.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        except:
            # Insere falha no log
            logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}sysusers_process.txt'.format(INSTALL_PATH, TEMP_FOLDER))
            print 'Falha ao criar arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar o relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        print 'Nenhum Host encontrado.'

def memory_storage_csv(dest, nome, idx=''):
    ''' Gera a lista com a Memoria e unidades de armazenamento cadastrados no Host com seu tamanho total e usado e exibe o resultado em arquivo separado por virgulas (CSV).
        dest contem o diretorio fornecido para salvar o relatorio. Tem que fornecer o caminho absoluto.
        nome contem o nome do arquivo que sera criado.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.        
        '''
    
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato CSV
            with open ('{0}{1}.csv'.format(dest, nome), 'w') as arq:
                
                # Insere as colunas no arquivo
                arq.writelines('"DATA";"HORA";"MEMORIA";"ID";"IP";"UNIDADE";"TAMANHO TOTAL";"TAMANHO USADO"\n')
                
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Passa host a host inserindo os dados no arquivo.
                    lg3 = dbmanager.query_group3_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Para cada dados da lista, escreve no arquivo
                    for j in lg3:
                        # Remove o separador e separa cada valor para uma variavel para ser escrito no arquivo
                        hrSD = j[3].split('|')
                        hrSS = j[4].split('|')
                        hrSU = j[5].split('|')
                        
                        # Escreve no arquivo
                        for a in xrange(1, len(hrSD) - 1):
                            arq.writelines('"{0}";"{1}";"{2}MB";"{3}";"{4}";"{5}";"{6}MB";"{7}MB"\n'.format(j[6], j[7], j[2], i[0], i[1], hrSD[a], hrSS[a], hrSU[a]))
            
            # Chama o gedit para exibir o arquivo
            subprocess.call(['gedit', '{0}{1}.csv'.format(dest, nome)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}.csv'.format(dest, nome))
        except:
            # Insere falha no log
            logdbquery('FALHA ao criar o arquivo {0}{1}.csv'.format(dest, nome))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}.csv'.format(dest, nome))
        print 'Nenhum Host encontrado.'

def ifs_txt(idx=''):
    ''' Gera a lista das interfaces de rede dos Hosts cadastrados e exibe o resultado em arquivo de texto.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
        
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato TXT
            with open('{0}{1}ifs.txt'.format(INSTALL_PATH, TEMP_FOLDER), 'w') as arq:
            
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Passa host a host inserindo os dados no arquivo.
                    lg6 = dbmanager.query_group6_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Para cada dados da lista, escreve no arquivo
                    for j in lg6:
                        # Remove o separador e separa cada valor para uma variavel para ser escrito no arquivo
                        ipAEA = j[2].split('|')
                        ipAEI = j[3].split('|')
                        ipAENM = j[4].split('|')
                        
                        # Escreve no arquivo
                        for a in xrange(1, len(ipAEA) - 1):
                            arq.writelines('ID: {0}\tHOST: {1}\tDATA: {2}\tHORA: {3}\nID da Interface: {4}\nIP: {5}\nMascara: {6}\n\n'.format(i[0], i[1], j[5], j[6], ipAEI[a], ipAEA[a], ipAENM[a]))
            
            # Chama o gedit para exibir o relatorio
            subprocess.call(['gedit', '{0}{1}ifs.txt'.format(INSTALL_PATH, TEMP_FOLDER)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}ifs.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        except:
            # Insere falha no log
            logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}sysusers_process.txt'.format(INSTALL_PATH, TEMP_FOLDER))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}hostslists.txt'.format(INSTALL_PATH, TEMP_FOLDER))
        print 'Nenhum Host encontrado.'

def ifs_csv(dest, nome, idx=''):
    ''' Gera a lista das interfaces de rede dos Hosts cadastrados e exibe o resultado em arquivo separado por virgulas (CSV).
        dest contem o diretorio fornecido para salvar o relatorio. Tem que fornecer o caminho absoluto.
        nome contem o nome do arquivo que sera criado.
        idx contem o indice do host, caso nao for fornecido sera retornado todos os hosts cadastrados.
        '''
    
    # Gera uma lista de tuplas com o(s) host(s) desejado(s).
    l = dbmanager.query_hosts_db('{0}{1}'.format(INSTALL_PATH, DB), idx)
    
    # Verifica ha host para o relatorio
    if len(l) > 0:
        try:
            # Cria o arquivo do relatorio no formato CSV
            with open('{0}{1}.csv'.format(dest, nome), 'w') as arq:
            
                # Insere as colunas no arquivo
                arq.writelines('"ID";"HOST";"DATA";"HORA";"ID INTERFACE";"IP";"MASCARA"\n')
                
                # Passa host a host inserindo os dados no arquivo.
                for i in l:
                    # Passa host a host inserindo os dados no arquivo.
                    lg6 = dbmanager.query_group6_db('{0}{1}'.format(INSTALL_PATH, DB), i[0])
                    
                    # Para cada dados da lista, escreve no arquivo
                    for j in lg6:
                        # Remove o separador e separa cada valor para uma variavel para ser escrito no arquivo
                        ipAEA = j[2].split('|')
                        ipAEI = j[3].split('|')
                        ipAENM = j[4].split('|')
                        
                        # Escreve no arquivo
                        for a in xrange(1, len(ipAEA) - 1):
                            arq.writelines('"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}"\n'.format(i[0], i[1], j[5], j[6], ipAEI[a], ipAEA[a], ipAENM[a]))
            
            # Chama o gedit para exibir o relatorio
            subprocess.call(['gedit', '{0}{1}.csv'.format(dest, nome)])
            
            # Insere sucesso no log
            logdbquery('SUCESSO ao criar o arquivo {0}{1}.csv'.format(dest, nome))
        except:
            # Insere falha no log
            logdbquery('FALHA ao criar o arquivo {0}{1}.csv'.format(dest, nome))
            print 'Falha ao criar o arquivo.'
    else:
        # Insere falha no log se nao houver hosts para gerar relatorio
        logdbquery('FALHA, Nenhum Host encontrado ao gerar {0}{1}.csv'.format(dest, nome))
        print 'Nenhum Host encontrado.'

if __name__ == '__main__':
    hostlist_txt()
