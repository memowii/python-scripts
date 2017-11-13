import socket
from argparse import ArgumentParser
from subprocess import run
from subprocess import DEVNULL
from sys import exit
from os.path import realpath
from os.path import expanduser


def handle_input():
    parser = ArgumentParser(description="set up an apache2 virtual host for Ubuntu 14 and 16")

    parser.add_argument('host', help='URL of the host, e.g., test.dev', nargs='?')
    parser.add_argument('user', help='owner-user of the created project directory', nargs='?')
    parser.add_argument('group', nargs='?',
                        help='(optional) owner-group of the created project directory, if absent owner-user will be used')
    parser.add_argument('-r', '--rewrite', action='store_true', help='enable URL rewrites')
    parser.add_argument('-e', '--example-index', action='store_true', help='create an index.php example')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--delete', help='delete a virtual host from /var/www/')

    return parser.parse_args()


def get_ip():
    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]


def create_virtual_host(args):
    host = args.host
    user = args.user
    group = args.group
    exec_script_path = realpath(expanduser(__file__))

    completed_process = run(['mkdir', '/var/www/' + host], stderr=DEVNULL)

    if completed_process.returncode:
        exit("{0} cannot create directory '/var/www/{1}' already exists: enter a different host name".format(
            exec_script_path, host))

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

    run(['a2ensite', host + '.conf'], stdout=DEVNULL)

    run(['service apache2 restart'], shell=True)

    ip = get_ip()

    run(["sed -i '1i{0} {1} # Added by script {2}\n' /etc/hosts".format(ip, host, exec_script_path)], shell=True)

    print('host {} has been created'.format(host))


def delete_host(host):
    run(['rm', '-rf', '/var/www/{}'.format(host)])
    run(['a2dissite', '{}.conf'.format(host)], stdout=DEVNULL)
    run(['rm', '/etc/apache2/sites-available/{}.conf'.format(host)])
    run(['sed', '-i', '/{}/d'.format(host), '/etc/hosts'])
    run(['service', 'apache2', 'restart'])
    print('host {} has been removed'.format(host))


def main():
    args = handle_input()

    if args.delete:
        delete_host(args.delete)
    else:
        create_virtual_host(args)


main()
