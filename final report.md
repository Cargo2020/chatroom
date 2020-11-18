

# I. 项目概述
## 1 简介
使用python开发一个网络多人聊天室。聊天室采用C/S（Client/Server）模式，基于socket编程实现网络通信。程序包括客户端和服务器端两部分，客户端发送聊天信息到服务器端，服务器端负责转发聊天信息给其他所有在线用户。  
聊天室使用TCP协议，在传输数据前建立连接、传输数据后释放连接。TCP能够为通信提供可靠的服务、能够按序到达目的端且不会出现错误。  
基本处理流程见下图：
[可以做一张流程图]

## 2 项目预览
【运行的截图们，可以再描述一下怎么启动程序】

# II. 协议及技术
## 1 Client-Server 架构
我们开发的多人聊天室采用典型的C/S架构。Client-Server架构是计算机网络中最常用的通信模式之一，其中客户端向服务器请求并接收服务；服务器端等待客户端连接、处理请求并提供服务。一台服务器可以同时为多个客户端提供服务，不同客户端之间的资源不能共享。使用C/S模式的典型应用还包括电子邮件和万维网等。  <br>
[图片]<br>
与Peer-to-peer结构相比，C/S结构指定了请求服务的客户端和提供服务的服务器端，因此需要一台中心化服务器（而P2P不需要）。在确保服务器端可靠性的前提下，C/S结构使得服务器端能更好的控制和管理客户端对资源的访问，为客户端提供更加安全高效的服务，而且更易于维护和修改。但是C/S结构也存在一些问题。例如当并发客户端请求频繁出现时，服务器会严重超载，造成流量堵塞；当关键服务器端发生故障时，所有客户端请求无法得到满足。这些情况下，C/S集中式体系架构不如P2P网络健壮。<br>
## 2 基于TCP协议的Socket通信
Socket用来描述IP地址和端口，是支持TCP/IP协议网络通信的基本操作单元。应用程序可以通过socket向网络发送请求或对请求做出响应。服务器端socket在特定IP地址的指定端口监听客户端请求，客户端socket指明需要连接的服务器地址及端口号，两端建立连接后即可通过输入输出流交换信息，实现网络通信。
在我们的多人聊天室中，为服务器端及每一个客户端建立socket，服务器端在指定端口（1501）进行监听，不同客户端均绑定相同端口，通过与服务器端的交互实现客户端之间相互通信。具体实现见第三部分。
[可以放一张socket通信图]

## 3 多线程
  多人聊天室需要多个客户端同时连接到服务器进行交互，因此需要在服务器端使用多线程。每新增加一个客户端连接，就为其分配一个线程，进行通信。<br>


## 4 传输协议
### 在现有的协议基础上，服务器和客户端的聊天交互还需要设计更高层次的协议。我们还需要自行商定协议，使得服务器和客户端理解正确拆分message的内容。
### 实现的功能
#### 用户端发出注册请求、服务器端响应并处理注册请求、用户端发出登录请求、服务器端响应登录请求、用户端发信、服务器端推送消息
### 实现方式
#### 在传输字符串中，首先提供操作符，指定操作，后再将各个操作对应参数以分隔符隔开，组合成字符串进行传输，接收端通过读取操作符和分隔符拆分解析信息。操作符：四项功能分别对应四个操作符，用户端发出登录请求（0001）、服务器端响应登录请求（1001）、用户端发信（0002）、服务器端推送消息（1002），同时选择分隔符：“|”
#### 关于使用的分隔符，可能出现的问题是客户发送的消息内部，以及nickname内部可能存在“|”干扰我们的识别。对于message内部存在的“|”，这其实是难以避免的，于是我们将这部分放在传输字符串的最后，这样在客户发送消息含有“|”的时候由于我们的解析是从左向右读取，并不影响消息的正常拆分。而对于nickname内部存在的“|”，我们可以在注册时将含有“|”的nickname设置为非法的昵称，不允许用户使用包含分隔符的昵称
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
~~~ python
def request_register(nickname, password):
return DELIMITER.join((REQUEST_REGISTER, nickname, password))
~~~
#### 服务器端响应并处理注册请求
- 包含信息：注册结果（1为成功，0为失败）、username
- 传输格式：1000|result|username
~~~ python
def response_register_request(result, username):
return DELIMITER.join([RESPONSE_REGISTER_REQUEST, result, username])
~~~
#### 用户端发出登录请求
- 包含信息：username、password
- 传输格式：0001|username|password
~~~ python
def request_login_result(username, password):
return DELIMITER.join((REQUEST_LOGIN, username, password))
~~~
#### 服务器端响应登录请求
- 包含信息：登录结果（1为成功，0为失败）、nickname、username
- 传输格式：1001|result|nickname|username
~~~ python
def response_login_result(result, nickname, username ):
return DELIMITER.join([RESPONSE_LOGIN_REQUEST,result,nickname,username])
~~~
#### 用户端发信
- 包含信息：username、要发送的信息
- 传输格式：0002|username|message
```python
def request_chat(username, message):
return DELIMITER.join((REQUEST_CHAT, username, message))
```
#### 服务器端推送消息
- 包含信息：nickname、要发送的消息
- 传输格式：1002|nickname|message
``` python
 def response_chat(nickname, massage):
 return DELIMITER.join([RESPONSE_CHAT_REQUEST,nickname, massage])
```
# III. 功能设计与实现


## 1 服务器端
### 服务器端设计逻辑
- 服务器端主要由以下三个类组成
  - Server类：服务器核心类，包含服务器所需要的所有方法
  - ServerSocket类：用于封装创建服务器套接字的若干方法，便于在Server类中的调用
  - ServerWrapper类：用于封装服务器编解码、收发消息的若干方法，便于在Server类中编写获取连接后的消息收发
- 在核心类Server中，首先创建ServerSocket类，创建服务器套接字，此后在接收到客户端连接时使用ServerWrapper类，创建服务器和客户端收发数据使用的client_socket。client_socket为ServerWrapper类，故有已近完成封装的“发送数据+utf-8编码”与“收到消息+utf-8解码”方法，可以直接调用来处理消息收发。
-实现多客户端连接以及客户端多次收发消息：多线程处理及while true循环（详见下文）
### 创建服务器套接字
#### 创建服务器套接字
- 创建socket的子类ServerSocket类，在这个类中直接包含服务器创建所需要的基本操作（创建套接字、绑定套接字以及服务器套接字进入监听模式），将这三个操作封装在一起，作为ServerSocket的创建函数，这样在使用中可以更便捷，在主函数中更清晰。故ServerSocket类中包含了socket, bind和listen三个函数。
- 创建套接字
- 将套接字与IP地址和端口号绑定
- 进入监听模式
- 为设计简便，将上述三个基本功能封装入ServerSocket类中，创建此类后，将直接完成上述操作，进入监听模式
- 对应代码如下
``` python
#ServerSocket类
class ServerSocket(socket.socket):

    def __init__(self):
        #设置为TCP类型
        super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        #设置地址和端口号
        self.bind((SERVER_IP, SERVER_PORT))
        #设置为监听模式
        self.listen(128)
     
#在服务器核心类Server中初始化ServerSocket
def __init__(self):
    self.server_socket = ServerSocket()
    print("waiting for connection")
```
### 接受客户端连接并提供服务
#### 接受多个客户端连接
- 若仅需要与一个客户端建立连接，那么直接使用socket.accept即可，但是此时存在多个客户端连接，就需要服务器端在接受一个连接后可以再次运行到socket.accpet的代码，再次接受新的连接，于是此时采用while true循环，不断在接收客户端代码和创建与客户端交互的client_socket之间循环，便于接受多个连接。
- 在创建与客户端交互的套接字时，应生成SocketWrapper套接字以便于使用封装好的方法实现与客户端之间的消息收发。
#### 与多个客户端进行消息收发
- 对不同客户端的连接需要进行多线程处理，每检测到一个客户端的连接，就开始一个新的线程对其请求进行后续消息收发服务。使用Thread类，以客户端请求处理器(request_handler)作为需要创立多线程方法。建立线程后即刻启动线程，收发客户端和服务器端之间的通信。而后续对内容的具体分辨和处理都在客户端请求处理器(request_handler)具体实现。
#### 对应代码如下
``` python
def startup(self):
        """获取客户端连接并提供服务"""
        while True:
            # 获取客户端连接
            soc, addr = self.server_socket.accept()

            # 生成套接字（与客户端交互）
            client_soc = SocketWrapper(soc)

            # 收发消息
            t = Thread(target=self.request_handler, args=(client_soc,))
            t.start()
```
### 服务器对数据的处理
#### 接收客户端请求
- 如果仅考虑一次性接收客户端请求，直接调用ServerSocket类中的recv_data封装方法即可，而如果需要多次接收客户端请求，则与接收客户端连接类似，需要多次运行到recv_data的代码，故也采取while true的形式。此外，一般而言，在完成接收后，用于与客户端交互的client_socket需要及时关闭，但是这里我们需要多次接收，所以socket.close不可以直接写在循环中，但是我们也不能一直不关闭套接字。于是在循环中需要一个if函数，在客户端发送的消息不为空字符串时，认为客户端还要继续发送，则不关闭套接字，若检测到客户端发送了空套接字，则认为客户端与主机端的通信结束了，就关闭client_socket。
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

#### 4.1.2 注册子窗口  
注册子窗口通过创建`RegisterWindow`类实现，`RegisterWindow`继承了`Toplevel`类，作为登录窗口的子窗口存在。点击登录窗口的``Register``按钮时弹出注册子窗口。
`RegisterWindow`类中包含的函数及基本功能见下表：  

|函数                               |功能            |
| -------------------------------- | --------------------------------------------- |  
|`register_window_init(self)`      |（1）设置窗口属性及控件布局，包括窗口标题、大小、位置；设置窗口尺寸不可更改；<br>（2）添加控件，包括两个标签（Nickname、Password）、两个对应文本框以及Register按钮|  
|`get_info(self)`                  |获取两个文本框中用户输入的注册信息，以 [nickname, password] 列表形式保存在user_info变量中|  

调试过程中发现，当点击`Register`按钮弹出注册窗口时，由于主窗口和子窗口实际是同时运行的，登录主窗口不会等待注册子窗口输入完再获取它的值，则传输到数据库中的注册信息总为空。解决方法为单独创建一个`RegisterWindow`注册子窗口类，在主窗口中调用并使用`wait_window()`方法，实现等待注册信息输入完成、点击子窗口中`Register`按钮后登录窗口再进行注册文本的获取及数据库传输。

### 4.2 聊天窗口
绘制聊天窗口的文件为`chat_window.py`。聊天窗口通过创建`ChatWindow`类实现，`ChatWindow`继承了`Toplevel`类。这是因为一个程序只能有一个根窗口（这里是登录窗口），其余窗口均需要以子窗口形式存在。<br>
`ChatWindow`类中包含的函数及基本功能见下表：<br>
|函数                                     |功能            |
| --------------------------------------- | -------------------------------------------------------- |  
|`add_widgets(self)`                      |设置窗口属性及布局，包括聊天内容显示框、聊天文本输入框和发送按钮。其中聊天内容显示框借助滚动文字控件ScrolledText实现。<br>窗口采用grid表格布局，聊天内容显示框放置在第一行；文本输入框及发送按钮放置在第二行，分别占据第一、二列。|  
|`set_title(self, title)`                      |定制化聊天窗口标题，格式为“Welcome ×× into chatroom”，××为对应登录用户的昵称|
|`on_send_button_click(self, command)`         |点击Send按钮后触发事件，参数command为待执行事件|  
|`get_input(self)`                     |获取聊天输入框中输入内容|  
|`clear_input(self)`                     |清除聊天输入框中内容。辅助实现：点击发送按钮后，输入框中内容全部清除（代表信息发送出去）|  
|`append_message(self, sender, message)`   |添加聊天信息到聊天内容显示框。效果如图：<br>发送者tag格式为[昵称：当前时间]，用户自己发出的信息昵称会显示为“Me”|  
|`on_window_closed(self, command)`       |用户退出时对窗口资源的释放|


# Ⅳ 优化方案
## 1 多聊天室
### 1.1 目前多聊天室的实现方式：
- 用户登录时输入聊天室号码
- 服务器数据库记录此次登录进入的聊天室
- 客户端向服务器发送消息
- 服务器仅向进入输入相同聊天室号的客户端推送消息。
### 1.2 存在的问题
- 用户每次登录只能进入一个聊天室，如需切换则需要重新登陆
- 用户进入聊天室没有限制，可随意进入他人聊天室，安全性较低。综合这两个缺点
- 当前的设计需要组织内部预先分配聊天室号码。
### 1.3 可能的优化方案：
- 在数据库中建立新表，包含聊天室号和聊天室密码
- 创建新页面：创建和加入聊天室
- 创建和加入聊天室
 - 创建：若在加入聊天室页面中，若输入不存在的聊天室号，则视为创建新聊天室，首次输入的密码即作为聊天室密码计入聊天室表中
 - 加入：加入新聊天室前，要求用户输入密码。若用户成功输入正确密码加入聊天室，则在用户表中插入一列，包含username、nickname、password、chatroom
- 不同聊天室消息收发：在现有仅向处在同一个聊天室的客户端推送消息的基础上，设计GUI使得不同聊天室的消息显示在不同的页面上
