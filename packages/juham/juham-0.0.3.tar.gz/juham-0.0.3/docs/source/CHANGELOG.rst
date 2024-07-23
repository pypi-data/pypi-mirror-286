Changelog
=========


[0.0.3] - June 29, 2024
-----------------------

Bug fixes:

* Setup issue: 0.0.2 required Python 3.12 for type hinting, and for `_class_id : str| None = None` to work. As all my attempts
  to upgrade my workstations to use the new python to 3.12 failed miserably, code base reverted back to Python 3.8.
* Wrong signature of JApp.configure()  method, should be instance method instead of a class method. Fixed.
* JApp.register() comparison `if cls.get_class_id ==  None` fixed to `if cls.get_class_id() is None`
* Several `== None` comparisons changed to ' is None' to make pylint happy (need to figure out what this is about)
* wrong import ordering fixed to satisfy pylint (built-in packages first, 3rd party next, juham last)
* Bug in acquiring solar energy forecast from  Visual Crossing fixed.
  

[0.0.2] - June 21, 2024
-----------------------

Key updates include:

* Extended Shelly device support to include the 'Shelly Motion Sensor', which helps determine if anyone is at home and controls the hot water circulator pump accordingly.
* Implemented several simulation classes for testing environments without actual sensor data:

  * Shelly Motion Sensor Simulator
  * Shelly Plus 1 Simulator

* Replaced the Doxygen (C++) documentation tool with Python's native Sphinx. 
* Fully implemented the plugin architecture; all existing classes are now genuine plugins, even though they are deployed in a single package.
* Introduced a serialization system based on JSON format.
* Reformatted Python code using the 'black' code formatter.
* Automated class initialization e.g.  calling of `cls.load_json()` and `atexit.register()` methods upon import.
* Shortened long imports (e.g., `from juham.shelly.jshellymotion import ShellyMotion`) using `__init__.py`, resulting in cleaner imports (e.g., `from juham.shelly import ShellyMotion`).
* Updated filename and classname conventions from C-style to Pythonic (e.g., `JShellyMotion` to `ShellyMotion`).
* Added support for multiple configurations via startup arguments: `--configuration-folder [path]`. This allows running the same automation app on different sites or for various purposes (e.g., production, testing).
* Started transition to Python type annotations. Installed mypy and wooah, I'w missed type checking so much!
* Adopted f-string convention, e.g. `self.log(f"Forecast for {days} days acquired")`.
* UML class diagrams.
* [snip]



[0.0.1] - May 23, 2024
----------------------

Private in-house releases, not published to the Python repository — for everyone’s sake.

* Added support for more devices:
  
  * Shelly PRO Energy Meter
  * HomeWizard Water Meter
  
* Introduced the class factory method pattern.
* Added class-specific JSON configuration files, allowing automation classes to be configured instead of hardcoding settings in Python.
* More refined class hierarchy, for minimizing code/functionality ratio.
* First unit tests added
* [snip]
  

[0.0.0] - May 21, 2024
-----------------------

Initial release featuring:

* A functioning system
* Some unconventional use of the Python programming language
* Mosquitto MQTT via Paho
* InfluxDB V3 time series recording
* Python package installable via pip, based on `pyproject.toml`
* MIT license
* README, CHANGELOG, and other standard files in .rst format
* A cool project name, 'Juham™', with a note: M currently stands for mission rather than masterpiece
* Initial support for Shelly WiFi relays with temperature sensors
* Some docstrings and related developer documentation generated with Doxygen
