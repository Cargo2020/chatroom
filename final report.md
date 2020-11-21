# I. 项目概述
## 1 简介
使用python开发一个网络多人聊天室。聊天室采用C/S（Client/Server）模式，基于socket编程实现网络通信。程序包括客户端和服务器端两部分，客户端发送聊天信息到服务器端，服务器端负责转发聊天信息给其他所有在线用户。  
聊天室使用TCP协议，在传输数据前建立连接、传输数据后释放连接。TCP能够为通信提供可靠的服务、能够按序到达目的端且不会出现错误。  


## 2 程序功能  
我们的多人聊天室能够实现以下功能：  
(1) 聊天功能。多个用户可以同时登录，进入聊天室进行实时聊天。每位用户能够看到发送信息的用户昵称及信息发送时间。  
(2) 注册功能。新用户可通过注册窗口进行注册，输入昵称及密码，获得数据库返回的唯一用户名。登录时使用用户名及密码登录。  
(3) 多台主机互联。经测试，在不同电脑上运行客户端程序，所有功能均可正常实现。即：用户可通过各自主机连接进入聊天室，进行实时聊天。  
(4) （拓展功能）多聊天室。用户可输入聊天室编号，进入指定聊天室。


## 3 程序结构
本程序分为`Server`和`Client`两个文件夹，具体文件结构见下表。

### 3.1 Server
| 文件名                 | 功能                                                         |
| ---------------------- | ------------------------------------------------------------ |
| `config.py`            | 保存程序中需要的参数，包括操作符、服务器地址和服务器端口号等信息，便于后续程序的引用，也便于后续的修改 |
| `db.py`                |                                                              |
| `response_protocol.py` | 定义了拼接服务器消息的函数                                   |
| `server.py`            | 服务器核心类，集成服务器所需的功能，包括创建与客户端连接、解析并处理客户端消息、向客户端发送消息、处理客户端下线的功能 |
| `server_socket.py`     | 对服务器socket的封装类，包含了服务器socket创建、与IP地址的绑定和进入监听状态 |
| `socket_wrapper.py`    | 对与客户端交互的socket的封装，主要对send和receive方法进行了封装，封装后的方法包含了收发以及收发后的解码 |


### 3.2 Client
| 文件名                | 功能                                                         |
| --------------------- | ------------------------------------------------------------ |
| `config.py`           | 保存程序中需要的参数，包括操作符、服务器地址和服务器端口号等信息，便于后续程序的引用，也便于后续的修改 |
| `request_protocol.py` | 定义了发送到服务器的协议文本格式                              |
| `client.py`           | 客户端核心类，实现客户端响应用户操作、发送消息、接收并处理消息的功能                              |
| `client_socket.py`    | 对客户端socket的封装类，包含了客户端socket创建、与服务器端的连接及收发消息 |
| `login.py`            | 登录及注册窗口图形界面设计                                   |
| `chat_window.py`      | 聊天窗口图形界面设计                                         |

## 4 程序预览

### 4.1 程序运行方式

- 服务器端：需要在config.py文件中配置如下变量，配置结束后直接运行server.py文件即可，程序会开始等待客户端的连接。

| 变量          | 意义                     |
| ------------- | ------------------------ |
| `SERVER_IP`   | 服务器的IP地址。         |
| `SERVER_PORT` | 服务器程序的端口号。     |
| `DB_HOST`     | 数据库服务器的IP地址。   |
| `DB_PORT`     | 数据库管理程序的端口号。 |
| `DB_NAME`     | 数据库名称。             |
| `DB_PASSWORD` | 数据库密码。             |

- 客户端：需要在config.py文件中配置如下变量，配置结束后直接运行client.py文件即可。点击register按钮注册新用户。老用户输入用户名、密码、房间号后点击login按钮即可登录。

| 变量          | 意义                 |
| ------------- | -------------------- |
| `SERVER_IP`   | 服务器的IP地址。     |
| `SERVER_PORT` | 服务器程序的端口号。 |


### 4.2 运行过程预览

==【运行的截图们，可以再描述一下怎么启动程序】==

# II. 协议及技术
## 1 Client-Server 架构
我们开发的多人聊天室采用典型的C/S架构。Client-Server架构是计算机网络中最常用的通信模式之一，其中客户端向服务器请求并接收服务；服务器端等待客户端连接、处理请求并提供服务。一台服务器可以同时为多个客户端提供服务，不同客户端之间的资源不能共享。使用C/S模式的典型应用还包括电子邮件和万维网等。 

![image-20201121154130317](C:\Users\LENOVO\AppData\Roaming\Typora\typora-user-images\image-20201121154130317.png)

与Peer-to-peer结构相比，C/S结构指定了请求服务的客户端和提供服务的服务器端，因此需要一台中心化服务器（而P2P不需要）。在确保服务器端可靠性的前提下，C/S结构使得服务器端能更好的控制和管理客户端对资源的访问，为客户端提供更加安全高效的服务，而且更易于维护和修改。但是C/S结构也存在一些问题。例如当并发客户端请求频繁出现时，服务器会严重超载，造成流量堵塞；当关键服务器端发生故障时，所有客户端请求无法得到满足。这些情况下，C/S集中式体系架构不如P2P网络健壮。<br>

## 2 基于TCP协议的Socket通信
Socket用来描述IP地址和端口，是支持TCP/IP协议网络通信的基本操作单元。应用程序可以通过socket向网络发送请求或对请求做出响应。服务器端socket在特定IP地址的指定端口监听客户端请求，客户端socket指明需要连接的服务器地址及端口号，两端建立连接后即可通过输入输出流交换信息，实现网络通信。
在我们的多人聊天室中，为服务器端及每一个客户端建立socket，服务器端在指定端口（1501）进行监听，不同客户端均绑定相同端口，通过与服务器端的交互实现客户端之间相互通信。具体实现见第三部分。

<img src="C:\Users\LENOVO\AppData\Roaming\Typora\typora-user-images\image-20201121154239741.png" alt="image-20201121154239741" style="zoom:67%;" />

## 3 多线程
  多人聊天室需要多个客户端同时连接到服务器进行交互，因此需要在服务器端使用多线程。每新增加一个客户端连接，就为其分配一个线程，进行通信。<br>


## 4 传输协议
在现有的协议基础上，服务器和客户端的聊天交互还需要设计更高层次的协议。我们还需要自行商定协议，使得服务器和客户端理解正确拆分message的内容。
### 4.1 实现功能
用户端发出注册请求、服务器端响应并处理注册请求、用户端发出登录请求、服务器端响应登录请求、用户端发信、服务器端推送消息。  
各功能的具体实现方式将在下文给出详细说明。
### 4.2 实现方式
在传输字符串中，首先提供操作符，指定操作，后再将各个操作对应参数以分隔符隔开，组合成字符串进行传输，接收端通过读取操作符和分隔符拆分解析信息。
- 操作符：五项功能分别对应五个操作符——用户端发出注册请求（0000）、用户端发出登录请求（0001）、服务器端响应登录请求（1001）、用户端发信（0002）、服务器端推送消息（1002）
- 分隔符：“|”<br>
关于分隔符，可能出现的问题是客户发送的message内部，以及nickname内部可能存在“|”干扰我们的识别。对于message内部存在的“|”，这其实是难以避免的，于是我们将这部分放在传输字符串的最后，这样在客户发送消息含有“|”的时候由于我们的解析是从左向右读取，并不影响消息的正常拆分。而对于nickname内部存在的“|”，我们可以在注册时将含有“|”的nickname设置为非法的昵称，不允许用户使用包含分隔符的昵称。<br>
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
#### 4.2.1 用户端发出注册请求
- 包含信息：nickname, password
- 传输格式：0000|nickname|password
~~~ python
def request_register(nickname, password):
return DELIMITER.join((REQUEST_REGISTER, nickname, password))
~~~
#### 4.2.2 服务器端响应并处理注册请求
- 包含信息：注册结果（1为成功，0为失败）、username
- 传输格式：1000|result|username
~~~ python
def response_register_request(result, username):
return DELIMITER.join([RESPONSE_REGISTER_REQUEST, result, username])
~~~
#### 4.2.3 用户端发出登录请求
- 包含信息：username、password
- 传输格式：0001|username|password
~~~ python
def request_login_result(username, password):
return DELIMITER.join((REQUEST_LOGIN, username, password))
~~~
#### 4.2.4 服务器端响应登录请求
- 包含信息：登录结果（1为成功，0为失败）、nickname、username
- 传输格式：1001|result|nickname|username
~~~ python
def response_login_result(result, nickname, username ):
return DELIMITER.join([RESPONSE_LOGIN_REQUEST,result,nickname,username])
~~~
#### 4.2.5 用户端发信
- 包含信息：username、要发送的信息
- 传输格式：0002|username|message
```python
def request_chat(username, message):
return DELIMITER.join((REQUEST_CHAT, username, message))
```
#### 4.2.6 服务器端推送消息
- 包含信息：nickname、要发送的消息
- 传输格式：1002|nickname|message
``` python
 def response_chat(nickname, massage):
 return DELIMITER.join([RESPONSE_CHAT_REQUEST,nickname, massage])
```


# III. 功能设计与实现

## 1 服务器端
### 1.1 设计逻辑
服务器端主要由以下三个类组成，ServerSocket类和ServerWrapper类分别对不同的功能进行了封装，便于后续的使用
(1) Server类：服务器核心类，包含服务器所需要的所有方法
(2) ServerSocket类：用于封装创建服务器套接字的若干方法，便于在Server类中的调用
(3) ServerWrapper类：用于封装服务器编解码、收发消息的若干方法，便于在Server类中编写获取连接后的消息收发<br>
在核心类Server中，首先创建ServerSocket类，创建服务器套接字。此后在接收到客户端连接时使用ServerWrapper类创建用于服务器端和客户端收发数据的client_socket。由于client_socket为ServerWrapper类，故有已经完成封装的“发送数据+utf-8编码”与“收到消息+utf-8解码”方法，可以直接调用来处理消息收发。<br>
服务器端需要支持多个客户端连接以及与各个客户端进行多次的消息交互，对此我们采用多线程处理及while true循环进行实现，详见下文。

### 1.2 功能及其实现
#### 1.2.1 创建服务器套接字
创建socket的子类ServerSocket类，这个类直接包含服务器创建所需要的基本操作——创建套接字、绑定套接字以及服务器套接字进入监听模式，将这三个操作封装在一起，作为ServerSocket的创建函数，这样在使用中可以更便捷，在主函数中更清晰。故ServerSocket类中包含了socket, bind和listen三个函数，这样在server中调用创建ServerSocket时，就可以直接创建一个已经处于监听状态的socket，使得在server中的代码更加简洁清晰。
对应代码如下：
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
#### 1.2.2 接受客户端连接并提供服务
##### (1) 接受多个客户端连接——while true循环
若仅需要与一个客户端建立连接，直接使用socket.accept()即可。但我们在调试过程中发现，即使serversocket没有关闭，由于socket.accept()代码段已经运行过一次了，新的连接无法创建，故需要多次运行这段代码，再接受新的连接，于是采用while true循环。由于在接收客户端连接之后还需要创建与客户端交互的client_socket，且这个socket每个客户端都需要一个，所以这段代码也要紧接着accept重复运行，因此使用while true不断在接收客户端代码和创建与客户端交互的client_socket之间循环，便于接受多个连接。  
在创建与客户端交互的套接字client_socket时，应生成封装了传输功能的SocketWrapper套接字类以便于使用封装好的方法实现与客户端之间的消息收发。
##### (2) 与多个客户端进行消息收发——多线程处理
服务器端需要同时服务不同的客户端，这些客户端发出的请求和需要的服务都是不相同的，因此需要进行多线程处理。每检测到一个客户端的连接，就开启一个新的线程对其请求进行后续服务。调用Thread类，以客户端请求处理器(request_handler)作为需要创立多线程方法。建立线程后即刻启动线程，收发客户端和服务器端之间的消息。而后续对内容的具体分辨和处理都在客户端请求处理器(request_handler)具体实现。
- Thread类：Thread类需要的参数包括一个可调用的target对象，以及参数args，在这里，我们调用的对象是具体处理客户端消息的request_handler类，参数是request_handler需要的client_soc
至此，服务器端已经完成了与客户端的基本连接，实现了跟多个客户端的多次通信，后续服务器端需要实现的内容就是对客户端消息的拆分和处理。
对应代码如下：
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
#### 1.2.3 服务器对数据的处理
##### (1) 接收客户端请求
如果仅考虑一次性接收客户端请求，直接调用ServerSocket类中的recv_data封装方法即可，而如果需要多次接收客户端请求，则与接收客户端连接类似，需要多次运行到recv_data的代码，故也采取while true的形式。此外，一般而言，在完成接收后，用于与客户端交互的client_socket需要及时关闭，但是这里我们需要多次接收，所以socket.close()不可以直接写在循环中。但我们也不能一直不关闭套接字，于是在循环中需要一个if函数，在客户端发送的消息不为空字符串时，认为客户端还要继续发送，则不关闭套接字，若检测到客户端发送了空套接字，则认为客户端与主机端的通信结束，关闭client_socket。
基于上述考虑，处理客户端请求的流程可总结为：
首先建立循环查看客户端传来的数据，如果客户端没有数据传输，则证明客户端关闭，服务器端将移除离线用户，关闭客户端，结束循环；如果客户端有数据传输，则服务器端接收客户端数据并进行下一步解析处理，分析请求类型并根据请求类型调用相应的处理函数。
对应代码如下：
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
##### (2) 解析并处理客户端信息
根据分隔符解析数据：客户端以统一的格式（request_id|information1|information2)传输数据，数据各部分以分隔符"|"分隔开。服务器将数据解析为三部分，并通过request_id判断请求类型，调用相应函数以处理数据。

- 三种数据信息类型：

  | 功能 | request_id | information1     | information2       |
  | ---- | ---------- | ---------------- | ------------------ |
  | 注册 | 0000       | 昵称(nickname)   | 密码(password)     |
  | 登陆 | 0001       | 用户名(username) | 密码(password)     |
  | 聊天 | 0002       | 用户名(username) | 聊天内容(messages) |

对应代码如下：
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
##### (3) 请求处理函数
创建request_id和方法关联字典，并将request_id和处理函数注册到字典中。这种存储方式将请求类型与处理函数的函数名一一对应起来，且在后续调用过程中直接传输request_id即可得到相应处理函数，这样大大缩减了代码量并且提高了请求处理函数的调用灵活性。  

对应代码如下：
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

- 三种请求处理函数

  | 函数名称                   | 函数功能 | 参数                   | response               |
  | -------------------------- | -------- | ---------------------- | ---------------------- |
  | `request_register_handler` | 注册     | `nickname`, `password` | `username`             |
  | `request_login_handler`    | 登陆     | `username`, `password` | `nickname`, `username` |
  | `request_chat_handler`     | 聊天     | `username`,`message`   | `nickname`, `message`  |

i. 处理注册功能(request_id=0000)：注册功能需要解析出客户端传来的昵称(nickname)和密码(password)，将之存入数据库中，并自动生成一个独一无二的用户名(username)作为用户的唯一身份标识（也是数据库中的主键）传回到客户端。
  对应代码如下：
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
  
ii. 处理登陆功能(request_id=0001)：由于用户只能通过用户名和密码登陆系统，服务器端需要在客户端传来的数据中解析出用户名，密码。首先，服务器需要在数据库中查询用户名与登陆密码是否匹配，以确定用户是否可以登陆。如果用户登陆成功，则将用户名及昵称返回给客户端。
  对应代码如下：
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
  
iii. 处理聊天功能(request_id=0002)：首先服务器端需要解析出用户名(username)及聊天内容(message)，然后在数据库中找到该用户的昵称(nickname)，并将昵称及聊天内容广播给所有在线用户（发送消息的用户除外）
  对应代码如下：
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

##### (4) 清理离线用户
由于我们规定了用户不能向服务器发送空字符串，当某客户端数据为空时会判定其下线,这时需要切断服务器端与客户端之间的连接。
对应代码如下：
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
客户端需要实现三个功能：接收并响应用户操作、发送消息到服务器、重复地接收并处理来自服务器的消息。这些功能主要由Client类实现。  
此外，我们还为客户端设计了图形界面，包括登录/注册窗口及聊天室窗口，为用户提供更友好的交互界面和更便捷的操作方式。

### 2.1 主体功能及其实现

#### 2.1.1 响应用户
在`Client`类中，我们通过以下这些函数实现对用户操作的响应：  
|函数                                     |功能            |
| --------------------------------------- | -------------------------------------------------------- |
|`startup(self)`                      |开启窗口，连接服务器端，创建并开启一个子线程来专门接受消息，实现对窗口操作的响应|
|`clear_inputs(self)`                      |清理窗口内容，打开新窗口的前置工作|
|`response_login_handle(self)` |登录结果的响应|
|`response_register_handle(self)` |注册结果的响应|
|`response_chat_handle(self)` |聊天信息的响应|
|`exit(self)` |退出程序|  

部分功能性函数对应代码如下：
```python
    def startup(self):
        self.conn.connect()
        Thread(target=self.response_handle).start()
        self.window.mainloop()

    def clear_inputs(self):
        self.window.clear_username()
        self.window.clear_password()
        
    def response_login_handle(self, response_data):
        print('接收到登录信息~~', response_data)
        result = response_data['result']
        if result == '0':
            showinfo('提示', '登录失败，账号或密码错误！')
            print('登录失败')
            return

        showinfo('提示', '登录成功！')
        nickname = response_data['nickname']
        username = response_data['username']
        roomnumber = response_data['roomnumber']
        self.username = username
        self.roomnumber = roomnumber
        print('%s 的昵称为 %s，已经登录成功' % (username, nickname))

        self.window_chat.set_title(nickname, roomnumber)
        self.window_chat.update()
        self.window_chat.deiconify()

        self.window.withdraw()

    def response_register_handle(self, response_data):
        print('接收到注册信息~~', response_data)
        result = response_data['result']
        if result == '0':
            showinfo('提示', '注册失败')
            print('注册失败')
            return

        #showinfo('提示', '注册成功！')
        username = response_data['username']
        showinfo('提示', '注册成功！你的账号为 %s。' % username)

    def response_chat_handle(self,response_data):
        print('接收到聊天消息~~', response_data)
        sender = response_data['nickname']
        message = response_data['message']
        self.window_chat.append_message(sender, message)

    def exit(self):
        self.is_running = False
        self.conn.close()
        sys.exit(0)
```
#### 2.1.2 发送消息  

`Client`类中实现发送消息的函数及基本功能见下表：  

|函数                               |功能            |
| -------------------------------- | --------------------------------------------- |
|`send_login_data(self)`      |（1）获取到用户输入的账号密码；<br>（2）生成合乎规则的协议文本；<br>（3）发送协议|
|`send_chat_data(self)`                  |（1）获取输入框内容并清空输入框<br>（2）拼接协议文本<br />（3）发送协议<br />（4）把消息内容显示到聊天区|
|`send_register_data(self)` |（1）获取到用户输入的昵称和密码；<br/>（2）生成协议文本；<br/>（3）发送协议|

三个函数代码如下：
```python
    def send_login_data(self):
        username = self.window.get_username()
        password = self.window.get_password()
        roomnumber = self.window.get_roomnumber()

        request_text = RequestProtocol.request_login_result(username, password, roomnumber)
        print('发送给服务器的登录文本为：'+request_text)
        self.conn.send_data(request_text)
        # recv_data = self.conn.recv_data()
        # print(recv_data)


    def send_chat_data(self):
        message = self.window_chat.get_input()
        print('a %s a' % message)
        self.window_chat.clear_input()

        request_text = RequestProtocol.request_chat(str(self.username), message, str(self.roomnumber))

        self.conn.send_data(request_text)

        self.window_chat.append_message('Me', message)

    def send_register_data(self):
        register_info = self.window.set_up_config()
        nickname = register_info[0]
        password = register_info[1]

        request_text = RequestProtocol.request_register(nickname, password)
        print('发送给服务器的注册文本为：'+request_text)
        self.conn.send_data(request_text)
        # recv_data = self.conn.recv_data()
        # print(recv_data)
```

#### 2.1.3 接收消息  

与服务器端类似，客户端需要实现客户端多次收发消息，我们用while true循环实现。来自服务器的消息分为注册响应、登录响应、聊天信息三类，需要分别解析协议文本。对应代码如下：

```python
    def parse_response_data(recv_data):
        response_data_list = recv_data.split(DELIMITER)

        response_data = dict()
        response_data['response_id'] = response_data_list[0]

        if response_data['response_id'] == RESPONSE_LOGIN_REQUEST:
            response_data['result'] = response_data_list[1]
            response_data['nickname'] = response_data_list[2]
            response_data['username'] = response_data_list[3]
            response_data['roomnumber'] = response_data_list[4]

        elif response_data['response_id'] == RESPONSE_CHAT_REQUEST:
            response_data['nickname'] = response_data_list[1]
            response_data['message'] = response_data_list[2]

        elif response_data['response_id'] == RESPONSE_REGISTER_REQUEST:
            response_data['result'] = response_data_list[1]
            response_data['username'] = response_data_list[2]

        return response_data
```

### 2.2 图形界面
客户端图形界面包括登录窗口以及聊天窗口，主要通过`tkinter`库实现。用户运行程序后首先进入登录窗口，输入用户名及密码，经数据库验证成功后进入聊天窗口，开始收发聊天消息。登录窗口同时提供注册按钮，未经注册的用户需要首先注册后方能登录连入聊天室。
#### 2.2.1 登录/注册窗口  
绘制登录窗口（含注册窗口）的文件为`login.py`，文件主要包含`WindowLogin`类和`RegisterWindow`类。
##### (1) 登录窗口
登录窗口通过创建`WindowLogin`类实现，`WindowLogin`继承了`tkinter`库中的`Tk`窗口类。  
`WindowLogin`类中包含的函数及基本功能见下表：  
| 函数                                             | 功能                                                         |
| ------------------------------------------------ | ------------------------------------------------------------ |
| `window_init(self)`                              | 设置窗口基本属性，包括窗口标题、大小、位置；设置窗口尺寸不可修改 |
| `add_widgets(self)`                              | 添加控件，包括两个标签（Username, Password）、两个对应文本框、以及三个按钮（Reset、Login、Register）。<br>窗口整体采用grid表格布局，用户名、密码的标签及输入框分别放置在第一、二行；三个按钮放置在一个Frame中，Frame整体置于第三行。 |
| `clear_input(self)`                              | 实现对用户名、密码文本框中已输入内容的清除，辅助实现Reset按钮功能 |
| `get_username(self)`                             | 获取用户名文本框中输入内容                                   |
| `get_password(self)`                             | 获取密码文本框中输入内容                                     |
| `on_reset_button_click(self, command)`           | 点击Reset按钮后触发事件，参数command为待执行事件             |
| `on_login_button_click(self, command)`           | 点击Login按钮后触发事件，参数command为待执行事件             |
| `on_register_button_click(self, command)`        | 点击Register按钮后触发事件，参数command为待执行事件          |
| `get_register_info(self)`  `set_up_config(self)` | 调用注册子窗口，等待子窗口输入并获取子窗口中注册文本信息     |
| `on_window_closed(self, command)`                | 用户退出时对窗口资源的释放                                   |

在设计登录窗口时，有意将点击按钮触发指令编写成独立的函数，而非直接在初始化Button时设置command参数。这是为了方便后续客户端向服务器端传递登录/注册信息，以实现点击按钮的同时完成信息的跨端传输。  
部分功能性函数对应代码如下：
```python
    def clear_input(self):
        self.children['username_entry'].delete(0, END)
        self.children['password_entry'].delete(0, END)

    def get_username(self):
        return self.children['username_entry'].get()
    def get_password(self):
        return self.children['password_entry'].get()
        
    def on_reset_button_click(self, command):
        reset_bt = self.children['bt_frame'].children['reset_bt']
        reset_bt['command'] = command
    def on_login_button_click(self, command):
        login_bt = self.children['bt_frame'].children['login_bt']
        login_bt['command'] = command
    def on_register_button_click(self, command):
        register_bt = self.children['bt_frame'].children['register_bt']
        register_bt['command'] = command
        
    def get_register_info(self):
        register_win = RegisterWindow()
        self.wait_window(register_win)
        return register_win.user_info
    def set_up_config(self):
        res = self.get_register_info()
        return res
```
[登录窗口截图]  

##### (2) 注册子窗口  
注册子窗口通过创建`RegisterWindow`类实现，`RegisterWindow`继承了`Toplevel`类，作为登录窗口的子窗口存在。点击登录窗口的``Register``按钮时弹出注册子窗口。
`RegisterWindow`类中包含的函数及基本功能见下表：  

| 函数                         | 功能                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `register_window_init(self)` | （1）设置窗口属性及控件布局，包括窗口标题、大小、位置；设置窗口尺寸不可更改；<br>（2）添加控件，包括两个标签（Nickname、Password）、两个对应文本框以及Register按钮 |
| `get_info(self)`             | 获取两个文本框中用户输入的注册信息，以 [nickname, password] 列表形式保存在user_info变量中 |

调试过程中发现，当点击`Register`按钮弹出注册窗口时，由于主窗口和子窗口实际是同时运行的，登录主窗口不会等待注册子窗口输入完再获取它的值，则传输到数据库中的注册信息总为空。解决方法为单独创建一个`RegisterWindow`注册子窗口类，在主窗口中调用并使用`wait_window()`方法，实现等待注册信息输入完成、点击子窗口中`Register`按钮后登录窗口再进行注册文本的获取及数据库传输。

获取注册信息的`get_info(self)`函数代码如下：
```python
   def get_info(self):
        self.user_info = [self.new_name.get(), self.new_password.get()]
        self.destroy()
```

#### 2.2.2 聊天窗口
绘制聊天窗口的文件为`chat_window.py`。聊天窗口通过创建`ChatWindow`类实现，`ChatWindow`继承了`Toplevel`类。这是因为一个程序只能有一个根窗口（这里是登录窗口），其余窗口均需要以子窗口形式存在。<br>
`ChatWindow`类中包含的函数及基本功能见下表：<br>
| 函数                                    | 功能                                                         |
| --------------------------------------- | ------------------------------------------------------------ |
| `add_widgets(self)`                     | 设置窗口属性及布局，包括聊天内容显示框、聊天文本输入框和发送按钮。其中聊天内容显示框借助滚动文字控件ScrolledText实现。<br>窗口采用grid表格布局，聊天内容显示框放置在第一行；文本输入框及发送按钮放置在第二行，分别占据第一、二列。 |
| `set_title(self, title)`                | 定制化聊天窗口标题，格式为“Welcome ×× into chatroom”，××为对应登录用户的昵称 |
| `on_send_button_click(self, command)`   | 点击Send按钮后触发事件，参数command为待执行事件              |
| `get_input(self)`                       | 获取聊天输入框中输入内容                                     |
| `clear_input(self)`                     | 清除聊天输入框中内容。辅助实现：点击发送按钮后，输入框中内容全部清除（代表信息发送出去） |
| `append_message(self, sender, message)` | 添加聊天信息到聊天内容显示框。效果如图：<br>发送者tag格式为[昵称：当前时间]，用户自己发出的信息昵称会显示为“Me” |
| `on_window_closed(self, command)`       | 用户退出时对窗口资源的释放                                   |

用于添加聊天信息的`append_message()`函数代码如下：
```python
    def append_message(self, sender, message):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime())
        send_info = '%s: %s\n' % (sender, send_time)
        self.children['textarea'].insert(END, send_info, 'green')
        self.children['textarea'].insert(END, ' ' + message + '\n')
        self.children['textarea'].yview_scroll(3, UNITS)
```

## 3 数据库

为了支持注册与登录功能，需要在服务器端部署数据库。我们使用PostgreSQL作为数据库平台，同时使用psycopg2包让Python控制我们的数据库。

我们的数据库设计非常简单，只有一个名为“user_info”的表，该表中包含三列：用户名，昵称和密码。用户名是我们的主键，它是一个唯一的整数，注册时会自动分配。昵称和密码可以由用户设定。该表的设计如下：

```sql
CREATE TABLE IF NOT EXISTS user_info(username serial PRIMARY KEY, nickname VARCHAR(80), password VARCHAR(80)) 
```

我们设计了两个函数来与数据库通信：

| 函数                                     | 功能                                                         |
| ---------------------------------------- | ------------------------------------------------------------ |
| `check_log_in(self, username, password)` | 登录函数，它将检查键入的用户名和密码是否与数据库中存储的数据一致。若一致则返回成功登录信息。 |
| `register(self, nickname, password)`     | 注册函数，它会将新用户的昵称和密码存入数据库，同时返回新用户的唯一用户名。 |


## 4 （拓展功能）多聊天室
在实现基本的多人聊天室功能的基础上，我们考虑对程序进行拓展，实现多聊天室。用户可以在登录窗口输入想要进入的房间号，只有进入相同房间号的用户可以互相收发消息。<br>

为了实现多聊天室的功能，首先需要对服务器与客户端的通信协议进行修改，在客户端请求登录和发送聊天消息时加入房间号：

- 客户端请求登录： 

  `0001|username|password|roomnumber`

- 客户端发送聊天信息：

  `0002|username|messages|roomnumber`

用户登录时需要首先指定房间号`roomnumber`，服务器端将该用户的socket与房间号绑定并存入在线用户字典

```python
self.clients[username] = {'sock': client_soc, 'nickname': nickname, 'roomnumber': roomnumber}
```

客户端发送的聊天信息中也包含房间号，服务器在转发该条聊天时，只转发至有相同房间号的客户端：

```Python
for u_name, info in self.clients.items():
    if username == u_name:  # 不需要向发送消息的人转发数据
        continue
    if info['roomnumber'] == roomnumber: # 只给同一聊天室的人发送信息
        info['sock'].send_data(msg)
```


# Ⅳ 分析与评价
## 1 优化方向
### 1.1 多聊天室
目前，我们仅通过更改传输协议实现多聊天室功能，而没有将房间号作为属性与数据库进行联动。即：不同聊天室的编号及数量已经内嵌在程序中，用户不能更改或添加。这种设计实现起来较为简单，但存在以下两点不足：<br>
（1）用户每次登录只能进入一个聊天室，如需切换需要重新登录  
（2）用户不能自己创建聊天室，且聊天室无密码，所有用户均可进入，无法实现特定用户群体间私密性的群聊功能  
我们认为，通过新增“用户创建聊天室”的功能，可以解决以上问题。具体流程与我们已实现的注册功能类似：用户输入新建聊天室的名称及密码，传至数据库，数据库返回该聊天室的唯一编号（主键）。在选择进入聊天室的界面，用户可通过输入聊天室编号及密码进入指定聊天室。  
基于以上设计，可能需要对传输协议进行修改、在数据库中建立新表存储聊天室信息、以及新建图形界面提供用户输入窗口。我们已进行了部分修改工作，但遗憾程序未能正常运行，因此作为优化方案置于此处。

### 1.2 其他功能
多人聊天室其他可拓展的功能包括：允许用户上传及下载文件、发送表情包、发送视频等。这些功能的实现涉及到其他相关知识（如文件读写、图片编解码等）以及对更多python库的调用，留待我们之后继续学习与改进。  

## 2 程序评价

### 2.1 程序特点
#### (1) 易于修改  
在开发中，我们采取了从建立最基础的功能开始，之后逐步优化的和复杂化开发模式。首先实现了客户端和服务器端的连接，在此基础上实现了单个客户端和单个服务器端的单次消息收发。接着我们进一步实现了客户端和服务器端的多次消息收发，并继续优化至可与多个客户端多次收发消息。完成基本的消息传输搭建后，我们开始对客户端传来的不同消息编写方法进行处理，最终完成了单聊天室多客户端多次通讯的设计。在实现基本功能后，我们又尝试了将现有的单聊天室转化为多聊天室，完成了最终提交的设计。<br>
依照上述开发过程，我们的代码从整体上呈现出层次化的特点。后续的功能都是以前面的功能为基础，在前面的功能上叠加新的方法进行处理。如对客户端消息的解析和处理是基于客户端和服务器端的基本的消息传递。这样的设计使得此程序在进一步添加功能上非常容易，且新功能的加入并不会对原有的同级功能和更底层功能产生影响。这一特点在debug中为我们节省了很多时间，也为此程序提供了较好的成长性。<br>
#### (2) 简洁性
在方法编写上，我们对socket类现有的基本方法进行了封装，为不同功能的socket建立了不同的子类，子类中有封装好的方法。这样的设计模式使得核心类的代码非常简洁，易于阅读，在多人开发的过程中大大提升了效率。且在修改方法细节时可以直接在子类中修改，而不需要在每次调用处进行修改，对于多次调用的方法在修改上也更便利。<br>
#### (3) 高成长性
在方法调用上，我们采取了方法关联字典的技巧。在实操过程中我们发现，我们需要server处理的情景越来越多，在初始的代码编写中，我们采用了先解析服务器收到的数据，得到请求id（请求id代表了这是一个 注册/登陆/聊天的请求)，并不断进行条件判断，调用不同的函数。但是随着请求id的增多，每一次更改代码都略显繁琐，所以我们采用了方法关联字典的方式来解决这个问题。采用方法关联字典后，对新请求的处理只需要在方法关联字典上添加即可，调用时只需要在方法关联字典中按照请求id寻找方法即刻。此技巧避免了冗长的条件判断，减少了修改的代码量，也赋予了这个聊天室更好的功能成长性。<br><br>
总结来看，我们在开发过程中充分考虑到了多人合作开发的实际需求，通过以上方式尽可能减少组员之间的代码依赖性，提高程序鲁棒性。因此，整个开发过程较为灵活，推进过程比较顺利。

### 2.2 程序不足
(1) 实现的功能较少。目前仅支持公共聊天室内的文字聊天，缺少私聊、上传文件及图片等功能。
(2) 用户体验不够完善。用户登录后仅能在聊天室内收发信息，而不能知道当前在线的用户数量及身份。此外，程序不具有查看其他人用户名的功能，所有用户都是使用昵称交流，因此在聊天室中很难分辨两个昵称一样的用户。
(3) 尚不支持用户修改昵称及密码，提出这类请求需要增加新的操作符。
(4) 传输协议设计的比较简单。这固然为我们的程序实现带来了便利，但同时也可能限制了对更多更复杂功能的拓展与开发。
