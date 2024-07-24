import argparse
import logging
from juham.app import JApp
from juham.base import Object
from juham.base import JLog
from juham.database import JInflux
from juham.mqtt import JPaho2

from juham.ts import ForecastRecord
from juham.ts import PowerRecord
from juham.ts import PowerPlanRecord
from juham.ts import LogRecord
from juham.web import RSpotHintaFi
from juham.web import RVisualCrossing

from juham.web import HomeWizardWaterMeter
from juham.shelly import ShellyPlus1
from juham.shelly import ShellyPro3EM
from juham.shelly import ShellyMotion
from juham.automation import RPowerPlan
from juham.automation import RBoiler
from juham.automation import WaterCirculator
from juham.automation import EnergyCostCalculator
from juham.simulation import RTracker

from juham.shelly import ShellyPlus1Simulator
from juham.shelly import ShellyMotionSimulator


class MyHomeApp(JApp):
    """Juham home automation application.
    This initially such a beautiful application turned into this nonsense, piece by piece,
    due to python compatiblity issues. See register_plugins() and instantitate_plugins()

    """

    _class_id = ""
    application_name: str = "myhome"
    enable_plugins: bool = False  # load plugins, see pyproject.toml

    def __init__(self, name: str = "myhome"):
        """Creates home automation application with the given name.
        If --enable_plugins is False create hard coded configuration
        by calling instantiate_classes() method.

        Args:
            name (str): name for the application
        """
        super().__init__(name)

    @classmethod
    def parse_args(cls) -> None:
        """Parse the startup arguments defined by this class.
        So we introduce --enable_plugins startup option, to disable plugin
        loading for python 3.9 and earlier.
        """
        parser = argparse.ArgumentParser(description=cls.get_class_id())
        parser.add_argument(
            "--enable_plugins",
            type=bool,
            help="Enable plugins",
        )
        args = parser.parse_args()
        cls.enable_plugins = args is not None and args.enable_plugins

    @classmethod
    def register_classes(cls):
        """Hard coded class registrations for python 3.9 and below."""
        JLog.register()
        ForecastRecord.register()
        PowerRecord.register()
        PowerPlanRecord.register()
        LogRecord.register()
        RSpotHintaFi.register()
        RVisualCrossing.register()
        HomeWizardWaterMeter.register()
        ShellyPlus1.register()
        ShellyPro3EM.register()
        ShellyMotion.register()
        RPowerPlan.register()
        RBoiler.register()
        WaterCirculator.register()
        EnergyCostCalculator.register()
        RTracker.register()
        ShellyPlus1Simulator.register()
        ShellyMotionSimulator.register()

    def instantiate_classes(self):
        """Hard coded configuration for python3.9"""
        self.add(ForecastRecord())
        self.add(PowerRecord())
        self.add(PowerPlanRecord())
        self.add(LogRecord())
        self.add(RSpotHintaFi())
        self.add(RVisualCrossing())
        self.add(HomeWizardWaterMeter())
        self.add(ShellyPlus1())
        self.add(ShellyPro3EM())
        self.add(ShellyMotion())
        self.add(RPowerPlan())
        self.add(RBoiler())
        self.add(WaterCirculator())
        self.add(EnergyCostCalculator())
        self.add(RTracker())
        self.add(ShellyPlus1Simulator())
        self.add(ShellyMotionSimulator())

    @classmethod
    def register(cls):
        if cls._class_id == "":
            app_name = "myhome"
            JApp.register()
            JApp.application_name = app_name
            Object.set_log(JLog(app_name))
            JInflux.register()
            JPaho2.register()

            # register plugins
            if cls.plugins:
                cls.load_plugins()
            else:
                cls.register_classes()
            cls.initialize_class()


def main():

    # instantiate the application
    app = MyHomeApp()

    if app.enable_plugins:
        # load configuration to instantiate home automation objects
        try:
            with open("myhome.json", "r") as f:
                app.deserialize_from_json(f)
        except FileNotFoundError:
            app.warning(
                f'No "myhome.json" found, falling back to default configuration'
            )
            plugins = app.instantiate_plugins(app.plugins)
            app.add_all(plugins)
            app.info(f"Loaded and installed {len(plugins)} classes")
            with open("myhome.json", "w") as f:
                app.serialize_to_json(f)
            app.info(
                "myhome.json and class specific configuration files created in ~/.juham/ folder. Edit and restart"
            )
            exit(2)
        except Exception as e:
            app.error(f'Exception {e} occurred while reading "myhome.json"')
            exit(1)
    else:
        app.instantiate_classes()

    # start the network loops
    app.run()


if __name__ == "__main__":
    main()
