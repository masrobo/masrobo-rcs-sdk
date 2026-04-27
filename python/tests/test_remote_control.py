import os
import sys
import logging
import argparse
from dotenv import load_dotenv

# 添加父目录到 Python 路径，以便使用相对路径引入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from masrobo_rcs_sdk import SendDeviceCommandRequest, TopicRemoteControl, RobotController

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Remote control test script')
    parser.add_argument('--base-url', help='Base URL for the RCS API')
    parser.add_argument('--app-id', help='Application ID')
    parser.add_argument('--app-key', help='Application Key')
    parser.add_argument('--device-id', default='0b67403e575fed0b', help='Device ID')
    parser.add_argument('--product-name', default='AibbyPet', help='Product name')
    parser.add_argument('--command', default='move', help='Command to send')
    parser.add_argument('--parameter', default='{"x": 0, "y": 0}', help='Command parameter')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    return parser.parse_args()

def load_config(args):
    """加载配置"""
    # 尝试从.env文件加载环境变量
    load_dotenv()
    
    config = {
        'base_url': args.base_url or os.environ.get('BASE_URL'),
        'app_id': args.app_id or os.environ.get('APP_ID'),
        'app_key': args.app_key or os.environ.get('APP_KEY'),
        'device_id': args.device_id,
        'product_name': args.product_name,
        'command': args.command,
        'parameter': args.parameter
    }
    
    # 验证必要的配置
    required_fields = ['base_url', 'app_id', 'app_key']
    missing_fields = [field for field in required_fields if not config[field]]
    if missing_fields:
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
    
    return config

def main():
    """主函数"""
    try:
        args = parse_args()
        
        if args.debug:
            logger.setLevel(logging.DEBUG)
        
        logger.info("Starting remote control test...")
        
        # 加载配置
        config = load_config(args)
        logger.debug(f"Configuration: {config}")
        
        # 创建客户端
        logger.info("Creating RobotController instance...")
        client = RobotController(
            base_url=config['base_url'],
            app_id=config['app_id'],
            app_key=config['app_key'],
        )
        
        # 构建请求
        logger.info(f"Preparing command: {config['command']} with parameter: {config['parameter']}")
        request = SendDeviceCommandRequest(
            command=config['command'],
            parameter=config['parameter'],
            device_id=config['device_id'],
            product_name=config['product_name'],
            topic_name=TopicRemoteControl,
        )
        
        # 发送命令
        logger.info("Sending device command...")
        response = client.IotDevice.send_device_command(request)
        logger.info(f"Command sent successfully! Response: {response}")
        
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()