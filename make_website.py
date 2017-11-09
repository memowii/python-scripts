import socket

from subprocess import run

host = 'test.dev'
user = 'memowii'

run(['mkdir', '-p', '/var/www/' + host])

run(['chown', '-R', user + ':' + user, '/var/www/' + host])

conf_content = """
<Directory /var/www/{0}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
</Directory>

<VirtualHost *:80>
        ServerAdmin admin@{0}
        ServerName {0}
        ServerAlias www.{0}
        DocumentRoot /var/www/{0}
        ErrorLog ${{APACHE_LOG_DIR}}/error.log
        CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
""".format(host)

run(['echo "' + conf_content + '" > /etc/apache2/sites-available/' + host + '.conf'], shell=True)

run(['a2ensite', host + '.conf'])

run(['service apache2 restart'], shell=True)

ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

run(["sed -i '1i{0} {1}\n # Added by script .py' /etc/hosts".format(ip, host)], shell=True)

# todo list: 1.tomar argumentos del usuario (host, user, rewrite?, index?) 2. poder remove lo que se creo