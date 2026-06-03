# Java 单元测试

## 运行命令

```bash
bash java/scripts/mvn-test.sh
```

## 测试参考

Java 单元测试参考 Python SDK 的做法（`python/tests/test_device_info.py`）：
- 从 `.env` 文件加载环境变量（使用 `dotenv-java`）
- 使用 `RobotController` 创建客户端
- 测试方法名、断言逻辑与 Python 测试保持一致

## 测试文件

- `java/src/test/java/cn/boticz/masrobo/service/IotDeviceServiceTest.java`
- 环境变量文件：`java/.env`