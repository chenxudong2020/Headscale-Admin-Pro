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

CONTAINER_DB_DIR="/var/lib/headscale"
DB_FILE="$CONTAINER_DB_DIR/db.sqlite"
if [ ! -f "$DB_FILE" ]; then
	echo "将自动生成数据库文件"
	# 初始化数据库
    cd /app
	python3 -m flask db init
	python3 -m flask db migrate
	python3 -m flask db upgrade
else
    echo "检测到SQLITE已有数据"
fi