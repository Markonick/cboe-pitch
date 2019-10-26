# Soem useful commands to run 
find . -name "*.pyc" -exec rm -f {} \;
sudo rm celery/pitch_data.txt
sudo rm -rf migrations
docker exec -it backend flask db init
docker exec -it backend flask db migrate
docker exec -it backend flask db upgrade