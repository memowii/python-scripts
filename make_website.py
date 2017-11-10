import argparse
import socket

from subprocess import run

parser = argparse.ArgumentParser(description="set up an apache2 virtual host for Ubuntu 14 and 16")
parser.add_argument("host", help="URL of the host, e.g., test.dev")
parser.add_argument("user", help="owner-user of the created project directory")
parser.add_argument("group", nargs='?',
                    help="(optional) owner-group of the created project directory, if absent owner-user will be used")
parser.add_argument("-r", "--rewrite", action="store_true", help="enable URL rewrites")
parser.add_argument("-e", "--example-index", action="store_true", help="create an index.php example")
args = parser.parse_args()

host = args.host
user = args.user
group = args.group

run(['mkdir', '-p', '/var/www/' + host])

create_directory_project_command = 'chown -R {0}:{0} /var/www/{1}'.format(user, host)

if group:
    create_directory_project_command = create_directory_project_command.replace(':' + user, ':' + group)

run([create_directory_project_command], shell=True)

if args.example_index:
    example_index = """
<html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
 <?php echo '<h1>It works!</h1>'; ?>
 </body>
</html>
"""
    run(['echo "' + example_index + '" > /var/www/' + host + '/index.php'], shell=True)

conf_content = """
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

if args.rewrite:
    conf_content = """
<Directory /var/www/{0}>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

{1}
""".format(host, conf_content)

run(['echo "' + conf_content + '" > /etc/apache2/sites-available/' + host + '.conf'], shell=True)

run(['a2ensite', host + '.conf'])

run(['service apache2 restart'], shell=True)

ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
    [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

run(["sed -i '1i{0} {1}\n # Added by script {2}' /etc/hosts".format(ip, host, parser.prog)], shell=True)