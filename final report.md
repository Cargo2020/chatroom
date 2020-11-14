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
### 解析客户端信息
- 根据分隔符解析数据
  - 
### 判断请求类型
### 调用请求对应处理函数
- 客户端会发来四种类型的数据，分别是请求注册、请求登陆、请求聊天和请求发送文件，服务器需要对其解析，分析请求类型，并根据请求类型调用相应的处理函数
