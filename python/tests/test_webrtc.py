import argparse
import asyncio
import json
import logging
import os
import ssl
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None
from aiortc import (
    RTCConfiguration,
    RTCIceCandidate,
    RTCIceServer,
    RTCPeerConnection,
    RTCSessionDescription,
)
from aiortc.contrib.media import MediaBlackhole
from aiortc.sdp import candidate_from_sdp, candidate_to_sdp
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MasRobo RCS WebRTC MQTT test client")
    parser.add_argument("--mqtt-url", help="MQTT broker URL, e.g. mqtts://masnode.com:8883")
    parser.add_argument("--mqtt-username", help="MQTT username")
    parser.add_argument("--mqtt-password", help="MQTT password")
    parser.add_argument("--app-id", help="RCS App ID")
    parser.add_argument("--device-id", help="Target device ID")
    parser.add_argument("--signal-channel", help="camera_id or audio_id")
    parser.add_argument("--signal-topic", help="Override signaling topic")
    parser.add_argument("--client-id", help="Client ID used in signaling")
    parser.add_argument("--room-id", help="Optional room ID")
    parser.add_argument("--join-payload", help="Extra JSON merged into joinRoom payload")
    parser.add_argument("--stun-url", help="STUN URL")
    parser.add_argument("--turn-url", help="TURN URL")
    parser.add_argument("--turn-username", help="TURN username")
    parser.add_argument("--turn-password", help="TURN password")
    parser.add_argument("--send-offer", action="store_true", help="Create and publish a local offer after joinRoom")
    parser.add_argument("--send-offer-delay", type=float, help="Seconds to wait after joinRoom before sending a local offer")
    parser.add_argument("--show-video", action="store_true", help="Show remote video in a local window")
    parser.add_argument("--timeout", type=int, default=90, help="Seconds to wait before exiting")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def parse_json(value: str, field_name: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{field_name} must decode to a JSON object")
    return parsed


def build_topic(app_id: str, device_id: str, signal_channel: str) -> str:
    return f"/device/rtc/{app_id}/{device_id}/{signal_channel}"


def load_config(args: argparse.Namespace) -> Dict[str, Any]:
    load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

    client_id = (
        args.client_id
        or os.environ.get("WEBRTC_CLIENT_ID")
        or f"webrtc-client-{uuid.uuid4().hex[:12]}"
    )
    join_payload_raw = args.join_payload or os.environ.get("WEBRTC_JOIN_PAYLOAD", "{}")
    join_payload = parse_json(join_payload_raw, "WEBRTC_JOIN_PAYLOAD")

    config = {
        "mqtt_url": args.mqtt_url or os.environ.get("MQTT_URL"),
        "mqtt_username": args.mqtt_username or os.environ.get("MQTT_USERNAME"),
        "mqtt_password": args.mqtt_password or os.environ.get("MQTT_PASSWORD"),
        "app_id": args.app_id or os.environ.get("WEBRTC_APP_ID") or os.environ.get("APP_ID"),
        "device_id": args.device_id or os.environ.get("WEBRTC_DEVICE_ID") or os.environ.get("DEVICE_ID"),
        "signal_channel": args.signal_channel or os.environ.get("WEBRTC_SIGNAL_CHANNEL", "camera_id"),
        "signal_topic": args.signal_topic or os.environ.get("WEBRTC_SIGNAL_TOPIC"),
        "client_id": client_id,
        "room_id": args.room_id or os.environ.get("WEBRTC_ROOM_ID") or client_id,
        "join_payload": join_payload,
        "stun_url": args.stun_url or os.environ.get("WEBRTC_STUN_URL"),
        "turn_url": args.turn_url or os.environ.get("WEBRTC_TURN_URL"),
        "turn_username": args.turn_username or os.environ.get("WEBRTC_TURN_USERNAME"),
        "turn_password": args.turn_password or os.environ.get("WEBRTC_TURN_PASSWORD"),
        "send_offer": args.send_offer or os.environ.get("WEBRTC_SEND_OFFER", "0") == "1",
        "send_offer_delay": float(args.send_offer_delay or os.environ.get("WEBRTC_SEND_OFFER_DELAY", "1.0")),
        "show_video": args.show_video or os.environ.get("WEBRTC_SHOW_VIDEO", "1") == "1",
        "timeout": args.timeout,
    }

    if not config["signal_topic"]:
        config["signal_topic"] = build_topic(
            config["app_id"],
            config["device_id"],
            config["signal_channel"],
        )

    required = [
        "mqtt_url",
        "mqtt_username",
        "mqtt_password",
        "app_id",
        "device_id",
        "stun_url",
        "turn_url",
        "turn_username",
        "turn_password",
    ]
    missing = [name for name in required if not config.get(name)]
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")

    return config


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        parsed = json.loads(payload)
        if isinstance(parsed, dict):
            return parsed
    raise ValueError(f"Unsupported payload format: {payload!r}")


def candidate_from_payload(payload: Dict[str, Any]) -> RTCIceCandidate:
    candidate = candidate_from_sdp(payload["candidate"])
    candidate.sdpMid = payload.get("sdpMid")
    candidate.sdpMLineIndex = payload.get("sdpMLineIndex")
    return candidate


class MqttSignaling:
    def __init__(self, config: Dict[str, Any], loop: asyncio.AbstractEventLoop) -> None:
        self.config = config
        self.loop = loop
        self.queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()
        self.connected = asyncio.Event()
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=config["client_id"],
            protocol=mqtt.MQTTv311,
        )
        self.client.username_pw_set(config["mqtt_username"], config["mqtt_password"])
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        parsed = urlparse(config["mqtt_url"])
        self.host = parsed.hostname
        self.port = parsed.port or (8883 if parsed.scheme == "mqtts" else 1883)
        self.use_tls = parsed.scheme == "mqtts"

        if not self.host:
            raise ValueError(f"Invalid MQTT URL: {config['mqtt_url']}")

        if self.use_tls:
            self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Any, reason_code: Any, properties: Any) -> None:
        logger.info("MQTT connected: %s", reason_code)
        client.subscribe(self.config["signal_topic"], qos=1)
        self.loop.call_soon_threadsafe(self.connected.set)

    def on_disconnect(self, client: mqtt.Client, userdata: Any, disconnect_flags: Any, reason_code: Any, properties: Any) -> None:
        logger.info("MQTT disconnected: %s", reason_code)

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        try:
            raw_payload = msg.payload.decode("utf-8")
            logger.info("MQTT received raw topic=%s payload=%s", msg.topic, raw_payload)
            payload = json.loads(raw_payload)
            payload["_topic"] = msg.topic
            self.loop.call_soon_threadsafe(self.queue.put_nowait, payload)
        except Exception:
            logger.exception("Failed to decode MQTT message: %r", msg.payload)

    async def connect(self) -> None:
        self.client.connect(self.host, self.port, keepalive=60)
        self.client.loop_start()
        await asyncio.wait_for(self.connected.wait(), timeout=15)

    async def publish(self, message_type: str, payload: Dict[str, Any]) -> None:
        body = json.dumps({"type": message_type, "payload": payload}, ensure_ascii=False)
        logger.info("MQTT publish payload: %s", body)
        info = self.client.publish(self.config["signal_topic"], body, qos=1)
        await asyncio.to_thread(info.wait_for_publish)
        logger.info("Published %s to %s", message_type, self.config["signal_topic"])

    async def receive(self) -> Dict[str, Any]:
        return await self.queue.get()

    async def close(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()


class WebRtcClient:
    def __init__(self, config: Dict[str, Any], signaling: MqttSignaling) -> None:
        self.config = config
        self.signaling = signaling
        self.media_sink = MediaBlackhole()
        self.video_tasks: set[asyncio.Task[Any]] = set()
        self.received_offer = False
        self.received_answer = False
        self.received_remote_track = False
        self.window_name = f"MasRobo WebRTC - {config['device_id']}"
        self.pc = RTCPeerConnection(
            RTCConfiguration(
                iceServers=[
                    RTCIceServer(urls=[config["stun_url"]]),
                    RTCIceServer(
                        urls=[config["turn_url"]],
                        username=config["turn_username"],
                        credential=config["turn_password"],
                    ),
                ]
            )
        )
        self._wire_events()

    def _wire_events(self) -> None:
        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange() -> None:
            logger.info("ICE state: %s", self.pc.iceConnectionState)

        @self.pc.on("connectionstatechange")
        async def on_connectionstatechange() -> None:
            logger.info("Peer state: %s", self.pc.connectionState)

        @self.pc.on("track")
        def on_track(track: Any) -> None:
            logger.info("Received track: kind=%s id=%s", track.kind, track.id)
            self.received_remote_track = True
            if track.kind == "video" and self.config["show_video"]:
                task = asyncio.create_task(self._render_video(track))
                self.video_tasks.add(task)
                task.add_done_callback(self.video_tasks.discard)
            else:
                self.media_sink.addTrack(track)

        @self.pc.on("icecandidate")
        async def on_icecandidate(candidate: Optional[RTCIceCandidate]) -> None:
            if candidate is None:
                return
            await self.signaling.publish(
                "candidate",
                {
                    "candidate": candidate_to_sdp(candidate),
                    "sdpMid": candidate.sdpMid,
                    "sdpMLineIndex": candidate.sdpMLineIndex,
                    "clientId": self.config["client_id"],
                    "roomId": self.config["room_id"],
                    "deviceId": self.config["device_id"],
                },
            )

    async def start(self) -> None:
        if self.config["signal_channel"] == "audio_id":
            self.pc.addTransceiver("audio", direction="recvonly")
        else:
            self.pc.addTransceiver("video", direction="recvonly")
            self.pc.addTransceiver("audio", direction="recvonly")
        if self.config["show_video"]:
            self._show_waiting_window("Waiting for remote video...")
        if not self.config["show_video"] or cv2 is None:
            await self.media_sink.start()

    async def send_join(self) -> None:
        payload = {
            "appId": self.config["app_id"],
            "deviceId": self.config["device_id"],
            "channel": self.config["signal_channel"],
            "clientId": self.config["client_id"],
            "roomId": self.config["room_id"],
        }
        payload.update(self.config["join_payload"])
        await self.signaling.publish("joinRoom", payload)

    async def send_offer(self) -> None:
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        await self.signaling.publish(
            "offer",
            {
                "sdp": self.pc.localDescription.sdp,
                "type": self.pc.localDescription.type,
                "clientId": self.config["client_id"],
                "roomId": self.config["room_id"],
                "deviceId": self.config["device_id"],
            },
        )

    async def handle_message(self, message: Dict[str, Any]) -> None:
        message_type = message.get("type")
        payload = normalize_payload(message.get("payload", {}))
        logger.info("Received signaling message: %s", message_type)

        if payload.get("clientId") == self.config["client_id"] and message_type != "offer":
            logger.debug("Ignoring looped-back self message")
            return

        if message_type == "offer":
            self.received_offer = True
            logger.info("Applying remote offer payload: %s", json.dumps(payload, ensure_ascii=False))
            description = RTCSessionDescription(sdp=payload["sdp"], type=payload.get("type", "offer"))
            await self.pc.setRemoteDescription(description)
            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)
            await self.signaling.publish(
                "answer",
                {
                    "sdp": self.pc.localDescription.sdp,
                    "type": self.pc.localDescription.type,
                    "clientId": self.config["client_id"],
                    "roomId": self.config["room_id"],
                    "deviceId": self.config["device_id"],
                },
            )
            return

        if message_type == "answer":
            self.received_answer = True
            logger.info("Applying remote answer payload: %s", json.dumps(payload, ensure_ascii=False))
            description = RTCSessionDescription(sdp=payload["sdp"], type=payload.get("type", "answer"))
            await self.pc.setRemoteDescription(description)
            return

        if message_type == "candidate":
            logger.info("Applying remote candidate payload: %s", json.dumps(payload, ensure_ascii=False))
            await self.pc.addIceCandidate(candidate_from_payload(payload))
            return

        if message_type in {"joinRoom", "joined", "ready", "ping", "pong"}:
            return

        logger.warning("Unhandled signaling message: %s", message)

    async def _render_video(self, track: Any) -> None:
        if cv2 is None:
            logger.warning("OpenCV is not installed, cannot open video window")
            self.media_sink.addTrack(track)
            return

        logger.info("Opening video window: %s", self.window_name)
        self._ensure_window()

        try:
            while True:
                frame = await track.recv()
                image = frame.to_ndarray(format="bgr24")
                cv2.imshow(self.window_name, image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    logger.info("Video window closed by user")
                    break
        except Exception as exc:
            logger.info("Video render loop ended: %s", exc)
        finally:
            self._destroy_window()

    def _ensure_window(self) -> None:
        if cv2 is None:
            return
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def _show_waiting_window(self, message: str) -> None:
        if cv2 is None or np is None:
            logger.warning("OpenCV or numpy is not installed, cannot open waiting video window")
            return
        self._ensure_window()
        canvas = np.zeros((540, 960, 3), dtype=np.uint8)
        cv2.putText(canvas, "MasRobo WebRTC", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 3)
        cv2.putText(canvas, message, (40, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 220, 255), 2)
        cv2.putText(canvas, "Press q in this window to close it", (40, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (180, 180, 180), 2)
        cv2.imshow(self.window_name, canvas)
        cv2.waitKey(1)

    def _destroy_window(self) -> None:
        if cv2 is None:
            return
        try:
            cv2.destroyWindow(self.window_name)
        except Exception:
            pass

    def log_summary(self) -> None:
        if not self.received_offer and not self.received_answer and not self.received_remote_track:
            if self.config["show_video"]:
                self._show_waiting_window("No remote signaling received after joinRoom")
            logger.warning(
                "No remote WebRTC signaling received after joinRoom. "
                "Only MQTT connect and local join were observed."
            )
        elif not self.received_remote_track:
            if self.config["show_video"]:
                self._show_waiting_window("Signaling received, but no remote video track")
            logger.warning("WebRTC signaling arrived, but no remote media track was received")

    async def close(self) -> None:
        for task in list(self.video_tasks):
            task.cancel()
        if self.video_tasks:
            await asyncio.gather(*self.video_tasks, return_exceptions=True)
        if not self.config["show_video"] or cv2 is None:
            await self.media_sink.stop()
        await self.pc.close()


async def run() -> None:
    args = parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    config = load_config(args)
    logger.info("Using signaling topic: %s", config["signal_topic"])

    loop = asyncio.get_running_loop()
    signaling = MqttSignaling(config, loop)
    webrtc = WebRtcClient(config, signaling)

    try:
        await signaling.connect()
        await webrtc.start()
        await webrtc.send_join()

        if config["send_offer"]:
            logger.info(
                "send_offer enabled, waiting %.2f seconds before creating local offer",
                config["send_offer_delay"],
            )
            await asyncio.sleep(config["send_offer_delay"])
            await webrtc.send_offer()

        deadline = loop.time() + config["timeout"]
        while loop.time() < deadline:
            remaining = max(1, int(deadline - loop.time()))
            message = await asyncio.wait_for(signaling.receive(), timeout=remaining)
            await webrtc.handle_message(message)
    except asyncio.TimeoutError:
        webrtc.log_summary()
        raise
    finally:
        await webrtc.close()
        await signaling.close()


def main() -> None:
    try:
        asyncio.run(run())
    except asyncio.TimeoutError:
        logger.info("Timed out waiting for signaling messages")
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as exc:
        logger.exception("WebRTC test client failed: %s", exc)
        raise


if __name__ == "__main__":
    main()
