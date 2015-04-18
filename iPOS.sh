#!/bin/bash
# Instala openBravo POS para Delti
# Leon Ramos et al
# 18/04/2015

#VARIABLES
APT=/usr/bin/apt-get
DEBUG=1

END_USER=vdirectas
END_USER_PASS=vdirectas

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

function update {
  $APT update -y
  $APT install vim openssh-server aptitude git -y
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
  if [ ! -d "${INST_PATH}" ] ; then
    pdebug "Creating installation directory ${INST_PATH}"
    /bin/mkdir -p ${INST_PATH}
  else 
    perror "Installation directory ${INST_PATH} exists, aborting."
  fi

  pdebug "Decompresing ${POS_BIN} to ${INST_PATH}..."
  /usr/bin/unzip ${POS_BIN} -d ${INST_PATH}
  
  pdebug "Decompresing ${POS_LANG} to ${INST_PATH}..."
  /usr/bin/unzip ${POS_LANG} -d ${INST_PATH}
}

#LOGIC
checkRoot
#update
addUser
install

exit 0
