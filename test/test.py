from os import environ as env
import unittest
import memcache

print(env)


memcache_address = '{}:{}'.format(env['PROXY_PORT_22121_TCP_ADDR'], env['PROXY_PORT_22121_TCP_PORT'])

class TestMemcache(unittest.TestCase):
    def test_can_get_values(self):
        mc = memcache.Client([memcache_address], debug=1)

        mc.set('some_key', 'Some value')
	
        self.assertEquals('Some value', mc.get('some_key'))
        
        mc.set('some_key', '2222')
	
        self.assertEquals('2222', mc.get('some_key'))


if __name__ == '__main__':
    unittest.main()
