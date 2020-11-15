

# I. 项目概述

# II. 协议及技术
## 传输协议
### 实现的功能：用户端发出注册请求、服务器端响应并处理注册请求、用户端发出登录请求、服务器端响应登录请求、用户端发信、服务器端推送消息
### 实现方式：通过定义不同的操作变化定义不同的操作，并以“|”为分隔符传递信息，将要传递的信息组合拼接进行传输。接收方按照协议的对拼接后的字符串进行分割，获取需要的信息。具体设计如下
```python
#-----------set_ups-------------------
REQUEST_REGISTER = '0000' #REGISTER REQUEST
REQUEST_LOGIN = '0001' # LOGIN REQUEST
REQUEST_CHAT = '0002' # CHATTING  REQUEST
RESPONSE_REGISTER_REQUEST = '1000'
RESPONSE_LOGIN_REQUEST = '1001' # RESPOND TO LOG IN
RESPONSE_CHAT_REQUEST = "1002" #RESPOND TO CHATTING
DELIMITER = "|"
```
#### 用户端发出注册请求
- 包含信息：nickname, password
- 传输格式：0000|nickname|password
- 具体代码如下
~~~ python
def request_register(nickname, password):
return DELIMITER.join((REQUEST_REGISTER, nickname, password))
~~~
#### 服务器端响应并处理注册请求
- 包含信息：注册结果（1为成功，0为失败）、username
- 传输格式：1000|result|username
#### 用户端发出登录请求
- 包含信息：username、password
- 传输格式：0001|username|password
#### 服务器端响应登录请求
- 包含信息：登录结果（1为成功，0为失败）、nickname、username
- 传输格式：1001|result|nickname|username
#### 用户端发信
- 包含信息：username、要发送的信息
- 传输格式：0002|username|message
#### 服务器端推送消息
- 包含信息：nickname、要发送的消息
- 传输格式：1002|nickname|message


# III. 功能设计与实现


## 1 服务器端
### 服务器对数据的处理
#### 接收客户端请求
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
#### 解析并处理客户端信息
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
#### 请求处理函数
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
#### 清理离线用户
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



## 2 客户端


## 3 数据库

## 4 GUI（客户端）
客户端图形界面包括登录窗口以及聊天窗口，主要通过`Tkinter`库实现。用户运行程序后首先进入登录窗口，输入用户名及密码，经数据库验证成功后进入聊天窗口，开始收发聊天消息。登录窗口同时提供注册按钮，未经注册的用户需要首先注册后方能登录连入聊天室。  

### 4.1 登录/注册窗口  
绘制登录窗口（含注册窗口）的文件为`login.py`，文件主要包含`WindowLogin`类和`RegisterWindow`类。
#### 4.1.1 登录窗口
登录窗口通过创建'WindowLogin'类实现，`WindowLogin`继承了`tkinter`库中的`Tk`窗口类。  
`WindowLogin`类中包含的函数及基本功能见下表：  
|函数                                     |功能            |
| --------------------------------------- | -------------------------------------------------------- |  
|`window_init(self)`                      |设置窗口基本属性，包括窗口标题、大小、位置；设置窗口尺寸不可修改|  
|`add_widgets(self)`                      |添加控件，包括两个标签（Username, Password）、两个对应文本框、以及三个按钮（Reset、Login、Register）。<br>窗口整体采用grid表格布局，用户名、密码的标签及输入框分别放置在第一、二行；三个按钮放置在一个Frame中，Frame整体置于第三行。|
|`clear_input(self)`                      |实现对用户名、密码文本框中已输入内容的清除，辅助实现Reset按钮功能|  
|`get_username(self)`                     |获取用户名文本框中输入内容|  
|`get_password(self)`                     |获取密码文本框中输入内容|  
|`on_reset_button_click(self, command)`   |点击Reset按钮后触发事件，参数command为待执行事件|  
|`on_login_button_click(self, command)`   |点击Login按钮后触发事件，参数command为待执行事件|  
|`on_register_button_click(self, command)`|点击Register按钮后触发事件，参数command为待执行事件|  
|`get_register_info(self)`  `set_up_config(self)` |调用注册子窗口，等待子窗口输入并获取子窗口中注册文本信息|
|`on_window_closed(self, command)`        |用户退出时对窗口资源的释放|

在设计登录窗口时，有意将点击按钮触发指令编写成独立的函数，而非直接在初始化Button时设置command参数。这是为了方便后续客户端向服务器端传递登录/注册信息，以实现点击按钮的同时完成信息的跨端传输。  
[登录窗口截图]  

### 4.1.2 注册子窗口  
注册子窗口通过创建`RegisterWindow`类实现，`RegisterWindow`继承了`Toplevel`类，作为登录窗口的子窗口存在。点击登录窗口的``Register``按钮时弹出注册子窗口。
`RegisterWindow`类中包含的函数及基本功能见下表：  

|函数                               |功能            |
| -------------------------------- | --------------------------------------------- |  
|`register_window_init(self)`      |（1）设置窗口属性及控件布局，包括窗口标题、大小、位置；设置窗口尺寸不可更改；<br>（2）添加控件，包括两个标签（Nickname、Password）、两个对应文本框以及Register按钮|  
|`get_info(self)`                  |获取两个文本框中用户输入的注册信息，以 [nickname, password] 列表形式保存在user_info变量中|  

调试过程中发现，当点击Register按钮弹出注册窗口时，由于主窗口和子窗口实际是同时运行的，登录主窗口不会等待注册子窗口输入完再获取它的值，则传输到数据库中的注册信息总为空。解决方法为单独创建一个RegisterWindow注册子窗口类，在主窗口中调用并使用wait_window()方法，实现等待注册信息输入完成、点击子窗口中Register按钮后登录窗口再进行注册文本的获取及数据库传输。
