import { describe, it, expect } from 'vitest';

import { RobotController } from '../src/robot_controller';

function createService() {
  const { VITE_BASE_URL, VITE_APP_ID, VITE_APP_KEY, VITE_DEVICE_ID, VITE_PROJECT_NAME } = process.env;
  if (!VITE_BASE_URL || !VITE_APP_ID || !VITE_APP_KEY || !VITE_DEVICE_ID || !VITE_PROJECT_NAME) {
    throw new Error('环境变量不完整，请确保 .env 文件中包含 VITE_BASE_URL、VITE_APP_ID、VITE_APP_KEY、VITE_DEVICE_ID、VITE_PROJECT_NAME');
  }
  return {
    controller: new RobotController({
      baseURL: VITE_BASE_URL,
      appId: VITE_APP_ID,
      appKey: VITE_APP_KEY,
    }),
    deviceId: VITE_DEVICE_ID,
    productName: VITE_PROJECT_NAME,
  };
}

describe('TestGetDeviceInfo', () => {
  it('test_get_device_info', async () => {
    const { controller, deviceId, productName } = createService();

    const result = await controller.IotDevice.getDeviceInfo({ device_id: deviceId });

    console.log('Device info result:', JSON.stringify(result, null, 2));

    expect(result).not.toBeNull();
    expect(result.device_id).toBe(deviceId);
    expect(result.product_name).toBe(productName);
    expect(result.device_name).toBeDefined();
    expect(result.status).toBeDefined();

    console.log(`设备名称: ${result.device_name}`);
    console.log(`产品名称: ${result.product_name}`);
    console.log(`设备状态: ${result.status}`);
  });

  it('test_add_device', async () => {
    const { controller, deviceId, productName } = createService();

    const result = await controller.IotDevice.addDevice({ project_name: productName, device_id: deviceId });
    expect(result).not.toBeNull();
    expect(result.qrcode_url).toBeDefined();
    console.log(`addDevice 调用成功: qrcode_url=${result.qrcode_url}`);
  });
});
