# pneumonia_cnn

### Installation in AWS EC2
<pre>
cd /home
git clone https://github.com/samuelkim7/pneumonia_cnn
</pre>

### Run in AWS EC2
<pre>
docker pull samuelmwkim/pneumonia_cnn
docker-compose run sh -c "python manage.py migrate"
docker-compose run sh -c "python manage.py createsuperuser"
docker-compose up
</pre>
