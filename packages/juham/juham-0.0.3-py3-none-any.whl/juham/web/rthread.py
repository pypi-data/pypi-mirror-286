import json
from threading import Thread, Event
from typing import Any
from juham.base import Base, Object


class IWorkerThread(Thread, Object):
    """Base class for Juham threads used for tasks such as data acquisition
    that need to be run asynchronously. This class defines the `update()`
    method, in which subclasses can execute their specific code. The
    `update_interval()` method (default is 60 seconds) determines how
    frequently the `update()` method is called.

    An alternative to threads is to use cron. However, the advantage of using threads is that they run in the same
    memory space, unlike cron, which spawns a separate process and Python instance to execute the code.

    Args:
        Thread (client): MQTT client for the thread
    """

    event_topic: str = ""

    def __init__(self, client=None):
        super().__init__()
        self.mqtt_client = client
        self.stay = True
        self.name = "unnamed thread"
        self.event_topic = ""
        self._stop_event = Event()

    def stop(self) -> None:
        """Request the thread to stop processing further tasks.

        Note that the method does not wait the thread to terminate.  If
        the thread is sleeping, it will be awakened and stopped. If the
        thread is in the middle of its code execution, it will finish
        its current job before stopping.  In oder to wait until the
        thread has completed its call join() method.
        """
        self._stop_event.set()

    def run(self) -> None:
        """Thread  loop.

        Calls update() method in a loop and if the return value is True
        sleeps the update_interval() number of seconds before the next
        update call. If the update method returns False then the error
        is logged, and the sleep time is shortened to 5 seconds to
        retry. After three subsequent failures the update_interval is
        reset to original
        """
        self.debug(
            f"Thread {self.name} started with update interval {self.update_interval()}"
        )
        failures: int = 0
        updates: int = 0
        while not self._stop_event.is_set():
            if not self.update():
                seconds: float = 5
                failures = failures + 1
                self.error(
                    f"Thread {self.name} update {str(updates)} failure {str(failures)}, retry after {str(seconds)} ..."
                )
                if failures > 3:
                    failures = 0
                    seconds = self.update_interval()
            else:
                seconds = self.update_interval()
            updates = updates + 1
            self._stop_event.wait(seconds)
        self.debug(f"Thread {self.name} stopped")
        self.mqtt_client = None

    def update_interval(self) -> float:
        """Fetch the update interval in seconds. The default is 60.

        Returns:
            float: number of seconds
        """
        return 60.0

    def update(self) -> bool:
        """Method called from the threads run loop.

        Up to the sub classes to implement.

        Returns:
            bool: True upon succesfull update. False implies an error .
        """
        return True

    def log(self, type: str, msg: str, details: str) -> None:
        """Log event to event log.

        Args:
            type (str): one of the following: "info", "debug", "warning", "error"
            msg (str): message to be logged
            details (str): detailed description
        """
        if self.mqtt_client is not None:
            data = {"type": type, "msg": msg, "details": details}
            msg = json.dumps(data)
            self.mqtt_client.publish(self.event_topic, msg, qos=1, retain=True)

    def error(self, msg, details=""):
        self.log("Error", msg, details)

    def warning(self, msg, details=""):
        self.log("Warning", msg, details)

    def info(self, msg, details=""):
        self.log("Info", msg, details)

    def debug(self, msg, details=""):
        self.log("Debug", msg, details)

    @classmethod
    def register(cls):
        # nothing to do here
        pass


class RThread(Base):

    event_topic = Base.mqtt_root_topic + "/event"

    def __init__(self, name):
        super().__init__(name)
        self.worker: IWorkerThread = None

    def disconnect(self):
        self.worker.stay = False

    def shutdown(self):
        self.worker.stop()  # request to thread to exit its processing loop
        self.worker.join()  # wait for the thread to complete
        super().shutdown()

    def on_message(self, client: object, userdata: Any, msg: object) -> None:
        """The standared MQTT callback for arriving messages.

        Args:
            client (object) : mqtt client
            userdata (Any) : any user specific data
            msg (object): MQTT message
        """
        if msg.topic == self.event_topic:
            em = json.loads(msg.payload.decode())
            self.on_event(em)
        else:
            self.error(f"Unknown message to {self.name}: {msg.topic}")

    def on_event(self, em) -> None:
        """Notification event callback e.g info or warning.

        Args:
            em (dictionary): dictionary describing the event
        """
        if em["type"] == "Info":
            self.info(em["msg"], em["details"])
        elif em["type"] == "Debug":
            self.debug(em["msg"], em["details"])
        elif em["type"] == "Warning":
            self.warning(em["msg"], em["details"])
        elif em["type"] == "Error":
            self.error(em["msg"], em["details"])
        else:
            self.error("PANIC: unknown event type " + em["type"], str(em))

    def run(self):
        """Run the network loop."""
        super().run()
        self.worker.mqtt_client = self.mqtt_client
        self.worker.name = self.name
        self.worker.event_topic = self.event_topic
        self.worker.start()

    @classmethod
    def register(cls):
        Base.register()
