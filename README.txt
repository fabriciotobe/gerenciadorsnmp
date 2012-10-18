Programa de gerenciamento de informacoes atraves do protocolo SNMP

AUTOR: Fabricio Kelmer
CONTATO: fabriciotobe@gmail.com
DATA: 16 de Outubro de 2012

Leia a documentacao, e importante! ;)

RESUMO

	O programa utiliza o protocolo SNMP para pegar informacoes em determinado intervalo de tempos de Hosts na rede. Estas informacoes sao armazenadas em um banco de dados utilizando sqlite. As seguintes informacoes sao registradas:
	- IP
	- Nome do Host
	- Descricao
	- Informacoes de contato
	- Tempo na qual o sistema esta ligado
	- Local de registro do sistema
	- Servicos do sistema
	- Numero de usuarios logados
	- Numero de processos do sistema
	- Memoria
	- Unidades de armazenamento
	- Tamanho total das unidades de armazenamento
	- Escao usado das unidades de armazenamento
	- Interfaces de rede


INSTALACAO

	> Gerenciador
	
	Para gerenciar o programa e o banco de dados e necessario utilizar o Linux e seguir os seguintes passos para instalacao.
	1. Configurar o INTALL_PATH no arquivo settings.py
	2. Instalar o pysnmp (pip install pysnmp)
	3. Instalar o snmpd (no Ubuntu: apt-get install snmpd)
	4. Abrir o arquivo snmpd.conf no diretorio de instalacao e alterar syslocation (Local) e syscontact (Contato).
	5. Copiar o arquivo snmpd.conf do diretorio de instalacao para /etc/snmp/snmpd.conf. Fazer backup do original.
	6. Reiniciar o snmpd (service snmpd restart)
	7. Executar no manager.py e executar a opcao 8 - limpar banco de dados
	8. Agendar o coletor na opcao 5 - agendar a coleta de informacoes
	
	> Cliente Linux
	1. Instalar o snmpd
	2. Copiar o arquivo de configuracao snmpd.conf pre configurado do diretorio padrao do Gerenciador para o cliente.
	3. Reiniciar o snmpd
	
	> Cliente Windows XP/2003
	1. Iniciar
	2. Painel de Controle
	3. Adicionar e remover programas
	4. Na lateral esquerda, adicionar/remover componentes do windows
	5. Abrir Ferramentas de gerenciamento e monitoramento
	6. Marcar Simple Network Management Protocol
	7. Clicar Ok e depois Avancar, aguardar e depois concluir
	8. Acessar o gerenciador de servicos (services.msc)
	9. Abrir o servico Servico SNMP
	10. Na guia Agente, adicionar informacoes de contato e local e selecionar todos os servicos
	11. Na guia Intercalacoes, inserir a comunidade public
	12. Na guia Seguranca, adicionar em Nome de comunidades aceitas a comunidade public (somente leitura)
	13. Na guia Seguranca, definir se ira aceita pacotes SNMP de qualquer host ou definir o IP do host gerenciador
	14. Aplicar as configuracoes e reniciar o servico.
	
	> Cliente Windows Vista/7
	1. Iniciar
	2. Painel de Controle
	3. Programas
	4. Ativar ou desativar recursos do Windows
	5. Marcar Protocolo SNMP
	6. Clicar Ok.
	7. Acessar o gerenciador de servicos (services.msc)
	8. Abrir o servico Servico SNMP
	9. Na guia Agente, adicionar informacoes de contato e local e selecionar todos os servicos
	10. Na guia Intercalacoes, inserir a comunidade public
	11. Na guia Seguranca, adicionar em Nome de comunidades aceitas a comunidade public (somente leitura)
	12. Na guia Seguranca, definir se ira aceita pacotes SNMP de qualquer host ou definir o IP do host gerenciador
	13. Aplicar as configuracoes e reniciar o servico.
		

PROGRAMAS

	> collector.py
	  Executa a coleta das informacoes. Quando existe agendamento, este programa e utilizado.
	  Se chamado diretamente, executa a coleta de todos os hosts cadastrados no banco de dados
	> dbmanager.py
	  Gerencia todas os cadastros, modificacoes e consultas no banco de dados.
	  Se chamado diretamente, executa uma consulta em todos os hosts cadastrados
	> dbquery.py
	  Gera os relatorios das informacoes do banco de dados. Existem duas saidas: TXT e CSV
	  Se chamando diretamente, executa o relatorio de hosts cadastrados com informacoes basicas em TXT
	> ipscanner.py
	  Escaneia um determinado range de IPs e exibe uma lista dos que estao online. Verifica tambem se o protocolo SNMP esta ativo nos hosts online.
	  Para chamar diretamente, deve ser passado por parametro ip inicial e ip final.
	> logs.py
	  Grava em arquivos de logs as operacoes dos programas. Nao pode ser chamado diretamente.
	> manager.py
	  Exibe o menu de trabalho principal do programa, atraves deste e possivel manusear quase todas as informacoes.
	  Tambem executa tarefas simples como cadastros manuais de hosts, alteracoes de hosts, exclusao de hosts, agendamento do coletor e backup do banco de dados.
	> settings.py
	  Arquivo de configuracao
	> snmpget.py
	  Programa que recolhe as informacoes dos hosts.
	  Para chamar diretamente, deve ser passado por parametro o ID do host e o IP. Para obter estas informacoes, executar o dbquery.py


SUGESTAO DE MELHORIAS

	Existe a possibilidade de expandir as informacoes obtidas via SNMP. Dentro do programa snmpget estao disponiveis funcoes que pegam processos que estao rodando, consumo de cpu e consumo de memoria. Fica como melhoria do programa, habilitar estas informacoes.
