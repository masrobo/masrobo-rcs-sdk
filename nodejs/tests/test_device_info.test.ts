import { describe, it, expect, vi, beforeEach } from 'vitest';

// 模拟 client
const mockRequest = vi.fn();
vi.mock('../src/client', () => ({
  Client: vi.fn().mockImplementation(() => ({
    request: mockRequest,
  })),
}));

import { IotDeviceService } from '../src/iot_device';

describe('IotDeviceService.getDeviceInfo', () => {
  let service: IotDeviceService;

  beforeEach(() => {
    mockRequest.mockReset();
    // 从 Client 创建 service，由于 vi.mock 会自动注入 mock
    service = new IotDeviceService({ request: mockRequest } as any);
  });

  it('应成功获取设备信息', async () => {
    const fakeData = {
      device_id: 'test-device-001',
      product_name: 'AibbyPet',
      device_name: '测试设备',
      status: 1,
      services: { webrtc: { enabled: true } },
    };
    mockRequest.mockResolvedValue(fakeData);

    const result = await service.getDeviceInfo({ device_id: 'test-device-001' });

    expect(result).toEqual(fakeData);
    expect(result.device_id).toBe('test-device-001');
    expect(result.services.webrtc.enabled).toBe(true);

    // 验证请求参数
    expect(mockRequest).toHaveBeenCalledWith('POST', '/iot/device/info', {
      body: { device_id: 'test-device-001' },
    });
  });

  it('应返回完整字段的设备信息', async () => {
    const fakeData = {
      id: 42,
      device_id: 'device-full-001',
      iot_product_id: 15,
      product_name: 'SmartSensor',
      category_code: 'sensor',
      user_id: 888,
      device_name: '温湿度传感器 #1',
      active_type: ['MANUAL', 'API'],
      status: 1,
      active_time: '2025-06-01T10:30:00',
      deactive_time: null,
      application_id: 300,
      developer_id: 50,
      app_id: 'my-app',
      application_name: '我的应用',
      developer_name: '开发者',
      product_title: '智能传感器 Pro',
      device_data: { temperature: 25.5, humidity: 60 },
      device_data_time: '2025-06-03T12:00:00',
      screenshot: 'https://cdn.example.com/snap.jpg',
      screenshot_time: '2025-06-03T12:00:00',
      services: {
        webrtc: { enabled: false },
        ota: { enabled: true, version: '2.0.1' },
      },
      rel_role: 0,
      rel_source: 'shared',
    };
    mockRequest.mockResolvedValue(fakeData);

    const result = await service.getDeviceInfo({ device_id: 'device-full-001' });

    expect(result.device_id).toBe('device-full-001');
    expect(result.device_data.temperature).toBe(25.5);
    expect(result.services.ota.version).toBe('2.0.1');
  });

  it('device_id 为空时应抛出错误', async () => {
    await expect(service.getDeviceInfo({ device_id: '' })).rejects.toThrow();
  });

  it('device_id 缺失时应抛出错误', async () => {
    await expect(service.getDeviceInfo({})).rejects.toThrow();
  });

  it('API 返回业务错误时应抛出异常', async () => {
    mockRequest.mockRejectedValue(new Error('device not found'));

    await expect(
      service.getDeviceInfo({ device_id: 'nonexistent-device' })
    ).rejects.toThrow('device not found');
  });

  it('HTTP 401 时应抛出异常', async () => {
    mockRequest.mockRejectedValue(new Error('unauthorized'));

    await expect(
      service.getDeviceInfo({ device_id: 'test-device' })
    ).rejects.toThrow('unauthorized');
  });
});