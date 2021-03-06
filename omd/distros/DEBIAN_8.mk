DISTRO_CODE       = jessie
OS_PACKAGES       =
OS_PACKAGES      += libcap2-bin # needed for setting special file permissions
OS_PACKAGES      += cron # needed for sites cron jobs
OS_PACKAGES      += time # needed for mk-job
OS_PACKAGES      += traceroute # needed for Check_MK parent scan
OS_PACKAGES      += curl
OS_PACKAGES      += dialog
OS_PACKAGES      += dnsutils
OS_PACKAGES      += graphviz
OS_PACKAGES      += apache2
OS_PACKAGES      += libapache2-mod-proxy-html
OS_PACKAGES      += libdbi1
OS_PACKAGES      += libevent-2.0-5
OS_PACKAGES      += libgd3
OS_PACKAGES      += libltdl7
OS_PACKAGES      += libpango1.0-0
OS_PACKAGES      += libperl5.20
OS_PACKAGES      += libreadline6
OS_PACKAGES      += libuuid1
OS_PACKAGES      += binutils # Needed by Check_MK Agent Bakery
OS_PACKAGES      += rpm
OS_PACKAGES      += php5
OS_PACKAGES      += php5-cgi
OS_PACKAGES      += php5-cli
OS_PACKAGES      += php5-gd
OS_PACKAGES      += php5-sqlite
OS_PACKAGES      += php-pear
OS_PACKAGES      += rsync
OS_PACKAGES      += smbclient
OS_PACKAGES      += rpcbind
OS_PACKAGES      += lcab # needed for creating MSI packages
OS_PACKAGES      += unzip
OS_PACKAGES      += xinetd
OS_PACKAGES      += libfreeradius-client2
OS_PACKAGES      += libpcap0.8 # needed for cmc
OS_PACKAGES      += libgsf-1-114 # needed by msitools/Agent Bakery
OS_PACKAGES      += libglib2.0-0 # needed by msitools/Agent Bakery
OS_PACKAGES      += cpio # needed for Agent bakery (solaris pkgs)
OS_PACKAGES      += poppler-utils # needed for preview of PDF in reporting
OS_PACKAGES      += libffi6 # needed for pyOpenSSL and dependant
OS_PACKAGES      += libpq5
USERADD_OPTIONS   =
ADD_USER_TO_GROUP = gpasswd -a %(user)s %(group)s
PACKAGE_INSTALL   = aptitude -y update ; aptitude -y install
ACTIVATE_INITSCRIPT = update-rc.d %s defaults
APACHE_CONF_DIR   = /etc/apache2/conf.d
APACHE_INIT_NAME  = apache2
APACHE_USER       = www-data
APACHE_GROUP      = www-data
APACHE_VERSION    = 2.4.10
APACHE_CTL        = /usr/sbin/apache2ctl
APACHE_MODULE_DIR = /usr/lib/apache2/modules
APACHE_MODULE_DIR_64 = /usr/lib/apache2/modules
HTPASSWD_BIN      = /usr/bin/htpasswd
APACHE_ENMOD      = a2enmod %s
PHP_FCGI_BIN      = /usr/bin/php5-cgi
BECOME_ROOT       = su -c
ARCH              = $(shell dpkg --print-architecture)
MOUNT_OPTIONS     =
INIT_CMD          = /etc/init.d/%(name)s %(action)s
