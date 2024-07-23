# Checks the state of the importing.
# Exit 0 if the import is done, else 1

# If there's no matching processlist, then it's done.
sleep 10;  # Sleep is necessary to ensure that the initialization has started.
check="$(mysql -u root -pp@ssw0rd1 -e "SELECT state FROM information_schema.processlist WHERE db='osu'")"
echo "osu.mysql Health Check: $check"
[ -z "$check" ] && exit 0 || exit 1