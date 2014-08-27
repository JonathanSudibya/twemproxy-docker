import os
import ConfigParser as configparser
import boto
import yaml



def write_nutcracker_config(backends):
    with open('/etc/nutcracker/nutcracker.yaml', 'w') as nutcracker:
        nutcracker.write(yaml.dump({
            'gamma':{
                'listen': '0.0.0.0:22121',
                'hash': 'fnv1a_64',
                'hash_tag': 'P:',
                'distribution': 'ketama',
                'timeout': 250,
                'auto_eject_hosts': False,
                'servers': backends
            }
        }, default_flow_style=False))

def write_supervisor_config(memcached_backends=[]):
    config = configparser.ConfigParser()
    config.add_section('supervisord')
    config.set('supervisord', 'nodaemon', True)
    config.add_section('program:nutcracker')
    config.set('program:nutcracker', 'command', '/usr/local/bin/nutcracker -c /etc/nutcracker/nutcracker.yaml -o /var/log/nutcracker/nutcracker.log -s 22222 -v 6')

    index = 0
    for memcache in memcached_backends:
        index = index + 1
        section_name = 'program:memcached_{}'.format(index)
        config.add_section(section_name)
        config.set(section_name, 'command', '/usr/bin/memcached -p {}'.format(memcache))
        config.set(section_name, 'user', 'memcache')

    with open('/etc/supervisor/conf.d/supervisord.conf', 'w') as supervisor:
        config.write(supervisor)

def get_aws_ip(instance, use_public_ip):
    if use_public_ip:
        return instance.ip_address
    else:
        return instance.private_ip_address

def generate_config_files():
    tag_name  = os.environ.get('AWS_TAG_NAME', None)
    tag_value = os.environ.get('AWS_TAG_VALUE', None)
    public_ip = 'true' == os.environ.get('AWS_PUBLIC_IP', 'true').lower()
    region    = os.environ.get('AWS_REGION', 'us-east-1')

    if tag_name and tag_value:
        conn = boto.connect_ec2()
        instances = conn.get_only_instances(filters={'tag:{}'.format(tag_name):tag_value})

        backends = ['{}:11211:1'.format(get_aws_ip(instance, public_ip)) for instance in instances if instance.state == 'running']
        write_nutcracker_config(backends)
        write_supervisor_config()
        

    else:
        write_nutcracker_config(['127.0.0.1:11211:1', '127.0.0.1:11212:1'])
        write_supervisor_config(['11211','11212'])


if __name__ == '__main__':
    generate_config_files()
