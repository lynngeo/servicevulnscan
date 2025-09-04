# 记录日志的模块

from loguru import logger
import sys
import os

# 终端日志输出格式
stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
    '[<level>{level: <5}</level>] ' \
    '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
    '<level>{message}</level>'

logger.remove()
'''
自定义日志等级
调用方式：logger.log("<level>", "<message>")
'''
logger.level(name='TRACE', color='<cyan><bold>', icon='✏️')
logger.level(name='DEBUG', color='<blue><bold>', icon='🐞 ')
logger.level(name='INFOR', no=20, color='<green><bold>', icon='ℹ️')
logger.level(name='ALERT', no=30, color='<yellow><bold>', icon='⚠️')
logger.level(name='ERROR', color='<red><bold>', icon='❌️')
logger.level(name='FATAL', no=50, color='<RED><bold>', icon='☠️')
if not os.environ.get('PYTHONIOENCODING'):  # 设置编码
    os.environ['PYTHONIOENCODING'] = 'utf-8'
logger.add(sys.stderr, level='INFOR', format=stdout_fmt, enqueue=True)
