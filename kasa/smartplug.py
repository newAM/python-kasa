"""Module for plugs."""
import logging
from typing import Any, Dict

from kasa.smartdevice import DeviceType, SmartDevice, requires_update

_LOGGER = logging.getLogger(__name__)


class SmartPlug(SmartDevice):
    """Representation of a TP-Link Smart Switch.

    Usage example when used a a synchronous library:
    ```python
    p = SmartPlug("192.168.1.105")

    # print the devices alias
    print(p.alias)

    # change state of plug
    await p.turn_on()
    await p.turn_off()

    # query and print current state of plug
    print(p.state_information)
    ```

    Errors reported by the device are raised as SmartDeviceExceptions,
    and should be handled by the user of the library.
    """

    def __init__(self, host: str) -> None:
        super().__init__(host)
        self.emeter_type = "emeter"
        self._device_type = DeviceType.Plug

    @property  # type: ignore
    @requires_update
    def is_on(self) -> bool:
        """Return whether device is on.

        :return: True if device is on, False otherwise
        """
        sys_info = self.sys_info
        return bool(sys_info["relay_state"])

    async def turn_on(self):
        """Turn the switch on.

        :raises SmartDeviceException: on error
        """
        await self._query_helper("system", "set_relay_state", {"state": 1})
        await self.update()

    async def turn_off(self):
        """Turn the switch off.

        :raises SmartDeviceException: on error
        """
        await self._query_helper("system", "set_relay_state", {"state": 0})
        await self.update()

    @property  # type: ignore
    @requires_update
    def led(self) -> bool:
        """Return the state of the led.

        :return: True if led is on, False otherwise
        :rtype: bool
        """
        sys_info = self.sys_info
        return bool(1 - sys_info["led_off"])

    async def set_led(self, state: bool):
        """Set the state of the led (night mode).

        :param bool state: True to set led on, False to set led off
        :raises SmartDeviceException: on error
        """
        await self._query_helper("system", "set_led_off", {"off": int(not state)})
        await self.update()

    @property  # type: ignore
    @requires_update
    def state_information(self) -> Dict[str, Any]:
        """Return switch-specific state information.

        :return: Switch information dict, keys in user-presentable form.
        :rtype: dict
        """
        info = {"LED state": self.led, "On since": self.on_since}
        return info
