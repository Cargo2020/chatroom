from config import *

class ResponseProtocol(object):
#*******服务器响应协议的格式******

    @staticmethod
    def response_login_result(result, nickname, username ):
         """
         生成用户登录的字符串
         result ：成功与否（1成功）
         nickname ： 昵称
         username ： 用户名
         return : 返回的登录结果字符串
         """
        return DELIMITER.join([RESPONSE_LOGIN_REQUEST, 
        result, nickname, username])

    @staticmethod
    def response_chat(nickname, massage):
        """
        """
        return DELIMITER.join([RESPONSE_CHAT_REQUEST, 
        nickname, massage])