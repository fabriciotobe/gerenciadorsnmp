## Arquivo de configuracao

# @autor: Fabricio Kelmer
# @contato: fabriciotobe@gmail.com
# @data: 16 de Outubro de 2012

# Porta padrao do protocolo SNMP. Padrao 161
DEFAULT_PORT = 161

# Comunidade utilizada no SNMP. Padrao public
DEFAULT_COMMUNITY = 'public'

# Campo padrao para localizacao de Hosts com SNMP ativo. Padrao sysName. NAO ALTERAR
DEFAULT_FIELD = 'sysName'

# Versao do protocolo SNMP. Padrao SNMPv2-MIB
SNMP_VERSION = 'SNMPv2-MIB'

# Diretorio de instalacao, alterar antes de executar o setup.py. Inserir o caminho absoluto e a ultima barra.
INSTALL_PATH = '/'

# Caminho do banco de dados. Padrao diretorio de instalacao + INTALL_PATH
DB = 'database/snmpdb.sqlite'

# Caminho do diretorio temporario. Padrao diretorio de instalacao + TEMP_FOLDER
TEMP_FOLDER = 'temp/'

# Caminho do diretorio de logs local. Padrao diretorio de instalacao + LOG_FOLDER
LOG_FOLDER = 'logs/'
