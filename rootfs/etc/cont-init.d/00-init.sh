#!/command/with-contenv bash
set -e

CONTAINER_CONFIG_DIR="/etc/headscale"
INIT_DATA_APP_CONFIG="/data"
if [ -z "$(ls -A $CONTAINER_CONFIG_DIR 2>/dev/null)" ]; then
	echo "复制配置文件"
    cp -r $INIT_DATA_APP_CONFIG/etc/headscale /etc/
else
    echo "检测到headscale存在配置文件"
fi