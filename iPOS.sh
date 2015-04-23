#!/bin/bash
# Instala openBravo POS para Delti
# Leon Ramos et al
# 18/04/2015

#VARIABLES
APT=/usr/bin/apt-get
DEBUG=1

END_USER=vdirectas
END_USER_PASS=vdirectas

MYSQL_ROOT=jittermysql
MYSQL_DB=VDSEMILLA
MYSQL_USR=sistemas
MYSQL_PASS=123qweobp
MYSQL_INIT_DB=VDSEMILLA.sql
MYSQL_TMP=/tmp/iPOS_db.sql.tmp
MS="-e 's/\{MYSQL_DB\}/${MYSQL_DB}/g' -e 's/\{MYSQL_USR\}/${MYSQL_USR}/g' -e 's/\{MYSQL_PASS\}/${MYSQL_PASS}/g' -e 's/\{POS_USR\}/${POS_USR}/g' -e 's/\{POS_PASS\}/${POS_PASS}/g'"
POS_USR=SEMILLA
POS_PASS=SEMILLA
MYSQL_PASS_C=$(java utils/encrypt ${MYSQL_USR} ${MYSQL_PASS})

POS_TMP=/tmp/iPOS_properties.tmp
POS_PROPERTIES=openbravopos.properties
POS="-e 's/\{MYSQL_DB\}/${MYSQL_DB}/g' -e 's/\{MYSQL_USR\}/${MYSQL_USR}/g' -e 's/\{MYSQL_PASS\}/${MYSQL_PASS_C}"

RD="-e 's/\{MYSQL_DB\}/${MYSQL_DB}/g' -e 's/\{MYSQL_USR\}/${MYSQL_USR}/g' -e 's/\{MYSQL_PASS\}/${MYSQL_PASS}"

INST_PATH=/opt/DPOS
POS_BIN=openbravopos_2.30_bin.zip
POS_LANG=openbravopos_2.20_es.zip

#FUNCTIONS
function pdebug {
  if [ "$DEBUG" == "1" ] ; then
    echo "iPOS> $1 " ; 
  fi
}

function perror {
  >&2 echo "ERR> $1 ";
  exit 1
}

function checkRoot {
  if [ "$(/usr/bin/whoami)" != "root" ] ; then
    perror "Not superuser privileges, run with sudo or root user.";
  fi
}

function warning {
  key=1
  while [[ $key =~ ^[^YNn]$  ]] ; do 
    echo
    echo "This script will install OpenBravo POS 2.30"
    echo "on an Ubuntu 14.04TLS 32bit system"
    echo
    echo "WARNING!!! - All previous Data for POS will be erased"
    echo
    read -p "Are you sure you want to continue? (Y/n) " -n 1 -r
    echo
    key=$REPLY
  done
  if [ "$key" != "Y" ] ; then
    pdebug "Exiting..."
    exit 0
  fi
}

function update {
  $APT update -y
  $APT install vim openssh-server aptitude git libmysql-java mysql-server default-jre tcllib mysqltcl -y
}

function addUser {
  ret=false
  /usr/bin/getent passwd $END_USER >/dev/null 2>&1 && ret=true
  
  if $ret; then
    pdebug "User $END_USER already exists, skipping."
  else
    pdebug "Creating ${END_USER} user."
    /usr/sbin/useradd -s /bin/bash -m -p "`/usr/bin/openssl passwd -1 ${END_USER_PASS}`" ${END_USER}
  fi   
}

function install {
  if [ -d "${INST_PATH}" ] ; then
    pdebug "Installation directory ${INST_PATH} exists, erasing."
    rm -Rf ${INST_PATH}
  fi
  pdebug "Creating installation directory ${INST_PATH}"
  /bin/mkdir -p ${INST_PATH}

  pdebug "Decompresing ${POS_BIN} to ${INST_PATH}..."
  /usr/bin/unzip ${POS_BIN} -d ${INST_PATH}
  
  pdebug "Decompresing ${POS_LANG} to ${INST_PATH}..."
  /usr/bin/unzip ${POS_LANG} -d ${INST_PATH}

  pdebug "Changing permissions."
  chmod 755 ${INST_PATH}/start.sh

  pdebug "Installing shortcuts"
  [ -d "/home/${END_USER}/Escritorio" ] && /bin/cp -f shortcuts/POS.desktop /home/${END_USER}/Escritorio 
  [ -d "/home/${END_USER}/Desktop" ] && /bin/cp -f shortcuts/POS.desktop /home/${END_USER}/Desktop 

  pdebug "Installing ReporteDiario.py"
  pdebug "Setting initial data to py script"
  /bin/sed "${RD}" ReporteDiario.py > ReporteDiario.py.1
  
  pdebug "Installing py script"
  /bin/cp -f ReporteDiario.py.1 /bin/ReporteDiario.py
  
  pdebug "Erasing temporal file"
  rm -f ReporteDiario.py.1

  pdebug "Setting permissions to py script"
  chmod 755 /bin/ReporteDiario.py

}

function setupMysql {
   pdebug "Setting initial data to seed file: ${MYSQL_INIT_DB}"
   /bin/sed "${MS}" ${MYSQL_INIT_DB} > ${MYSQL_TMP}.1
   
   pdebug "Creating initial DB: ${MYSQL_DB}"
   /usr/bin/mysql -u root --password=${MYSQL_ROOT} < ${MYSQL_TMP}.1
 
   pdebug "Erasing temporal files"
   rm -f ${MYSQL_TMP}.1 

   pdebug "Setting initial data to ${POS_PROPERTIES}"
   /bin/sed "${POS}" ${POS_PROPERTIES} > ${POS_TMP}.1

   pdebug "Copying ${POS_PROPERTIES} to /home/${END_USER}"
   /bin/cp ${POS_TMP}.1 /home/${END_USER}/${POS_PROPERTIES}
   chown ${END_USER}.${END_USER} /home/${END_USER}/${POS_PROPERTIES}

   pdebug "Erasing temporal files"
   rm -f ${POS_TMP}.1 
}


#LOGIC
checkRoot
warning
update
addUser
install
setupMysql

exit 0
