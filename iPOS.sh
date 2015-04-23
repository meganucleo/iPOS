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
MS1=s/\{MYSQL_DB\}/${MYSQL_DB}/g
MS2=s/\{MYSQL_USR\}/${MYSQL_USR}/g
MS3=s/\{MYSQL_PASS\}/${MYSQL_PASS}/g
POS_USR=SEMILLA
POS_PASS=SEMILLA
MS4=s/\{POS_USR\}/${POS_USR}/g
MS5=s/\{POS_PASS\}/${POS_PASS}/g

POS_TMP=/tmp/iPOS_properties.tmp
POS_PROPERTIES=openbravopos.properties
POS1=s/\{MYSQL_DB\}/${MYSQL_DB}/g
POS2=s/\{MYSQL_USR\}/${MYSQL_USR}/g

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
  $APT install vim openssh-server aptitude git libmysql-java mysql-server default-jre tcllib -y
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

}

function setupMysql {
   pdebug "Setting initial data to seed file: ${MYSQL_INIT_DB}"
   /bin/sed "${MS1}" ${MYSQL_INIT_DB} > ${MYSQL_TMP}.1
   /bin/sed "${MS2}" ${MYSQL_TMP}.1 > ${MYSQL_TMP}.2
   /bin/sed "${MS3}" ${MYSQL_TMP}.2 > ${MYSQL_TMP}.3
   /bin/sed "${MS4}" ${MYSQL_TMP}.3 > ${MYSQL_TMP}.4
   /bin/sed "${MS5}" ${MYSQL_TMP}.4 > ${MYSQL_TMP}.5
   
   pdebug "Creating initial DB: ${MYSQL_DB}"
   /usr/bin/mysql -u root --password=${MYSQL_ROOT} < ${MYSQL_TMP}.5
 
   pdebug "Erasing temporal files"
   rm -f ${MYSQL_TMP}.1 ${MYSQL_TMP}.2 ${MYSQL_TMP}.3 ${MYSQL_TMP}.4 ${MYSQL_TMP}.5

   pdebug "Setting initial data to ${POS_PROPERTIES}"
   /bin/sed "${POS1}" ${POS_PROPERTIES} > ${POS_TMP}.1
   /bin/sed "${POS2}" ${POS_TMP}.1 > ${POS_TMP}.2

   pdebug "Copying ${POS_PROPERTIES} to /home/${END_USER}"
   cp ${POS_TMP}.2 /home/${END_USER}/${POS_PROPERTIES}
   chown ${END_USER}.${END_USER} /home/${END_USER}/${POS_PROPERTIES}

   pdebug "Erasing temporal files"
   rm -f ${POS_TMP}.1 ${POST_TMP}.2
}

#LOGIC
checkRoot
warning
update
addUser
install
setupMysql

exit 0
