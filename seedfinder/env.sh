export ACHE_HOME=$(dirname $(which ache))/../lib/ache/
echo "ACHE_HOME : $ACHE_HOME"
export PATH="$ACHE_HOME/bin:$PATH"

python multiple_queries_seedfinder.py


