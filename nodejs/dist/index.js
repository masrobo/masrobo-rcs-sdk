var s = Object.defineProperty;
var d = (e, t, i) => t in e ? s(e, t, { enumerable: !0, configurable: !0, writable: !0, value: i }) : e[t] = i;
var o = (e, t, i) => d(e, typeof t != "symbol" ? t + "" : t, i);
import l from "axios";
function p({ baseURL: e, token: t, httpClient: i } = {}) {
  if (!e || !String(e).trim())
    throw new Error("baseURL is required");
  if (!t || !String(t).trim())
    throw new Error("token is required");
  return {
    baseURL: String(e).trim().replace(/\/+$/, ""),
    token: String(t).trim(),
    httpClient: i || l.create({ timeout: 3e4 })
  };
}
class u extends Error {
  constructor(i, n, c, a) {
    super(n ? `open api error: status=${i} code=${n} message=${c}` : `open api error: status=${i} message=${c}`);
    o(this, "statusCode");
    o(this, "code");
    o(this, "rawBody");
    this.name = "APIError", this.statusCode = i, this.code = n, this.rawBody = a;
  }
}
function m(e) {
  return e ?? null;
}
function h(e, t, i) {
  const n = t || {};
  return new u(
    e,
    n.code || 0,
    n.msg || "request failed",
    i
  );
}
class v {
  constructor(t = {}) {
    o(this, "baseURL");
    o(this, "token");
    o(this, "httpClient");
    const i = p(t);
    this.baseURL = i.baseURL, this.token = i.token, this.httpClient = i.httpClient;
  }
  async request(t, i, { query: n, body: c } = {}) {
    const a = await this.httpClient.request({
      method: t,
      url: `${this.baseURL}/${String(i).replace(/^\/+/, "")}`,
      params: n,
      data: c,
      headers: {
        Accept: "application/json",
        "X-Token": this.token,
        ...c ? { "Content-Type": "application/json" } : {}
      },
      validateStatus: () => !0
    });
    if (a.status >= 400 || (a.data || {}).code !== 200)
      throw h(a.status, a.data, a.data);
    return m((a.data || {}).data);
  }
}
function r(e, t) {
  if (e == null)
    throw new Error(`${t} is required`);
  if (typeof e == "string" && !e.trim())
    throw new Error(`${t} is required`);
}
function _(e) {
  return e ?? null;
}
class w {
  constructor(t) {
    this.client = t;
  }
  async getLatestDeviceData(t = {}) {
    r(t.product_name, "product_name"), r(t.device_id, "device_id"), r(t.topic_name, "topic_name");
    const i = await this.client.request("GET", "/iot/device/data", { query: t });
    return _(i);
  }
  async sendDeviceCommand(t = {}) {
    r(t.command, "command"), r(t.parameter, "parameter"), r(t.device_id, "device_id"), r(t.product_name, "product_name"), r(t.topic_name, "topic_name"), await this.client.request("POST", "/iot/device/command", { body: t });
  }
  async bindDevice(t = {}) {
    r(t.device_id, "device_id"), await this.client.request("POST", "/iot/device/bind", { body: t });
  }
  async setting(t = {}) {
    r(t.device_id, "device_id"), r(t.temperature, "temperature"), r(t.humidity, "humidity"), r(t.alert_interval, "alert_interval"), r(t.alert_battery, "alert_battery"), await this.client.request("POST", "/iot/device/setting", { body: t });
  }
}
class g extends v {
  constructor(i) {
    super(i);
    o(this, "IotDevice");
    this.IotDevice = new w(this);
  }
}
const D = "device_data", S = "screenshot", b = "remote_control";
export {
  u as APIError,
  w as IotDeviceService,
  g as RobotController,
  D as TopicDeviceData,
  b as TopicRemoteControl,
  S as TopicScreenshot
};
