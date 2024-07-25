#  Copyright (C) 2019-2021 Parrot Drones SAS
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the Parrot Company nor the names
#    of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  PARROT COMPANY BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#  AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  SUCH DAMAGE.


import ctypes
import datetime
import json
import olympe_deps as od
import pprint
import time

from . import messages, SKYCTRL_DEVICE_TYPE_LIST
from .backend import BackendType, CtrlBackendNet, CtrlBackendMuxIp
from .cmd_itf import CommandInterfaceBase, ConnectedEvent
from .discovery import DiscoveryNet, DiscoveryNetRaw, DiscoveryMux
from concurrent.futures import TimeoutError as FutureTimeoutError
from concurrent.futures import CancelledError
from olympe.utils import callback_decorator
from olympe.concurrent import Future
from olympe.messages import antiflicker
from olympe.messages import ardrone3
from olympe.messages import camera2
from olympe.messages import connectivity
from olympe.messages import controllerNetwork
from olympe.messages import common
from olympe.messages import developer
from olympe.messages import mission
from olympe.messages import network
from olympe.messages import pointnfly
from olympe.messages import privacy
from olympe.messages import skyctrl
from olympe.networking import (
    Connection,
    ConnectionListener
)
from olympe.video.pdraw import (PDRAW_LOCAL_STREAM_PORT, PDRAW_LOCAL_CONTROL_PORT)
from tzlocal import get_localzone
from typing import List, Optional
from warnings import warn


class PilotingCommand:
    def __init__(self, time_function=None):
        self.set_default_piloting_command()
        if time_function:
            self.time_function = time_function
        else:
            self.time_function = time.time

    def update_piloting_command(self, roll, pitch, yaw, gaz, piloting_time):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.gaz = gaz
        self.piloting_time = piloting_time
        self.initial_time = self.time_function()

    def set_default_piloting_command(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.gaz = 0
        self.piloting_time = 0
        self.initial_time = 0


class ControllerBackendConnectionListener(ConnectionListener):
    def __init__(self, controller: "ControllerBase"):
        self._controller = controller

    def disconnected(self, _: Connection):
        self._controller._thread_loop.run_later(self._controller._on_device_removed)


class ControllerBase(CommandInterfaceBase):

    DEVICE_TYPES: Optional[List[int]] = None

    def __init__(self,
                 ip_addr,
                 *,
                 name=None,
                 drone_type=0,
                 proto_v_min=1,
                 proto_v_max=3,
                 is_skyctrl=None,
                 video_buffer_queue_size=8,
                 media_autoconnect=True,
                 backend=BackendType.Net,
                 time_function=None):
        self._logger_scope = "controller"
        self._ip_addr_str = str(ip_addr)
        self._ip_addr = ip_addr.encode('utf-8')
        self._is_skyctrl = is_skyctrl
        self._piloting = False
        self._time_function = time_function

        self._piloting_command = PilotingCommand(
            time_function=self._time_function)

        self._backend_type = backend
        if backend is BackendType.Net:
            self._backend_class = CtrlBackendNet
            self._discovery_class = DiscoveryNet
        elif backend is BackendType.MuxIp:
            self._backend_class = CtrlBackendMuxIp
            self._discovery_class = DiscoveryMux
        else:
            raise ValueError(f"Unknown backend type {backend}")
        super().__init__(
            name=name,
            drone_type=drone_type,
            proto_v_min=1,
            proto_v_max=3,
            device_addr=self._ip_addr,
            connection_listener=ControllerBackendConnectionListener(self)
        )

        if self._time_function is not None:
            self._scheduler.set_time_function(self._time_function)

        self._connected_future = None
        self._last_disconnection_time = None
        # Setup piloting commands timer
        self._piloting_timer = self._thread_loop.create_timer(
            self._piloting_timer_cb)

    def is_skyctrl(self):
        if self._is_skyctrl is None:
            return self._device_type in SKYCTRL_DEVICE_TYPE_LIST
        else:
            return self._is_skyctrl

    def _recv_message_type(self):
        return messages.ArsdkMessageType.CMD

    def _create_backend(
            self,
            name,
            proto_v_min,
            proto_v_max,
            *,
            device_addr=None,
            connection_listener=None
    ):
        self._backend = self._backend_class(
            name=name,
            proto_v_min=proto_v_min,
            proto_v_max=proto_v_max,
            device_addr=device_addr,
            connection_listener=connection_listener
        )

    def _declare_callbacks(self):
        """
        Define all callbacks
        """
        super()._declare_callbacks()
        self._device_cbs_cfg = od.struct_arsdk_device_conn_cbs.bind({
            "connecting": self._connecting_cb,
            "connected": self._connected_cb,
            "disconnected": self._disconnected_cb,
            "canceled": self._canceled_cb,
            "link_status": self._link_status_cb,
        })

    @callback_decorator()
    def _create_command_interface(self):
        """
        Create a command interface to send command to the device
        """

        cmd_itf = od.POINTER_T(od.struct_arsdk_cmd_itf)()

        res = od.arsdk_device_create_cmd_itf(
            self._device.arsdk_device,
            self._cmd_itf_cbs,
            ctypes.pointer(cmd_itf))

        if res != 0:
            self.logger.error(f"Error while creating command interface: {res}")
            cmd_itf = None
        else:
            self.logger.info("Command interface has been created")

        return cmd_itf

    @callback_decorator()
    def _connecting_cb(self, _arsdk_device, arsdk_device_info, _user_data):
        """
        Notify connection initiation.
        """
        device_name = od.string_cast(arsdk_device_info.contents.name)
        self.logger.info(f"Connecting to device: {device_name}")

    @callback_decorator()
    def _connected_cb(self, _arsdk_device, arsdk_device_info, _user_data):
        if not self.connecting:
            self.logger.warning("This connection attempt has already timedout, disconnecting...")
            self._thread_loop.run_later(self._on_device_removed)
            return
        self._thread_loop.run_async(self._aconnected_cb, arsdk_device_info)

    async def _aconnected_cb(self, arsdk_device_info):
        """
        Notify connection completion.
        """
        device_name = od.string_cast(arsdk_device_info.contents.name)
        self.set_device_name(device_name)
        self.logger.info(f"Connected to device: {device_name}")
        json_info = od.string_cast(arsdk_device_info.contents.json)
        try:
            json_info = json.loads(json_info)
            self.logger.info(pprint.pformat(json_info))
        except ValueError:
            self.logger.error(f'json contents cannot be parsed: {json_info}')

        # Create the arsdk command interface
        if self._cmd_itf is None:
            self.logger.debug(f"Creating cmd_itf for {self._ip_addr_str} ...")
            self._cmd_itf = self._create_command_interface()
            if self._cmd_itf is None:
                self.logger.error(f"Creating cmd_itf for {self._ip_addr_str} failed")
                self.async_disconnect()
                if self._connect_future is not None and not self._connect_future.done():
                    self._connect_future.set_result(False)
                return

        self.connected = True
        if not await self._on_connected():
            if self._connect_future is not None and not self._connect_future.done():
                self._connect_future.set_result(False)
            return

        if self._connect_future is not None and not self._connect_future.done():
            self._connect_future.set_result(True)

    @callback_decorator()
    def _disconnected_cb(self, _arsdk_device, arsdk_device_info, _user_data):
        """
         Notify disconnection.
        """
        device_name = od.string_cast(arsdk_device_info.contents.name)
        self.logger.info(f"Disconnected from device: {device_name}")
        self.connected = False
        if self._disconnect_future is not None and not self._disconnect_future.done():
            self._disconnect_future.set_result(True)
        self._thread_loop.run_later(self._on_device_removed)

    @callback_decorator()
    def _canceled_cb(self, _arsdk_device, arsdk_device_info, reason, _user_data):
        """
        Notify connection cancellation. Either because 'disconnect' was
        called before 'connected' callback or remote aborted/rejected the
        request.
        """
        device_name = od.string_cast(arsdk_device_info.contents.name)
        reason = od.string_cast(
            od.arsdk_conn_cancel_reason_str(reason))
        self.logger.info(
            f"Connection to device: {device_name} has been canceled for reason: {reason}")
        if self._connect_future is not None and not self._connect_future.done():
            self._connect_future.set_result(False)
        self._thread_loop.run_later(self._on_device_removed)

    @callback_decorator()
    def _link_status_cb(self, _arsdk_device, _arsdk_device_info, status, _user_data):
        """
         Notify link status. At connection completion, it is assumed to be
         initially OK. If called with KO, user is responsible to take action.
         It can either wait for link to become OK again or disconnect
         immediately. In this case, call arsdk_device_disconnect and the
         'disconnected' callback will be called.
        """
        self.logger.info(f"Link status: {status}")
        # If link has been lost, we must start disconnection procedure
        if status == od.ARSDK_LINK_STATUS_KO:
            # the device has been disconnected
            self.connected = False
            self._thread_loop.run_later(self._on_device_removed)

    @callback_decorator()
    def _disconnection_impl(self):
        f = Future(self._thread_loop)
        if not self.connected:
            return f.set_result(True)

        if self._disconnect_future is not None and not self._disconnect_future.done():
            self._disconnect_future.cancel()
        self._disconnect_future = f
        if self._device is None:
            self._disconnect_future.set_result(False)
            return self._disconnect_future
        res = od.arsdk_device_disconnect(self._device.arsdk_device)
        if res != 0:
            self.logger.error(
                f"Error while disconnecting from device: {self._ip_addr} ({res})")
            self._disconnect_future.set_result(False)
        else:
            self.logger.info(
                f"disconnected from device: {self._ip_addr}")
        return self._disconnect_future

    def _synchronize_clock(self):

        date_time = datetime.datetime.now(
            get_localzone()).strftime("%Y%m%dT%H%M%S%z")
        if not self._is_skyctrl:
            current_date_time = common.Common.CurrentDateTime
        else:
            current_date_time = skyctrl.Common.CurrentDateTime
        res = self(current_date_time(datetime=date_time, _timeout=0.5))

        def _on_sync_done(res):
            if not res.success():
                msg = "Time synchronization failed for {}".format(
                    self._ip_addr)
                self.logger.warning(msg)
            else:
                self.logger.info("Synchronization of {} at {}".format(
                    self._ip_addr, date_time))

        res.add_done_callback(_on_sync_done)

    @callback_decorator()
    def _start_piloting_impl(self):
        delay = 100
        period = 25

        ok = self._thread_loop.set_timer(self._piloting_timer, delay, period)

        if ok:
            self._piloting = True
            self.logger.info(
                "Piloting interface has been correctly launched")
        else:
            self.logger.error("Unable to launch piloting interface")
        return self._piloting

    @callback_decorator()
    def _stop_piloting_impl(self):

        # Stop the drone movements
        self._piloting_command.set_default_piloting_command()
        time.sleep(0.1)

        ok = self._thread_loop.clear_timer(self._piloting_timer)
        if ok:
            # Reset piloting state value to False
            self._piloting = False
            self.logger.info("Piloting interface stopped")
        else:
            self.logger.error("Unable to stop piloting interface")

    @callback_decorator()
    def _piloting_timer_cb(self, timer, _user_data):
        self.logger.debug(f"piloting timer callback: {timer}")
        if self.connected:
            self._send_piloting_command()

    def _send_piloting_command(self):
        # When piloting time is 0 => send default piloting commands
        if self._piloting_command.piloting_time:
            # Check if piloting time since last pcmd order has been reached
            diff_time = (
                self._piloting_command.time_function() -
                self._piloting_command.initial_time
            )
            if diff_time >= self._piloting_command.piloting_time:
                self._piloting_command.set_default_piloting_command()

        # Flag to activate movement on roll and pitch. 1 activate, 0 deactivate
        if self._piloting_command.roll or (
            self._piloting_command.pitch
        ):
            activate_movement = 1
        else:
            activate_movement = 0

        self._send_command_impl(
            ardrone3.Piloting.PCMD,
            dict(
                flag=activate_movement,
                roll=self._piloting_command.roll,
                pitch=self._piloting_command.pitch,
                yaw=self._piloting_command.yaw,
                gaz=self._piloting_command.gaz,
                timestampAndSeqNum=0,
            ),
            quiet=True,
        )

    def start_piloting(self):
        """
        Start interface to send piloting commands

        :rtype: bool
        """
        if self._piloting:
            self.logger.debug("Piloting interface already started")
            return True

        f = self._thread_loop.run_async(self._start_piloting_impl)

        try:
            ok = f.result_or_cancel(timeout=2)
        except (FutureTimeoutError, CancelledError):
            self.logger.error("Unable to launch piloting interface")
            return False
        if not ok:
            self.logger.error("Unable to launch piloting interface")
            return False

        self.logger.info("Piloting started")
        return True

    def stop_piloting(self):
        """
        Stop interface to send piloting commands

        :rtype: bool
        """
        # Check piloting interface is running
        if not self._piloting:
            self.logger.debug("Piloting interface already stopped")
            return True

        f = self._thread_loop.run_async(self._stop_piloting_impl)

        try:
            ok = f.result_or_cancel(timeout=2)
        except (FutureTimeoutError, CancelledError):
            self.logger.error("Unable to stop piloting interface")
            return False
        if not ok:
            self.logger.error("Unable to stop piloting interface")
            return False

        self.logger.info("Piloting stopped")
        return True

    def piloting(self, roll, pitch, yaw, gaz, piloting_time):
        """
        Send manual piloting commands to the drone.
        This function is a non-blocking.

        :type roll: int
        :param roll: roll consign for the drone (must be in [-100:100])
        :type pitch: int
        :param pitch: pitch consign for the drone  (must be in [-100:100])
        :type yaw: int
        :param yaw: yaw consign for the drone  (must be in [-100:100])
        :type gaz: int
        :param gaz: gaz consign for the drone  (must be in [-100:100])
        :type piloting_time: float
        :param piloting_time: The time of the piloting command
        :rtype: bool

        """
        if not self.start_piloting():
            return False
        self._piloting_command.update_piloting_command(roll, pitch, yaw, gaz, piloting_time)
        return True

    def piloting_pcmd(self, roll, pitch, yaw, gaz, piloting_time):
        warn(
            "ControllerBase.piloting_pcmd is deprecated, "
            "please use ControllerBase.piloting instead",
            DeprecationWarning
        )
        return self.piloting(roll, pitch, yaw, gaz, piloting_time)

    async def _async_discover_device(self, deadline):
        # Try to identify the device type we are attempting to connect to...
        await self._backend.ready()
        timeout = (deadline - time.time()) / 2
        discovery = self._discovery_class(
            self._backend,
            ip_addr=self._ip_addr,
            devices_types=self.DEVICE_TYPES,
            timeout=timeout
        )
        device = await discovery.async_get_device()
        if device is not None:
            return device, discovery
        await discovery.async_stop()
        if self._backend_type is BackendType.Net:
            self.logger.warning(f"Net discovery failed for {self._ip_addr}")
            self.logger.warning(f"Trying 'NetRaw' discovery for {self._ip_addr} ...")
            assert await discovery.async_stop()
            timeout = (deadline - time.time()) / 4
            discovery = DiscoveryNetRaw(self._backend, ip_addr=self._ip_addr, timeout=timeout)
            device = await discovery.async_get_device()
            if device is None:
                await discovery.async_stop()
        return device, discovery

    async def _async_get_device(self, deadline):
        if self._device is not None:
            return True
        device, discovery = await self._async_discover_device(deadline)

        if device is None:
            self.logger.info(f"Unable to discover the device: {self._ip_addr}")
            return False

        # Save device related info
        self._device = device
        self._discovery = discovery
        self._device_type = self._device.type
        if self._is_skyctrl is None:
            if self._device_type in SKYCTRL_DEVICE_TYPE_LIST:
                self._is_skyctrl = True
            else:
                self._is_skyctrl = False
        return True

    @callback_decorator()
    def _connect_impl(self, deadline):
        self._connection_deadline = deadline
        # Use default values for connection json. If we want to changes values
        # (or add new info), we just need to add them in req (using json format)
        # For instance:
        req = bytes('{{ "{}": "{}", "{}": "{}", "{}": "{}"}}'.format(
            "arstream2_client_stream_port", PDRAW_LOCAL_STREAM_PORT,
            "arstream2_client_control_port", PDRAW_LOCAL_CONTROL_PORT,
            "arstream2_supported_metadata_version", "1"), 'utf-8')
        device_id = b""

        device_conn_cfg = od.struct_arsdk_device_conn_cfg(
            ctypes.create_string_buffer(b"olympe"), ctypes.create_string_buffer(b"desktop"),
            ctypes.create_string_buffer(bytes(device_id)), ctypes.create_string_buffer(req))

        # Send connection command
        if self._connect_future is not None and not self._connect_future.done():
            self._connect_future.cancel()
        self._connect_future = Future(self._thread_loop)
        res = od.arsdk_device_connect(
            self._device.arsdk_device,
            device_conn_cfg,
            self._device_cbs_cfg,
            self._thread_loop.pomp_loop
        )
        if res != 0:
            self.logger.error(f"Error while connecting: {res}")
            self._connect_future.set_result(False)
        else:
            self.logger.info("Connection in progress...")
        return self._connect_future

    async def _do_connect(self, timeout, retry):
        self.connecting = True
        try:
            grace_period = 5.
            if self._last_disconnection_time is not None:
                last_disconnection = (time.time() - self._last_disconnection_time)
                if last_disconnection < grace_period:
                    await self._thread_loop.asleep(grace_period - last_disconnection)
            # the deadline does not include the grace period
            backoff = 2.

            for i in range(retry):
                deadline = time.time() + timeout
                self.connecting = True
                if self.connected:
                    # previous connection attempt timedout but we're connected..
                    break
                if deadline < time.time():
                    self.logger.error(f"'{self._ip_addr_str}' connection timed out {i + 1}/{retry}")
                    await self._thread_loop.asleep(backoff)
                    backoff *= 2.
                    continue
                try:
                    self.logger.debug(f"Discovering device {self._ip_addr_str} ...")
                    if not await self._async_get_device(deadline):
                        self.logger.debug(f"Discovering device {self._ip_addr_str} failed")
                        if deadline < (time.time() + backoff):
                            self.logger.error(
                                f"'{self._ip_addr_str} connection (would) have timed out"
                            )
                            return False
                        await self._thread_loop.asleep(backoff)
                        backoff *= 2.
                        continue

                    self.logger.debug(f"Connecting device {self._ip_addr_str} ...")
                    self.connecting = True
                    connected = await self._connect_impl(deadline)
                except (FutureTimeoutError, CancelledError):
                    await self._thread_loop.asleep(backoff)
                    backoff *= 2.
                    continue
                if not connected:
                    self.logger.debug(f"Connecting device {self._ip_addr_str} failed")
                    await self._thread_loop.asleep(backoff)
                    backoff *= 2.
                    continue

                # We're connected
                break
            else:
                if self._discovery:
                    await self._discovery.async_stop()
                self.logger.error(f"'{self._ip_addr_str} connection retries failed")
                return False
        except (FutureTimeoutError, CancelledError):
            if self._discovery:
                await self._discovery.async_stop()
            self.logger.error(f"'{self._ip_addr_str} connection retries failed")
            return False
        finally:
            self.connecting = False

        return self.connected

    async def _send_states_settings_cmd(self, command):
        res = await self(command)
        if not res.success():
            self.logger.error(
                f"Unable get device state/settings: {command} "
                f"for {self._ip_addr}")
            self.async_disconnect()
            return False
        return True

    async def _on_connected(self):
        if not self._ip_addr_str.startswith("10.202") and (
                not self._ip_addr_str.startswith("127.0")):
            self._synchronize_clock()
        # We're connected to the device, get all device states and settings if necessary
        get_state_commands = []
        if not self._is_skyctrl:
            all_states_settings_commands = [
                common.Common.AllStates(), common.Settings.AllSettings()
            ]
            if self._device_type not in (
                    od.ARSDK_DEVICE_TYPE_ANAFI4K,
                    od.ARSDK_DEVICE_TYPE_ANAFI_THERMAL,
                    od.ARSDK_DEVICE_TYPE_ANAFI_UA,
                    od.ARSDK_DEVICE_TYPE_ANAFI_USA
            ):
                get_state_commands = [
                    antiflicker.Command.GetState(include_default_capabilities=True),
                    camera2.Command.GetState(include_default_capabilities=True),
                    connectivity.Command.GetState(include_default_capabilities=True),
                    developer.Command.GetState(),
                    network.Command.GetState(include_default_capabilities=True),
                    pointnfly.Command.GetState(include_default_capabilities=True),
                    privacy.Command.GetState(include_default_capabilities=True),
                    mission.custom_msg_enable()
                ]
        else:
            all_states_settings_commands = [
                skyctrl.Common.AllStates(),
                skyctrl.Settings.AllSettings(),
            ]
            if self._device_type not in [
                od.ARSDK_DEVICE_TYPE_SKYCTRL,
                od.ARSDK_DEVICE_TYPE_SKYCTRL_NG,
                od.ARSDK_DEVICE_TYPE_SKYCTRL_2,
                od.ARSDK_DEVICE_TYPE_SKYCTRL_2P,
                od.ARSDK_DEVICE_TYPE_SKYCTRL_3,
                od.ARSDK_DEVICE_TYPE_SKYCTRL_UA,
            ]:
                get_state_commands = [controllerNetwork.Command.GetState()]
        # Get device specific states and settings
        for states_settings_command in all_states_settings_commands:
            timeout = self._connection_deadline - time.time()
            try:
                res = await self._thread_loop.await_for(
                    timeout,
                    self._send_states_settings_cmd, states_settings_command
                )
            except FutureTimeoutError:
                return False
            if not res:
                return False

        # Get specific optional states
        for state_command in get_state_commands:
            timeout = self._connection_deadline - time.time() - 0.1
            if timeout < 0.0:
                # There is no time wait for optional states
                self._thread_loop.run_async(self._send_states_settings_cmd, state_command)
                continue
            try:
                res = await self._thread_loop.await_for(
                    timeout,
                    self._send_states_settings_cmd, state_command
                )
            except FutureTimeoutError:
                # Protobuf Command.GetState are optional
                continue
            if not res:
                return False

        # Process the ConnectedEvent
        event = ConnectedEvent()
        self.logger.info(str(event))
        self._scheduler.process_event(event)
        return True

    def async_connect(self, *, timeout=None, later=False, retry=1):
        if timeout is None:
            timeout = 6.0

        # If not already connected to a device
        if self.connected:
            f = Future(self._thread_loop)
            f.set_result(True)
            return f

        if self._connected_future is None:
            if not later:
                self._connected_future = self._thread_loop.run_async(
                    self._do_connect, timeout, retry)
            else:
                self._connected_future = self._thread_loop.run_later(
                    self._do_connect, timeout, retry)

        def _on_connect_done(f):
            self._connected_future = None
        self._connected_future.add_done_callback(_on_connect_done)

        return self._connected_future

    def connect(self, *, timeout=None, retry=1):
        """
        Make all step to make the connection between the device and the controller

        :param timeout: the global connection timeout in seconds  (including the
         retried connection attempt duration when `retry` > 1)
        :param retry: the number of connection attempts (default to `1`)

        :rtype: bool
        """

        if timeout is None:
            timeout = 6.0
        connected_future = self.async_connect(timeout=timeout, retry=retry)
        try:
            connected_future.result_or_cancel(timeout=(timeout * retry))
        except (FutureTimeoutError, CancelledError):
            self.logger.error(f"'{self._ip_addr_str}' connection timed out")
            # If the connection timedout we must disconnect
            self.disconnect()

        return self.connected

    @callback_decorator()
    def _on_device_removed(self):
        if self._discovery:
            self._discovery.async_stop()
        if self._piloting:
            self._stop_piloting_impl()
        self._disconnection_impl()
        self._last_disconnection_time = time.time()
        self._piloting_command = PilotingCommand(time_function=self._time_function)
        super()._on_device_removed()

    def _reset_instance(self):
        self._piloting = False
        self._piloting_command = PilotingCommand(time_function=self._time_function)
        self._device = None
        self._device_name = None
        self._discovery = None
        self._connected_future = None
        super()._reset_instance()
