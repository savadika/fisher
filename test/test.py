# 测试利用with语句来实现上下文管理器

# 1  flask  app  current_app只有一个，
# 2  在现实环境下，request肯定有多个，那么如果类只有一个，如何保证类里面的代码不被上一个程序修改
# 3  解决这个问题就是用到线程隔离对象，local  localstack
# 4  一般都是讲app以及Request先变成上下文对象，再推入线程隔离对象中进行隔离，来保证数据是独立的

import json

dic = {'name': 'ylf', 'age': 23}
dic2 = '{"name": "ylf", "age": 23}'
print(type(dic))
print('---------------')
print(type(dic2))
print('---------------')
# 字符串转换为字典
print(type(json.loads(dic2)))
# 字典转换为字符串
print(type(json.dumps(dic)))

