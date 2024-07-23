import json
import lmdb
import os
import shutil

class Structure:
    def __init__(self, key:str, data:list[tuple[str,object]] | int | float | None | str | list | set | tuple):
        """设置结构

        Args:
            key (str): 主键.
            data (list[tuple[str,object]] | int | float | None | str | list | set | tuple ): 
                内容结构 例:[("a",str),("主键",类型)] 或者 int,float,None,str,list,set,tuple
                
        """        
        self.key = key
        if type(data) == list and len(data) > 0 and type(data[0]) == tuple:
            self.data = {}
            for k, v in data:
                if v == list or v == set:
                    self.data[k] = []
                elif v == int:
                    self.data[k] = 0
                elif v == float:
                    self.data[k] = 0.0
                elif v == bool:
                    self.data[k] = False
                elif v == dict:
                    self.data[k] = {}
                elif v == object or v == None:
                    self.data[k] = None
                else:
                    self.data[k] = ""
        else:
            if data == list or data == set:
                self.data = []
            elif data == int:
                self.data = 0
            elif data == float:
                self.data = 0.0
            elif data == bool:
                self.data = False
            elif data == dict:
                self.data = {}
            elif data == object or data == None:
                self.data = None
            else:
                self.data = ""

    def __str__(self):
        return json.dumps(self.__dict__,ensure_ascii=False,indent=4) 

class ConfigDB():

    # 数据库存储路径
    db_path = os.path.join(os.getcwd(),'database')
    # 配置目录
    db_config_path = os.path.join(os.getcwd(),'config')
    # 数据库打开文件对象集合
    envs = {}
    # 编码
    code = 'utf-8'
    # 内存数据库大小
    size = 256
    # 最多命名数据库数量
    max_dbs = 512
    # 最多读写事务数量
    max_readers = 512
    
    def __init__(self,path:str = None, config_path:str = None,size:int = 256, max_dbs:int = 512,max_readers:int = 512):
        """配置数据库

        Args:
            path (str, optional): 数据库路径,默认当前 "database" 文件夹路径下. Defaults to None.
            config_path (str, optional): 数据库配置路径,默认当前 "config" 文件夹路径下. Defaults to None.
            size (int, optional): 内存数据库大小(以M为单位). Defaults to 256.
            max_dbs (int, optional): 最多命名数据库数量. Defaults to 128.
            max_readers (int, optional): 最多读写事务数量. Defaults to 512.
        """        
        if path:
            self.db_path = path
        if config_path:
            self.db_config_path = config_path

        self.size = size
        self.max_dbs = max_dbs
        self.max_readers = max_readers

        # 创建目录
        self._ensure_folder_exists(self.db_path)
        self._ensure_folder_exists(self.db_config_path)
    
    def _ensure_folder_exists(self,folder_path:str) -> bool:
        """创建文件目录

        Args:
            folder_path (str): 文件路径

        Returns:
            bool: 创建结果
        """        
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            return True
        except Exception:
            return False

    def _validate_json(self, data:dict, schema:dict):
        """检查json数据格式有效性

        Args:
            data (dict): 数据对象.
            schema (dict): 数据格式对象

        Raises:
            ValueError: 缺少字段
            ValueError: 类型错误

        Returns:
            bool: 检查结果
        """    
        for key, expected_type in schema.items():
            # 检查字段是否存在
            if key not in data:
                # raise ValueError(f"缺少字段：{key}")
                return False
            # 检查字段类型是否符合预期
            if not isinstance(data[key], type(expected_type)):
                # raise ValueError(f"字段 '{key}' 类型错误，期望 {type(expected_type)}, 实际 {type(data[key])}")
                return False
        return True    

    def init_db(self, db_name:str = 'db', size:int = None, max_dbs:int = None, max_readers:int = None) -> bool:
        """初始化数据库

        Args:
            db_name (str, optional): 数据库名. Defaults to 'db'.
            size (int, optional): 内存数据库大小(以M为单位). Defaults to 256.
            max_dbs (int, optional): 最多命名数据库数量. Defaults to 128.
            max_readers (int, optional): 最多读写事务数量. Defaults to 512.
        
        Returns:
            bool: 初始化或创建结果.
        """ 
        try:
            if size is None:
                size = self.size
            if max_dbs is None:
                max_dbs = self.max_dbs
            if max_readers is None:
                max_readers = self.max_readers
            if db_name in self.envs: # 如果已经存在则先关闭
                self.env_close(db_name)
            else:
                self.envs[db_name] = {}
            self.envs[db_name]['env'] = lmdb.open(os.path.join(self.db_path,db_name), map_size=1024*1024*size, max_dbs=max_dbs, max_readers=max_readers)
            self.envs[db_name]['size'] = size
            self.envs[db_name]['max_dbs'] = max_dbs
            self.envs[db_name]['max_readers'] = max_readers
            # 创建信息记录
            path = os.path.join(self.db_config_path,db_name) + ".json"
            if not os.path.exists(path):
                with open(path, 'w',encoding="utf-8") as file:
                    file.write(json.dumps({
                        'size':size,
                        'max_dbs':max_dbs,
                        'max_readers':max_readers,
                        'name_db_list':{}
                    }, ensure_ascii=False, indent=4))

            return True
        except Exception:
            return False
    
    def create_name_db(self, db_name:str, name_db:str, dec:str, data_structure:Structure) ->bool:
        """创建命名数据库---(如果不存在则创建命名数据库否则不操作)

        Args:
            db_name (str, optional): 数据库名.
            name_db (str): 命名数据库.
            dec (str): 命名数据库描述.
            data_structure (Structure): 结构体.
        
        Returns:
            bool: 创建结果.
        """
        try:
            # 添加信息记录
            path = os.path.join(self.db_config_path,db_name) + ".json"
            if  os.path.exists(path):
                # 创建命名数据库
                if db_name in self.envs:
                    self.envs[db_name]['env'].open_db(name_db.encode(self.code))
                    f = {}
                    with open(path, 'r',encoding="utf-8") as file:
                        f =  json.loads(file.read())
                    if name_db not in f['name_db_list']:
                        f['name_db_list'][name_db] = {
                                                        'dec':dec,
                                                        'structure':data_structure.__dict__
                                                    }
                        with open(path, 'w',encoding="utf-8") as file:
                            file.write(json.dumps(f, ensure_ascii=False, indent=4))
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    def write(self, db_name:str, name_db:str, key:str , value: int | float | None | str | list | dict) -> bool:
        """添加键值对

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            key (str): 键.
            value (int | float | None | str | list | dict): 值.

        Returns:
            bool: 添加结果.
        """ 
        try:
            # 校验数据格式
            check_result = True
            path = os.path.join(self.db_config_path,db_name) + ".json"
            if  os.path.exists(path):
                f = {}
                with open(path, 'r',encoding="utf-8") as file:
                    f =  json.loads(file.read())
                if name_db not in f['name_db_list']:
                    return False
                else:
                    data = f['name_db_list'][name_db]['structure']['data']
                    if type(value) == dict: # 如果是json格式
                        check_result = self._validate_json(value,data)
                    else:
                        check_result = type(value) == type(data)
            else:
                return False
            
            if not check_result:
                return False
            
            db = self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            with self.envs[db_name]['env'].begin(db=db, write=True) as txn:
                key = key.encode(encoding=self.code)
                if type(value) == dict:
                    try:
                        value = json.dumps(value,ensure_ascii=False).encode(encoding=self.code)
                    except Exception:
                        value = value.encode(encoding=self.code)
                else:
                    value = value.encode(encoding=self.code)
                txn.put(key, value)
            return True
        except Exception as e:
            return False

    def batch_write(self, db_name:str, name_db:str, k_v_list:list[dict[str,str|int|float|dict|None]]) -> bool:
        """批量添加键值对

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.            
            k_v_list (str): 键值对列表.

        Returns:
            tuple: (bool,list) -->(添加结果,添加失败的key及原因)
        """ 
        try:
            # 校验数据格式
            data = ""
            error_key = [] # 数据校验错误的key
            path = os.path.join(self.db_config_path,db_name) + ".json"
            
            if  os.path.exists(path):
                f = {}
                with open(path, 'r',encoding="utf-8") as file:
                    f =  json.loads(file.read())
                if name_db not in f['name_db_list']:
                    return (False,[])
                else:
                    data = f['name_db_list'][name_db]['structure']['data']
            else:
                return (False,[])

            db = self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            with self.envs[db_name]['env'].begin(db=db, write=True) as txn:
                for kv in k_v_list:
                    for k,v in kv.items():
                        try:
                            check_result = True
                            if type(v) == dict: # 如果是json格式
                                check_result = self._validate_json(v,data)
                            else:
                                check_result = type(v) == type(data)
                            if not check_result:
                                error_key.append({"key":k,"cause":"数据校验失败"})

                            key = k.encode(encoding=self.code)
                            if type(v) == dict:
                                try:
                                    value = json.dumps(v,ensure_ascii=False).encode(encoding=self.code)
                                except Exception:
                                    value = v.encode(encoding=self.code)
                            else:
                                value = v.encode(encoding=self.code)
                            txn.put(key, value)
                        except Exception as e:
                            error_key.append({"key":k,"cause":str(e)})
            return (True,error_key)
        except Exception:
            return (False,error_key)

    def read(self, db_name:str, name_db:str, key:str) -> str|dict|bool:
        """获取键值对

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            key (str): 键.

        Returns:
            result: str OR json OR False.
        """
        try:
            db =self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            result = None
            with self.envs[db_name]['env'].begin(db=db) as txn:
                result = txn.get(key.encode(encoding=self.code))
                if result:
                    result = result.decode(encoding=self.code)
            if result is not None and "{" in result:
                try:
                    result = json.loads(result)
                except Exception:
                    pass
            return result
        except Exception:
            return False
    
    def delete(self, db_name:str, name_db:str, key:str) -> bool:
        """删除键值对

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            key (str): 键.

        Returns:
            bool: 删除结果.
        """
        try:
            db =self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            result = None
            with self.envs[db_name]['env'].begin(db=db,write=True) as txn:
                result = txn.delete(key.encode(encoding=self.code))
            return result
        except lmdb.Error as e:
            return False
    
    def updata(self, db_name:str, name_db:str, key:str , value:str | dict) -> bool:
        """更新键值

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            key (str): 键.
            value (str | dict): 值.

        Returns:
            bool: 更新结果.
        """        
        try:
            # 校验数据格式
            check_result = True
            path = os.path.join(self.db_config_path,db_name) + ".json"
            if  os.path.exists(path):
                f = {}
                with open(path, 'r',encoding="utf-8") as file:
                    f =  json.loads(file.read())
                if name_db not in f['name_db_list']:
                    return False
                else:
                    data = f['name_db_list'][name_db]['structure']['data']
                    if type(value) == dict: # 如果是json格式
                        check_result = self._validate_json(value,data)
                    else:
                        check_result = type(value) == type(data)
            else:
                return False
            
            if not check_result:
                return False
            
            db =self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            with self.envs[db_name]['env'].begin(db=db, write=True) as txn:
                key = key.encode(encoding=self.code)
                if type(value) == dict:
                    try:
                        value = json.dumps(value,ensure_ascii=False).encode(encoding=self.code)
                    except Exception:
                        value = value.encode(encoding=self.code)
                else:
                    value = value.encode(encoding=self.code)
                txn.put(key, value, overwrite=True)
            return True
        except lmdb.Error as e:
            return False

    def get(self, db_name:str, name_db:str, keys:list[str]) -> tuple:
        """查找内部键值

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            keys (list[str]): 按层级顺序键.
            value (str | dict): 值.

        Returns:
            result: (结果状态, 层级 or None, 结果).
        """       
        try: 
            key_length = len(keys) 
            if key_length < 1:
                return (None,None,None)
            result =  self.read(db_name,name_db,keys[0])
            if result:
                if type(result) == dict and key_length > 1:
                    for index,key in enumerate(keys[1:]):
                        if key in result:
                            result = result[key]
                        else:
                            return (False,index + 1,key)
                    return (True,key_length,result)
                else:
                    return (True,None,result)
            else:
                return (None,None,None)
        except Exception as e:
            return (False,None,None)
    
    def set(self, db_name:str, name_db:str, keys:list[str] , value:str | dict) -> bool:
        """设置内部键值

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            keys (list[str]): 按层级顺序键.
            value (str | dict): 值.

        Returns:
            bool: 设置结果.
        """        
        try:

            def ensure_dict_keys_exist(json_obj, keys, value):
                """生成嵌套字典

                Args:
                    json_obj (_type_): 字典对象
                    keys (_type_): 键列表
                    value (_type_): 键值
                """                
                current_level = json_obj
                keys_length = len(keys)
                index = 0
                for key in keys:
                    if key not in current_level:
                        if index == keys_length - 1:
                            current_level[key] = value
                        else:
                            current_level[key] = {}
                    else:
                        if type(current_level[key]) != dict:
                            if index == keys_length - 1:
                                current_level[key] = value
                            else:
                                current_level[key] = {}
                        else:
                            if index == keys_length - 1:
                                current_level[key] = value
                    index += 1
                    current_level = current_level[key]

            key_length = len(keys) 
            if key_length < 1:
                return None
            result = self.read(db_name,name_db,keys[0])
            if result:
                if type(result) == dict and key_length > 1:
                    ensure_dict_keys_exist(result, keys[1:], value)
                    return self.updata(db_name, name_db, keys[0], result)
                else:
                    return self.updata(db_name, name_db, keys[0], result)
            else:
                m_key = keys[0]
                v_key = {}
                ensure_dict_keys_exist(v_key, keys[1:], value)
                return self.write(db_name, name_db, m_key, v_key)
        except Exception as e:
            return False

    def remove(self, db_name:str, name_db:str, keys:list[str]) -> bool:
        """移除某个内部键

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            keys (list[str]): 按层级顺序键.

        Returns:
            bool: 移除结果
        """        
        try:
            def remove_last_key_if_exists(dict_obj, keys_sequence):
                current_level = dict_obj
                for key in keys_sequence[:-1]:  # 遍历除了最后一个键的所有键
                    if key in current_level:
                        current_level = current_level[key]
                    else:
                        return  False# 如果某个键不存在，则退出函数
                # 删除最后一个键
                if keys_sequence[-1] in current_level:
                    del current_level[keys_sequence[-1]]
                return  True
            
            result = self.read(db_name, name_db, keys[0])
            if result:
                keys_length = len(keys)
                if type(result) == dict and keys_length > 1:
                    r = remove_last_key_if_exists(result,keys[1:])
                    if r:
                        return self.updata(db_name, name_db, keys[0], result)
                    else:
                        return False
                elif  keys_length == 1:
                    return self.delete(db_name, name_db, keys[0])
                else:
                    return False
            else:
                return False
        except Exception:
            return False

    def env_close(self, db_name:str) -> bool:
        """关闭数据库环境

        Args:
            db_name (str): 数据库名称.

        Returns:
            bool: 关闭结果
        """               
        try:
            if db_name in self.envs and self.envs[db_name]:
                self.envs[db_name]['env'].close()
            return True
        except Exception:
            return False

    def get_limit(self, db_name:str, name_db:str, start:int = 0, limit:int = 100) -> dict:
        """获取指定位置和数量的键值对

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库. 
            start (int, optional): 开始位置. Defaults to 0.
            limit (int, optional): 数量. Defaults to 100.

        Returns:
            json: 结果集
        """        
        try:
            db =self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            result = {}
            with self.envs[db_name]['env'].begin(db=db) as txn:
                # 创建游标
                cursor = txn.cursor()
                # 遍历指定数量的键值对
                count = 0
                end = max(start + limit - 1,0)
                for key, value in cursor:
                    if count >= start and end != 0:
                        value = value.decode(encoding=self.code)
                        if value is not None and "{" in value:
                            try:
                                value = json.loads(value)
                            except Exception:
                                pass
                        result[key.decode(encoding=self.code)] = value
                    if count == end:
                        break
                    count += 1

            return result
        except Exception as e:
            return False

    def get_sum(self, db_name:str, name_db:str) -> int:
        """获取存储键值对总数

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.

        Returns:
            int: 总数
        """        
        try:
            db =self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            result = 0
            with self.envs[db_name]['env'].begin(db=db) as txn:
                stats = txn.stat()
                result = stats['entries']
            return result
        except Exception:
            return False

    def matching(self, db_name:str, name_db:str,key:str|int|None|float, start:int = 0, limit:int = 100) ->list:
        """字符匹配(可内部键值的深度匹配)

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库.
            key (str | int | None | float): 需要匹配的字符.
            start (int, optional): 开始位置. Defaults to 0.
            limit (int, optional): 数量. Defaults to 100.           

        Returns:
            list: [匹配结果,匹配总数,key匹配数,content匹配数]
        """        
        try:
            def find_key_or_value_in_json_gen(json_obj, target_value, path=None):
                if path is None:
                    path = []
                
                if isinstance(json_obj, dict):
                    for key, value in json_obj.items():
                        # 检查键是否匹配，包括None的情况
                        if target_value is None and key is None:
                            yield path + [str(key)]

                        elif isinstance(target_value, str) and isinstance(key, str):
                            if key == target_value or target_value in key:
                                yield path + [key]

                        new_path = path + [key]
                        yield from find_key_or_value_in_json_gen(value, target_value, new_path)

                elif isinstance(json_obj, list):
                    for index, value in enumerate(json_obj):
                        new_path = path + [str(index)]
                        yield from find_key_or_value_in_json_gen(value, target_value, new_path)

                # 检查非容器类型的值是否匹配，包括None的情况
                elif target_value is None and json_obj is None:
                    yield path

                elif isinstance(target_value, str) and isinstance(json_obj, str):
                    if json_obj == target_value or target_value in json_obj:
                        yield path

                elif isinstance(target_value, (int, float)) and isinstance(json_obj, (int, float)):
                    if json_obj == target_value:
                        yield path

            db =self.envs[db_name]['env'].open_db(name_db.encode(self.code))
            result = {}
            is_equal_sign = key is None or isinstance(key, (int, float))
            matching_num = 0 # 匹配总数
            key_matching_num = 0 # key匹配数
            content_matching_num = 0 # content匹配数
            if key == "": # 不可使用空字符串来匹配
                return False
            with self.envs[db_name]['env'].begin(db=db) as txn:
                count = 0
                end = max(start + limit - 1,0)
                is_break = False
                cursor = txn.cursor()
                for _key, _value in cursor:
                    _key = _key.decode(encoding=self.code)
                    _value = _value.decode(encoding=self.code)
                    if _value is not None and "{" in _value:
                        try:
                            _value = json.loads(_value)
                        except Exception:
                            pass
                    key_is_key = (key == _key) if is_equal_sign else (key in _key)
                    if key_is_key:
                        matching_num += 1
                        key_matching_num += 1
                        if is_break == False:
                            if count >= start and end != 0:
                                result[_key] = {}
                                result[_key]['value'] = _value # 匹配到的内容
                                result[_key]['type'] = "key" # 匹配类型
                                if type(_key) == str:# 字符型
                                    result[_key]['location'] =  _key.find(key, 0) # 第一次匹配位置
                                else:# 非字符型
                                    result[_key]['location'] =  0 # 第一次匹配位置
                            if count == end:
                                is_break = True
                            count += 1
                    else:
                        if type(_value) == dict:
                            r = list(find_key_or_value_in_json_gen(_value,key))
                            if len(r) > 0:
                                matching_num += 1
                                content_matching_num += 1
                                if is_break == False:
                                    if count >= start:
                                        result[_key] = {}
                                        result[_key]['value']  = _value # 匹配到的内容
                                        result[_key]['type'] = "content" # 匹配类型
                                        result[_key]['location'] = r # 第一次匹配位置
                                    if count == end:
                                        is_break = True
                                    count += 1
            return [result,matching_num,key_matching_num,content_matching_num]
        except Exception as e:
            return False

    def get_name_database_list(self, db_name:str) -> list:
        """获取所有命名数据库名称

        Args:
            db_name (str): 数据库名.

        Returns:
            list: 命名数据库名称列表
        """        
        try:
            db_list = []
            with self.envs[db_name]['env'].begin() as txn:
                db_list = [key.decode(self.code) for key, _ in txn.cursor()]
            return db_list
        except Exception as e:
            return False

    def get_db_name_list(self) -> list:
        """获取所有数据库名称

        Returns:
            list: 数据库名称列表
        
        """
        def list_all_subfolders(directory):
            """
            递归遍历指定目录下的所有子文件夹。

            :param directory: 要遍历的目录路径
            """
            file_name_list = []
            for root, dirs, files in os.walk(directory):
                for dir in dirs:
                    file_name_list.append(dir)
            return file_name_list
        
        try:
            db_list = []
            db_list = list_all_subfolders(self.db_path)
            return db_list
        except Exception as e:
            return False

    def get_db_info(self, db_name:str) -> dict:
        """获取所有命名数据库名称

        Args:
            db_name (str): 数据库名.

        Returns:
            dict: 数据库信息详情
        """        
        try:
            db_info = {}
            info = self.envs[db_name]['env'].info()
            db_info['size'] = info['map_size']
            db_info['max_readers'] = info['max_readers']
            db_info['use_num_readers'] = info['num_readers']
            db_info['max_dbs'] = self.envs[db_name]['max_dbs']
            try:
                use_num_dbs = len(self.get_name_database_list(db_name))
            except Exception:
                use_num_dbs = 0
            db_info['use_num_dbs'] = use_num_dbs
            return db_info
        except Exception as e:
            return False

    def drop_name_db(self, db_name:str, name_db:str) ->bool:
        """删除指定命名数据库

        Args:
            db_name (str): 数据库名.
            name_db (str): 命名数据库名称.

        Returns:
            bool: 删除结果
        """        
        try:
            with self.envs[db_name]['env'].begin(write=True) as txn:
                dbi =self.envs[db_name]['env'].open_db(name_db.encode(self.code), txn=txn)
                txn.drop(dbi)
            # 移除信息记录
            path = os.path.join(self.db_config_path,db_name) + ".json"
            if  os.path.exists(path):
                f = {}
                with open(path, 'r',encoding="utf-8") as file:
                    f =  json.loads(file.read())
                del f['name_db_list'][name_db]
                with open(path, 'w',encoding="utf-8") as file:
                    file.write(json.dumps(f, ensure_ascii=False, indent=4))
            return True
        except Exception:
            return False

    def cleanup(self, db_name:str,db_path:str = None, db_config_path:str = None) -> bool:
        """删除指定数据库

        Args:
            db_name (str): 数据库名称.
            db_path (str, optional): 数据库路径,默认使用初始路径. Defaults to None.
            db_config_path (str, optional): 数据库配置文件路径,默认使用初始路径. Defaults to None.

        Returns:
            bool: 执行结果
        """           
        if db_path is None:
            db_path = self.db_path
        if db_config_path is None:
            db_config_path = self.db_config_path
        db = os.path.join(db_path,db_name)
        db_config = os.path.join(db_config_path,db_name) + ".json"
        if os.path.exists(db):
            try:
                self.env_close(db_name)
                shutil.rmtree(db)
                os.remove(db_config)
                return True
            except OSError as e:
                return False

