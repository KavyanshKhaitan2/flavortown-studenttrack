echo "###############################"
echo "### Update production build ###"
echo "###############################"
echo
echo "[i] Fetching git updates..."
git pull
echo "[i] Done"
echo
echo "[i] Migrating..."
uv run manage.py migrate
echo "[i] Done"
echo
#echo "[i] Deleting static..."
#rm -r static/
#echo "[i] Done"
echo
echo "[i] Building tailwindcss..."
uv run manage.py tailwind build
echo "[i] Done"
echo
echo "[i] Collecting static..."
uv run manage.py collectstatic --noinput
echo "[i] Done"
echo
echo "Killing gunicorn..."
pkill gunicorn
echo "[i] Done"
echo
echo "######################################"
echo "### All processes complete"
echo "######################################"
echo
echo "It will take up to 5 seconds for the webserver to restart."
echo "If it does not restart within a few seconds, please restart the container and debug the outages."