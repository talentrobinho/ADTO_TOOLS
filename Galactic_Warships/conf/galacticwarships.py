'''
SALT INFOMATION SETTING
'''
SALT_API="http://10.134.56.83:8000"
SALT_USER="salt_api"
SALT_PASSWORD="salt_api"
SALT_TARGET_TYPE="glob"
SALT_TARGET="Wireless_Union_WWW_TEST_A_0_10_134_39_135"
SALT_AUTH_TYPE="pam"
SALT_FUNCTION="cmd.run"
#SALT_FUNCTION="test.ping"
SALT_CLIENT="local"
#SALT_FUNC_ARG="source /etc/profile;yum clean all && yum -y install"
SALT_FUNC_ARG="yum clean all && yum -y install"
#SALT_FUNC_ARG="uptime"
