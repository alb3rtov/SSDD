mkdir -p /tmp/db/registry
icegridregistry --Ice.Config=config/node1.config &

./src/Server.py --Ice.Config=config/Server.config
