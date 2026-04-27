import { Client } from "./client";
import { IotDeviceService } from "./iot_device";

export class RobotController extends Client {
  public IotDevice: IotDeviceService;

  constructor(config: any) {
    super(config);
    this.IotDevice = new IotDeviceService(this);
  }
}