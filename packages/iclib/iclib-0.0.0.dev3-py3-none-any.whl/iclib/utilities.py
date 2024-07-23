"""This module implements various utilities."""

from collections.abc import Callable
from collections import deque
from dataclasses import dataclass, field
from threading import Event, Lock, Thread
from time import time

from periphery import GPIO


def bit_getter(index: int) -> Callable[[int], bool]:
    return lambda value: bool(value & (1 << index))


def twos_complement(value: int, bit_count: int) -> int:
    if value & (1 << (bit_count - 1)):
        value -= (1 << bit_count)

    return value


def lsb_bits_to_byte(*bits: bool) -> int:
    byte = 0

    for i, bit in enumerate(bits):
        byte |= bit << i

    return byte


def msb_bits_to_byte(*bits: bool) -> int:
    byte = 0

    for bit in bits:
        byte <<= 1
        byte |= bit

    return byte


@dataclass
class FrequencyMonitor:
    gpio: GPIO
    sample_count: int = field(default=5)
    poll_timeout: float = field(default=1)
    _lock: Lock = field(init=False, default_factory=Lock)
    _frequency: float = field(init=False, default=0)
    _stoppage: Event = field(init=False, default_factory=Event)
    _thread: Thread = field(init=False)

    def __post_init__(self) -> None:
        self._thread = Thread(target=self._monitor, daemon=True)

        self._thread.run()

    def _monitor(self) -> None:
        timestamps = deque[float](maxlen=self.sample_count)

        while not self._stoppage.is_set():
            if self.gpio.poll(self.poll_timeout):
                timestamps.append(time())

                if len(timestamps) > 1:
                    self.frequency = (
                        (len(timestamps) - 1)
                        / (timestamps[-1] - timestamps[0])
                    )

    @property
    def frequency(self) -> float:
        with self._lock:
            return self._frequency

    @frequency.setter
    def frequency(self, value: float) -> None:
        with self._lock:
            self._frequency = value

    def stop(self) -> None:
        self._stoppage.set()
        self._thread.join()
