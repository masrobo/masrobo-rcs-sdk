import { Client } from './client';

export declare class IotDeviceService {
    private client;
    constructor(client: Client);
    getLatestDeviceData(request?: any): Promise<any>;
    sendDeviceCommand(request?: any): Promise<void>;
    bindDevice(request?: any): Promise<void>;
    setting(request?: any): Promise<void>;
}
export declare class RobotController extends Client {
    IotDevice: IotDeviceService;
    constructor(config: any);
}
