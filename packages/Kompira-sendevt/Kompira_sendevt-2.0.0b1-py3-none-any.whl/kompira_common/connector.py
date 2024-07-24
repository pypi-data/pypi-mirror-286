# -*- coding: utf-8 -*-
import logging
import socket
from time import sleep
from ssl import SSLError, SSLSocket, VerifyMode, create_default_context

import amqpstorm
import amqpstorm.connection
import amqpstorm.channel
from amqpstorm.exception import AMQPConnectionError

from .config import DEFAULT_SSL_CACERTFILE, DEFAULT_SSL_CERTFILE, DEFAULT_SSL_KEYFILE, DEFAULT_SSL_VERIFY

#
# [NOTICE]
#   コマンドジョブのパフォーマンス改善のためウェイトを短くする(0.01 --> 0.002)
#
amqpstorm.connection.IDLE_WAIT = amqpstorm.channel.IDLE_WAIT = 0.002

logger = logging.getLogger('kompira')


DEFAULT_AMQP_PORT = 5672
DEFAULT_AMQPS_PORT = 5671
DEFAULT_USER_LOCAL = 'guest'
DEFAULT_USER_REMOTE = 'kompira'


class AMQPConnection:
    _default_parameters = {}

    @classmethod
    def setup(cls, server='localhost', port=None, user=None, password=None, ssl=None, **kwargs):
        """
        AMQP サーバへの接続設定

        - ローカルの AMQP サーバにはデフォルトで非 SSL で接続 (リモートには SSL)
        - ローカルの AMQP サーバにはデフォルトで guest ユーザで認証 (リモートには kompira)
        - パスワードはデフォルトでユーザ名と同じ
        - ポート番号は SSL 接続か否かでデフォルト値を調整 (5671 if ssl else 5672)
        """
        is_local = server in ('localhost', '127.0.0.1')
        if ssl is None and is_local:
            ssl = False
        if user is None:
            user = DEFAULT_USER_LOCAL if is_local else DEFAULT_USER_REMOTE
        if password is None:
            password = user
        if port is None:
            port = DEFAULT_AMQPS_PORT if ssl else DEFAULT_AMQP_PORT
        # SSL 接続時はオプションを辞書で渡す
        ssl_verify = kwargs.pop('ssl_verify', DEFAULT_SSL_VERIFY)
        ssl_cacertfile = kwargs.pop('ssl_cacertfile', None)
        ssl_certfile = kwargs.pop('ssl_certfile', None)
        ssl_keyfile = kwargs.pop('ssl_keyfile', None)
        cls._default_parameters['hostname'] = server
        cls._default_parameters['username'] = user
        cls._default_parameters['password'] = password
        cls._default_parameters['port'] = port
        cls._default_parameters['ssl'] = ssl
        if ssl:
            if ssl_verify:
                ssl_context = create_default_context(cafile=ssl_cacertfile or DEFAULT_SSL_CACERTFILE)
                ssl_context.verify_mode = VerifyMode.CERT_REQUIRED
                ssl_context.check_hostname = False
                ssl_context.load_cert_chain(ssl_certfile or DEFAULT_SSL_CERTFILE, ssl_keyfile or DEFAULT_SSL_KEYFILE)
                cls._default_parameters['ssl_options'] = {
                    'context': ssl_context
                }
            else:
                cls._default_parameters['ssl_options'] = {
                    'verify_mode': 'none'
                }

        cls._default_parameters.update(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        params = {}
        params.update(**cls._default_parameters)
        params.update(**kwargs)
        conn = amqpstorm.Connection(**params)
        #
        # [NOTICE]
        #   コマンドジョブのパフォーマンス改善のため TCP_NODELAY オプションをセットする
        #
        conn.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return conn

    @classmethod
    def get_ssl_version(cls, conn):
        sock = conn.socket
        if isinstance(sock, SSLSocket):
            try:
                return sock.version()
            except Exception as e:
                logger.exception('%s.get_ssl_version: caught %s', cls.__class__.__name__, e)
                return '<unknown>'
        return None

    @classmethod
    def get_sock_info(cls, conn):
        sockname = '%s:%s' % conn.socket.getsockname()[:2]
        peername = '%s:%s' % conn.socket.getpeername()[:2]
        ssl_ver = cls.get_ssl_version(conn)
        return f'AMQPS({sockname}->{peername},{ssl_ver})' if ssl_ver else f'AMQP({sockname}->{peername})'


class AMQPConnector:
    def __init__(self, post_connect=None, **kwargs):
        AMQPConnection.setup(**kwargs)
        self._post_connect = post_connect
        self._conn = None
        self._chan = None
        self._terminate = False
        self._max_retry = kwargs.get('max_retry', 3)
        self._retry_interval = kwargs.get('retry_interval', 30)

    @property
    def connection(self):
        return self._conn

    @property
    def channel(self):
        return self._chan

    @property
    def ssl_version(self):
        return AMQPConnection.get_ssl_version(self._conn)

    def _connect(self):
        logger.info('[%s] _connect start', self.__class__.__name__)
        self._conn = AMQPConnection.create()
        self._chan = self._conn.channel()
        logger.info('[%s] established connection to %s', self.__class__.__name__, AMQPConnection.get_sock_info(self._conn))
        if self._post_connect:
            self._post_connect(self._chan)
        logger.info('[%s] _connect succeeded', self.__class__.__name__)

    def close(self):
        #
        # コネクションのクローズ
        #
        try:
            self._terminate = True
            if self._conn:
                self._conn.close()
        except IOError as e:
            logger.error('[%s] failed to close connection: %s', self.__class__.__name__, e)

    def loop(self):
        retry_count = self._max_retry
        while not self._terminate:
            try:
                self._connect()
                #
                # 接続確立したらretry_countをリセットしておく
                #
                retry_count = self._max_retry
                self._chan.start_consuming()
                break
            except (KeyboardInterrupt, SystemExit) as e:
                logger.info('[%s] caught %s', self.__class__.__name__, type(e).__name__)
                break
            except AMQPConnectionError as e:
                logger.error('[%s] AMQP connection error: %s', self.__class__.__name__, e)
            except SSLError as e:
                logger.error('[%s] SSL error: %s', self.__class__.__name__, e)
            except socket.error as e:
                logger.exception('[%s] socket error: %s', self.__class__.__name__, e)
            except Exception as e:
                logger.exception('[%s] %s', self.__class__.__name__, e)
                break
            finally:
                if self._conn:
                    self._conn.close()
            #
            # 再接続処理
            #
            if retry_count == 0:
                logger.error('[%s] gave up retry connection', self.__class__.__name__)
                break
            elif self._max_retry > 0:
                retry_count -= 1
            self._wait()

    def _wait(self):
        if not self._terminate:
            logger.info('[%s] waiting %s seconds for retry connection ...', self.__class__.__name__, self._retry_interval)
            sleep(self._retry_interval)
