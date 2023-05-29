# encoding='utf-8'
import redis
import json

def init_redis(config):
    host = config['host']
    port = config['port']
    password = config['password']
    max_connections = config['max_connections']
    socket_connect_timeout=config['socket_connect_timeout']
    socket_timeout = config['socket_timeout']

    redisPool = redis.ConnectionPool(
        host = host,
        port = port,
        password = password,
        max_connections=max_connections,
        socket_timeout = socket_timeout,
        socket_connect_timeout = socket_connect_timeout,
        decode_responses=True
    )
    my_redis = redis.Redis(connection_pool=redisPool)
    
    return my_redis

def write_redis(k_v,config,name=None):
    my_redis = init_redis(config)
    
    for k,v in k_v.items():
        v = json.dumps(v,ensure_ascii=False)
        k_v[k] = v
    if name is None:
        my_redis.mset(k_v) # mset 设置多个值  e.g. value_dict = {'num': 123, 'str': 456} \n mset(value_dict)
    else:
        my_redis.hmset(name,k_v) # hset 一个name对应一个字典，类似于字典名字。字典中是key->value e.g. r.hset("Dict", "name", "goldsunshine") \n r.hgetall("Dict") \n {'name': 'goldsunshine'}

def read_redis(k=None,config=None,name=None):
    my_redis = init_redis(config=config)
    
    if name is None:
        if k is not None:
            v = my_redis.get(k)
        else:
            v = 'ERROR VALUE'
    else:
        if k is not None:
            v = my_redis.hget(name,k)
        else:
            v = my_redis.hgetall(name)
    return v

def del_key(k=None,config=None,name=None):
    my_redis = init_redis(config)
    if name is None:
        if k is not None:
            my_redis.delete(k)
        else:
            print('name is None and key is None')
    else:
        if k is not None:
            my_redis.hdel(name,k)
        else:
            my_redis.delete(name)
        

if __name__=='__main__':
    config = json.loads(open('../data/config.json','r').read())
    redis_config = config['redis_config']
    print(read_redis(k=None,config=redis_config,name='SUV'))
    #print(read_redis(k='宋PLUS新能源',config=redis_config,name='新能源'))
    #print(read_redis(k='宋PLUS新能源',config=redis_config,name=None))
    #print(read_redis(k=None,config=redis_config,name=None))
    del_key(k=None,config=redis_config,name='SUV')
    print(read_redis(k=None,config=redis_config,name='SUV'))
    print(read_redis(k=None,config=redis_config,name='轿车'))
