# 服务器端
## 服务器对数据的处理
### 接收客户端请求
- 建立循环查看客户端传来的数据
- 客户端没有数据传输
  - 证明客户端关闭
  - 移除离线用户，关闭客户端
  - 结束循环
- 客户端有数据传输
  - 接收客户端数据并进行下一步解析处理
  - 分析请求类型
  - 根据请求类型调用相应的处理函数
- 对应代码如下：
```python
def request_handler(self, client_soc):
    """处理客户端请求"""
    while True:
        # 接收客户端数据
        recv_data = client_soc.recv_data()
        if not recv_data:
            """没有接收到数据，客户端关闭(限定不能发送空的字符串）"""
            self.remove_offline_user(client_soc)
            client_soc.close()
            break
        
        # 解析数据
        parse_data = self.parse_request_text(recv_data)

        # 分析请求类型，并根据请求类型调用相应的处理函数
        handler_function = self.request_handler_function.get(parse_data['request_id'])
        if handler_function:
            handler_function(client_soc, parse_data)
```
### 解析并处理客户端信息
- 根据分隔符解析数据
  - 提取第一个分隔符前信息为请求类型request_id
  - 注册信息:0000|nickname|password
  - 登陆信息:0001|username|password
  - 聊天信息:0002|username|messages
- 根据request_id判断请求类型并调用相应处理函数
- 对应代码如下：
```python
def parse_request_text(self, text):
    # 解析客户端信息
    print('解析客户端数据:' + text)
    request_list = text.split('|')
    
    # 按照类型解析数据
      request_data = {}
      request_data['request_id'] = request_list[0]

      if request_data['request_id'] == REQUEST_LOGIN:
          # 用户请求登录
          request_data['username'] = request_list[1]
          request_data['password'] = request_list[2]
      elif request_data['request_id'] == REQUEST_CHAT:
          # 用户发来聊天信息
          request_data['username'] = request_list[1]
          request_data['messages'] = request_list[2]
      elif request_data['request_id'] == REQUEST_REGISTER:
          # 用户请求注册
          request_data['nickname'] = request_list[1]
          request_data['password'] = request_list[2]

      return request_data
```
### 请求处理函数
- 创建request_id和方法关联字典
- 将request_id和处理函数注册到字典中
- 相应代码如下：
```python
 def __init__(self):
        self.server_socket = ServerSocket()
        print("waiting for connection")

        # 创建请求的id和方法关联字典
        self.request_handler_function = {}
        self.register(REQUEST_LOGIN, self.request_login_handler)
        self.register(REQUEST_CHAT, self.request_chat_handler)
        self.register(REQUEST_REGISTER, self.request_register_handler)

        # 创建保存当前登陆用户的字典
        self.clients = {}

    def register(self, request_id, handler_function):
        # 注册消息类型和处理函数到字典里
        self.request_handler_function[request_id] = handler_function
```
- 具体的请求处理函数
- 处理注册功能
  - 将用户信息写入数据库
  - 将用户名信息返回到客户端
  - 相应代码如下：
  ```python
      def request_register_handler(self, client_soc, request_data):
        """处理注册功能"""
        print('收到注册请求~~准备处理~~')
        # 返回昵称及密码
        nickname = request_data['nickname']
        password = request_data['password']

        # 写入数据库
        db = DB()
        ret, username = db.register(nickname, password)
        db.close_db_connection()

        # 拼接返回给客户端的消息
        response_text = ResponseProtocol.response_register_request(ret, username)

        # 把消息发送给客户端
        client_soc.send_data(response_text)
  ```
- 处理登陆功能
  - 获取用户账号密码
  - 检察用户是否可以登陆
  - 保存已登录用户信息到数据库中
  - 向用户发送其用户名及昵称
  - 相应代码如下：
  ```python
      def request_login_handler(self, client_soc, request_data):
        """处理登陆功能"""
        print('收到登陆请求~~准备处理~~')
        # 获取账号密码
        username = request_data['username']
        password = request_data['password']

        # 检查是否能够登陆
        ret, nickname, username = self.check_user_login(username, password)

        # 登陆成功需要保存当前用户
        if ret == '1':
            self.clients[username] = {'sock': client_soc, 'nickname': nickname}

        # 拼接返回给客户端的消息
        response_text = ResponseProtocol.response_login_result(ret, nickname, username)

        # 把消息发送给客户端
        client_soc.send_data(response_text)

    def check_user_login(self, username, password):
        """
        检查用户是否登录成功，并返回检查结果
        0：失败
        1：成功
        返回昵称，用户账户
        """
        db = DB()
        ret, nickname, real_username = db.check_log_in(username, password)
        db.close_db_connection()
        return ret, nickname, real_username
  ```
- 处理聊天功能
  - 获取用户名及聊天内容
  - 将对应昵称及聊天内容转发给所有除发送人之外的在线用户
  - 对应代码如下：
  ```python
      def request_chat_handler(self, client_soc, request_data):
        """处理聊天功能"""
        print('收到聊天信息~~准备处理~~')
        # 获取消息内容
        username = request_data['username']
        messages = request_data['messages']
        # pdb.set_trace()
        nickname = self.clients[username]['nickname']

        # 拼接发送给客户端的消息文本
        msg = ResponseProtocol.response_chat(nickname, messages)

        # 转发消息给在线用户
        for u_name, info in self.clients.items():
            if username == u_name:  # 不需要向发送消息的人转发数据
                continue
            info['sock'].send_data(msg)
  ```
### 清理离线用户
- 将离线用户信息移出已登录用户数据库
- 对应代码如下
```python
def remove_offline_user(self, client_soc):
    """客户端下线的处理"""
    print("有客户端下线了~~")
    for username, info in self.clients.items():
        if info['sock'] == client_soc:
            print(self.clients)
            del self.clients[username]
            print(self.clients)
            break
```
