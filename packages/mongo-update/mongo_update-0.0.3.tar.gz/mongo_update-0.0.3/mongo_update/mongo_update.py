# -*- coding:utf-8 -*-
import datetime
import itertools
import multiprocessing
import os
import re
import warnings
import pandas as pd
import pymongo
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings('ignore')


def rename_col(username, password, host, db_name, collection_name, old_name, new_name, port: int = 27017,):
    """ 修改mongodb数据源 某集合的某个字段名 """
    # 连接到MongoDB
    _link = f'mongodb://{username}:{password}@{host}:{port}/'
    client = pymongo.MongoClient(_link)
    db = client[db_name]  # 替换为你的数据库名
    collection = db[collection_name]  # 替换为你的集合名

    # 修改字段名的操作
    rename_operation = {"$rename": {old_name: new_name}}

    # 应用修改到集合中的所有文档
    collection.update_many({}, rename_operation)
    if new_name == '日期':
        collection.create_index([(new_name, -1)], background=True)  # 必须, 创建索引, background 不阻塞


class CreateUser:
    """
    通过python 创建 mongodb 管理员账户
    """
    def __init__(self, username, password, host, port: int = 27017):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None

        self.db_roles = [{'pandas数据源': 'read'}]
        self.user_infos = []  # 现有用户信息
        self.root = False
        self.add_permission = True  # 更新权限时, 默认新增, 设置为False 则减去权限

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    @try_except
    def create_user(self):
        """
        role: read(只读), readAnyDatabase(读取所有), readWriteAnyDatabase(读写所有), userAdminAnyDatabase(用户管理权限)

        """

        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        db = self.client['admin']  # 切换到admin数据库
        users = db.system.users.find()  # 获取所有用户
        for user in users:
            self.user_infos.append({user['user']: user['roles']})

        add_roles = []
        for db_role in self.db_roles:
            for key, value in db_role.items():
                add_roles.append({
                    'role': value,
                    'db': key
                })
        # root_roles = ['root'],  # root 权限用户, 正常情况下不要创建 root
        root_roles = [
                {'role': 'userAdminAnyDatabase', 'db': 'admin'},  # 赋予所有数据库的用户管理权限
                {'role': 'readWriteAnyDatabase', 'db': 'admin'}  # 赋予所有数据库的读写权限
            ]

        user_list = []  # 现有用户列表
        i = 0
        for user_info in self.user_infos:
            for key, value in user_info.items():
                user_list.append(key)
                if self.username == key:
                    print(f'{self.username}: 用户已存在, 权限为: {value}')
                    if self.root:
                        print(f'不支持直接升级管理员权限, 请先删除用户再重新创建root角色, 设置 self.root = True ')
                    if self.add_permission:  # 新增权限
                        roles = value + add_roles
                    else:  # 减去权限
                        roles = [item for item in value if item['db'] != add_roles[0]['db']]
                    db.command('updateUser', self.username, roles=roles)  # 更新权限
                    i += 1
                    break
                if self.root:  # 设置超级管理员
                    db.command(command='createUser', value=self.username, pwd=self.password, roles=root_roles)
                    print(f'管理员创建成功: {self.username}, 权限为: {root_roles}')
                    self.client.close()
                    return
            if i > 0:
                self.client.close()
                return
        admin_user = db.command(command='createUser', value=self.username, pwd=self.password, roles=add_roles)
        if admin_user['ok'] > 0:
            print(f'普通用户创建成功: {self.username}, 权限为: {add_roles}')
        self.client.close()

    def delete_user(self):
        """ 删除指定用户: self.username """
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        db = self.client['admin']  # 切换到admin数据库
        users = db.system.users.find()  # 获取所有用户
        for user in users:
            self.user_infos.append({user['user']: user['roles']})

        user_list = []  # 现有用户列表
        i = 0
        for user_info in self.user_infos:
            for key, value in user_info.items():
                user_list.append(key)
                if self.username == key:
                    db.command("dropUser", self.username)
                    print(f'已删除用户: {self.username}')
                    i += 1
        if i == 0:
            print(f'不存在的用户: {self.username}, 无需执行删除操作')
        self.client.close()


class DownMongo:
    """  pass """
    def __init__(self, save_path, username, password, host, port: int = 27017):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None
        self.dbname = None
        self.collection_name = None
        self.days = 5
        self.start_date = None
        self.end_date = datetime.datetime.now()
        self.save_path = save_path

    def data_to_file(self, file_type, dbname, collection_name):
        """
        将 mongodb 数据保存本地
        dbname: 数据库名
        collections 集合名
        file_type: 保存的文件类型 csv, json, xlsx, xls
        """
        self.client = pymongo.MongoClient(self.link)  # 连接数据库
        self.dbname = dbname
        self.collection_name = collection_name
        _collection = self.client[self.dbname][self.collection_name]  # 连接集合
        print(f'正在下载数据 {self.host} {self.dbname}: {self.collection_name}, 数据区间: 近 {self.days} 天\n...')

        self.start_date = datetime.datetime.now() - datetime.timedelta(days=self.days)
        query = {  # 读取数据库中指定时间区间的数据
            '日期':
                {
                    '$gte': self.start_date,
                    '$lte': self.end_date
                },
        }
        _df = pd.DataFrame((list(_collection.find(query))))  # 将数据转换为 dataframe
        for col in _df.columns.tolist():  # 保存之前尝试转换数据类型
            if '日期' in col:
                _df[col] = _df[col].astype(str).apply(lambda x: ''.join(re.findall(r'(\d{4}-\d{2}-\d{2})', x)))
                _df[col] = pd.to_datetime(_df[col], format='%Y-%m-%d', errors='ignore')  # 转换日期列
            elif '_id' in col:
                # _df['_id'] = _df['_id'].astype(str)  # 将 '_id' 字段转换为字符串，因为它是一个 ObjectId 对象
                _df.drop('_id', axis=1, inplace=True)
            else:
                _df[col] = pd.to_numeric(_df[col], errors='ignore')
        print(f'查询的数据量: {len(_df)}')
        s_date = re.findall(r'(\d{4}-\d{2}-\d{2})', str(_df['日期'].values.min()))[0]
        e_date = re.findall(r'(\d{4}-\d{2}-\d{2})', str(_df['日期'].values.max()))[0]
        if not file_type.startswith('.'):
            file_type = '.' + file_type
        _path = os.path.join(self.save_path, f'{self.dbname}_{self.collection_name}_{s_date}_{e_date}{file_type}')
        if file_type.endswith('json'):
            _df.to_json(_path, orient='records', force_ascii=False)
        elif file_type.endswith('csv'):
            _df.to_csv(_path, encoding='utf-8_sig', index=False, header=True)
        elif file_type.endswith('xlsx') or file_type.endswith('xls'):
            _df.to_excel(_path, index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))  # freeze_ 冻结列索引
        else:
            print(f'{file_type}: 未支持的文件类型')
        print(f'{self.collection_name} 保存路径: {_path}, 数据完成！\n-->> 注意数据库导出的数据没有排重!')
        self.client.close()


class UploadMongo:
    """
    上传更新数据库
    目前有两类, 一类上传原始文件, 一类上传pandas数据源
    单独调用 add2mongo 方法，最后必须手动关闭数据库连接
    """

    def __init__(self, upload_path, username, password, host, port: int = 27017):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.link = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/'
        self.client = None
        self.dbname = None  # 上传到数据库时的数据库名
        self.collection_name = None  # 上传到数据库时的集合名, 这个类实际是以文件夹或者文件名作为集合名
        self.upload_path = upload_path
        self.data_days = 5  # 更新近期的数据, 不宜过大, 主要用于 pandas数据源, 原始文件不设置
        self.start_date = None

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    @try_except
    def upload_file(self, path):
        if '.DS_Store' in path or '.ini' in path or 'desktop' in path or 'baiduyun' in path:
            return
        if not path.endswith('csv') or path.endswith('年.csv'):
            return
        df = pd.read_csv(path, encoding='utf-8_sig', header=0, na_filter=False)
        if '日期' in df.columns.tolist():
            try:
                # 转换日期列
                df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x) if x else pd.to_datetime('2099-01-01'))
                self.start_date = pd.to_datetime(datetime.date.today() - datetime.timedelta(days=self.data_days))
                df = df[df['日期'] >= self.start_date]
                if len(df) == 0:
                    # 有些跨月报表可能空数据, 所以读取近35天
                    df = df[df['日期'] >= pd.to_datetime(datetime.date.today() - datetime.timedelta(35))]
                else:
                    df = df[df['日期'] >= self.start_date]  # 选取大于该时间点的数据
            except Exception as e:
                print(f'{path}: {e}')

        if len(df) == 0:  # 如果依然是空表，则不上传更新
            return
        self.add2mongo(df=df)

    @try_except
    def upload_dir(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if str(self.collection_name) not in name:  # 理论上文件夹名必然在文件名中
                    continue
                new_path = os.path.join(root, name)
                self.upload_file(new_path)

    def upload_pandas(self, select_files: str = None, skip_files: str = '其他数据'):
        """
        上传pandas数据源到数据库
        要检查 dbname, 不检查 collection
        select_files: 仅更新此文件
        skip_files: 跳过文件
        """
        if not self.dbname:
            print(f' {self.host}/{self.port}  未设置 self.dbname ')
            return
        pd_files = os.listdir(self.upload_path)
        for file in pd_files:
            if select_files:
                if select_files not in file:
                    continue
            if skip_files:
                if skip_files in file:
                    continue
            path = os.path.join(self.upload_path, file)
            if os.path.isfile(path):  # path: 单文件
                self.collection_name = f'{os.path.splitext(file)[0]}_f'
                self.upload_file(path=path)
            elif os.path.isdir(path):  # path: 文件夹
                if '其他数据' in path:
                    continue
                self.collection_name = f'{os.path.splitext(file)[0]}'
                self.upload_dir(path=path)

    @staticmethod
    def split_list(lst, _num=None):
        """
        <mongodb> 将列表 _num 等分
        """
        length = len(lst)
        if not _num:
            if length > 20000:
                _num = 30
            elif length > 10000:
                _num = 20
            elif length > 1000:
                _num = 15
            elif length > 200:
                _num = 5
            else:
                _num = 2
        if length % _num == 0:
            # print(length, _num)
            sublist_length = length // _num
            return [lst[i:i + sublist_length] for i in range(0, length, sublist_length)]
        else:
            sublist_length = length // _num
            extra = length % _num
            return [lst[i * sublist_length:i * sublist_length + sublist_length] for i in range(_num)] + \
                [lst[-extra:]]  # 添加剩余文档到列表末尾

    @staticmethod
    def duplicates_list(_datas):
        """
        <mongodb> 对传进来的 _datas 排重，数据量大时将消耗大量系统资源
        """
        if len(_datas) > 100 * 1000:
            print(f'数据量太大，可能大量消耗系统资源，谨慎执行!!! {len(_datas)}')
        _my_list = []
        for _data in _datas:
            if _data in _my_list:
                continue
            else:
                _my_list.append(_data)
        return _my_list

    def add2mongo(self, df, duplicates=None):
        """
        需要检查 self.dbname 和 self.collection_name
        df: 待插入数据, dataframe 格式
        duplicates: 排重功能, 数据量大时，将消耗大量资源，日常任务是数据少，应留空或设为 False, 提高性能
        """
        if not self.dbname or not self.collection_name:
            print(f'{self.host}/{self.port} 未指定 self.dbname/collection: {self.dbname}/{self.collection_name}')
            return
        self.client = pymongo.MongoClient(self.link)
        collections = self.client[self.dbname][self.collection_name]  # 连接数据库
        if '日期' in df.columns.tolist():
            df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
            collections.create_index([('日期', -1)], background=True)  # 必须, 创建索引, background 不阻塞

        datas = df.to_dict('records')  # 待插入的数据, [dict, dict, ....]

        if duplicates:  # 调用多进程排重函数, 日常任务不需要排重，请设置参数为 False
            datas = self.split_list(lst=datas)  # 将数据 n 等分
            results = []
            pool = multiprocessing.Pool()
            for data in datas:  # 遍历等分后的每个数据，使用多进程对其排重
                try:
                    results.append(pool.apply_async(self.duplicates_list, args=(data,)).get())
                except Exception as e:
                    print(e)
            pool.close()
            pool.join()
            results = list(itertools.chain.from_iterable(results))  # 合并同一个 list 中的多个 list
            new_list = self.duplicates_list(results)
        else:
            new_list = datas
        # n 等分后的数据, [[dict, dict, ...], [dict, dict, ...]]
        new_list = self.split_list(new_list, )
        # new_list: map 多线程只能传迭代对象，不能直接传其他参数, 所以将 _collection 封装到 list 内
        # new_list: [[_collection, [dict, dict, ...]], [_collection, [dict, dict, ...]]]
        new_list = [[collections, item] for item in new_list]

        def delete_data(data_list):
            """ data_list: [_collection, [dict, dict, ...]]
                delete_many 接受入参是 dict 文档, 所以需要将 data_list 的第二个参数遍历出来 """
            for my_datas in data_list[1]:
                data_list[0].delete_many(my_datas)

        def insert_data(data_list):  # insert_many 可以直接传入列表，表中包含一堆 dict
            data_list[0].insert_many(data_list[1])

        # 先检测原数据再插入新数据
        _now_p = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        print(f'{_now_p}正在更新mongoDB {self.host}:{self.port} 数据库: {self.dbname}/{self.collection_name}...')
        with ThreadPoolExecutor() as pool:  # 删除重复数据
            pool.map(delete_data, new_list)

        with ThreadPoolExecutor() as pool:  # 插入新数据
            pool.map(insert_data, new_list)

        # self.client.close()  # 必须注释掉，不要在这里关闭


def main():
    pass


if __name__ == '__main__':
    main()


