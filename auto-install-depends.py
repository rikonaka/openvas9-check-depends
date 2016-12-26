#!/usr/bin/env python

import os
import re
import commands

# Notice:
# This script mush run as root
# This tool result should not be the check the main basis
# We assuming that you system is base on x64
# Anthor: East Jay
# Email: xxy1836@gmail.com

# Define some color to show
RED_COLOR = "\033[31m"
GREEN_COLOR = "\033[32m"
YELLOW_COLOR = "\033[33m"
BULE_COLOR = "\033[34m"
PURPLE_COLOR = "\033[35m"
TAIL = "\033[0m"

# Define the apt-get show level
QUIET_LEVEL = 2


def check_version(package_name, want_version):
    # Check the version is current or NOT
    # This is the Python version and the from a my bash shell script

    result = commands.getstatusoutput("aptitude show %s | grep Version | cut -d '-' -f1 | cut -d '+' -f1" % package_name) 
    origin_version = result[1]
    split_version = origin_version.split(':')[-1]
    num_version = re.sub('\.|\:', '', split_version)
    
    num_version_add = int(num_version) * 100
    want_version_add =int(want_version) * 100
    comparison_version(num_version_add, want_version_add, package_name)
    
def comparison_version(num_version, want_version, package_name):
    # Just to make sure the num_version and want_version is same length
    # and comparison it
    
    num_version_length = len(str(num_version))
    want_version_length = len(str(want_version))

    if (num_version_length != want_version_length):
        if (num_version_length > want_version_length):
            num_version= num_version / 10
        else:
            num_version= num_version * 10

        comparison_version(num_version, want_version, package_name)

    else:
        print "%sCheck the %s package%s" % (YELLOW_COLOR, package_name, TAIL)
        if (num_version >= want_version):
            print "%sPackage %s is ok%s" % (GREEN_COLOR, package_name, TAIL)
        else:
            print "%sPackage %s version is too low, recommand version is %d, change it%s" % (RED_COLOR, package_name, want_version, TAIL)
            apt_result = commands.getstatusoutput("apt-get -y --reinstall -q=%d install %s" % (QUIET_LEVEL, package_name))
            return 0

def main():
    
    os.system("apt-get -y -q=%d update" % QUIET_LEVEL)
    
    print "%sInstall the base enviroment%s" % (PURPLE_COLOR, TAIL)
    os.system("apt-get -y -q=%d install gcc g++ vim cmake" % QUIET_LEVEL)

    # Greenbone source code
    print "%sInstall the greenbone enviroment%s" % (PURPLE_COLOR, TAIL)
    os.system("apt-get -y -q=%d install libgnutls-dev libgcrypt-dev libglib2.0-dev libglib2.0-0 libxml2 libxml2-dev libxslt-dev libmicrohttpd-dev libmicrohttpd10 pkg-config xsltproc" % QUIET_LEVEL)
    os.system("apt-get -y -q=%d install gettext doxygen xmltoman python-polib libmicrohttpd-dev libxml2-dev libxslt1-dev" % QUIET_LEVEL)

    check_version("libgnutls-dev", "3215") # 3215 is mean 3.2.15(greenbone/INSTALL gnutls >= 3.2.15)
    check_version("cmake", "280")
    check_version("libglib2.0-dev", "232")
    check_version("libmicrohttpd10", "90")

    # Openvas-clt source code
    print "%sInstall the openvas-cli enviroment%s" %(PURPLE_COLOR, TAIL)
    os.system("apt-get -y -q=%d install clang libclang-dev" % QUIET_LEVEL)

    # Openvas-libraries source code
    print "%sInstall the openvas-libraries enviroment%s" %(PURPLE_COLOR, TAIL)
    os.system("apt-get -y -q=%d install zlib1g zlib1g-dev libpcap-dev libgpgme11 libgpgme11-dev uuid-dev libssh-dev libhiredis-dev libksba-dev sqlfairy python-netsnmp" % QUIET_LEVEL)
    os.system("apt-get -y -q=%d install libfreeradius-client-dev dpkg-dev libgnutls28-dev bison libsnmp-dev libgcrypt20-dev libldap2-dev" % QUIET_LEVEL)
    os.system("apt-get -y -q=%d install libsqlite3-dev" % QUIET_LEVEL)

    check_version("libgpgme11", "112")
    check_version("libgpgme11-dev", "112")
    check_version("libssh-dev", "050")
    check_version("libhiredis-dev", "0101")
    check_version("libksba-dev", "107")
    check_version("libldap2-dev", "2411")
    check_version("libfreeradius-client-dev", "116")

    # Openvas-scanner source code 
    print "%sInstall the openvas-scanner enviroment%s" % (PURPLE_COLOR, TAIL)
    os.system("apt-get -y -q=%d install redis-server" % QUIET_LEVEL)
    check_version("redis-server", "240")

    # Install the openvas-smb source code
    print "%sInstall the openvas-smb source code%s" % (PURPLE_COLOR, TAIL)
    os.system("apt-get install -y -q=%d gcc-mingw-w64 libgnutls28-dev perl-base heimdal-dev libpopt-dev libglib2.0-dev" % QUIET_LEVEL)

    # Install the ospd source code
    print "%sInstall the ospd source code%s" % (PURPLE_COLOR, TAIL)
    os.system("apt-get -y -q=%d install python-setuptools python-paramiko" % QUIET_LEVEL)

    # Install the extra package
    os.system("apt-get -y -q=%d install gnutls-bin" % QUIET_LEVEL)
    search_nmap = os.system("type nmap")
    if search_nmap == 0:
        os.system("apt-get -y -q=%d autoremove nmap" % QUIET_LEVEL)
        if not os.path.isfile("nmap-5.51.tar.bz2"):
            os.system("wget https://nmap.org/dist/nmap-5.51.tar.bz2")
        os.system("bzip2 -cd nmap-5.51.tar.bz2 | tar xvf -")
        os.system("cd nmap-5.51 && ./configure && make && make install")
    else:
        os.system("wget https://nmap.org/dist/nmap-5.51.tar.bz2")
        os.system("bzip2 -cd nmap-5.51.tar.bz2 | tar xvf -")
        os.system("cd nmap-5.51 && ./configure && make && make install")
    os.system("apt-get -y -q=%d install texlive-latex-base rpm nsis texlive-full" % QUIET_LEVEL)
    
    install_redis_or_not = raw_input("Do you want to install and run the redis server by recommanded?[y/n]")
    if install_redis_or_not == 'y|Y':
        redis_server_status = os.system("ps -e | grep redis-server")
        if redis_server_status == 0:
            os.system("apt-get -y -q=%d autoremove redis-server" % QUIET_LEVEL)
        else:
            if not os.path.isfile("redis-3.2.6.tar.gz"):
                os.system("wget http://download.redis.io/releases/redis-3.2.6.tar.gz")
            os.system("tar zxvf redis-3.2.6.tar.gz && cd redis-3.2.6 && make && make test && make install && cp redis.conf /etc/ && sed -i 's/# unixsocket/unixsocket/g' /etc/redis.conf && sed -i 's/unixsocketperm/# unixsocketperm/g' /etc/redis.conf")
            os.system("redis-server /etc/redis.conf &")

if __name__ == "__main__":
    main()
