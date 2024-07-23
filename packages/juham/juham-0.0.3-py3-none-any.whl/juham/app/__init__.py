"""
Module: Juham Applications

Description:

This module implements applications built on top of the Juham framework. It provides a set of base 
classes and utilities that serve as the foundation for developing home automation applications. 
These classes enable seamless integration and interaction with various components of a home automation system, 
facilitating the creation of robust and customizable automation solutions.

Features:

- **Modular Plugin Architecture**: Design and implement home automation applications with a modular approach.
- **Extensible Base Classes**: Extendable classes that can be customized to meet specific automation requirements.
- **Seamless Integration**: Smooth integration with the Juham framework and its components.
- **Event Handling**: Efficient event handling and response mechanisms for real-time automation.
- **Logging and Error Handling**: Comprehensive logging and error handling for reliable application performance.
- **Serialization**: Robust serialization system for configuring applications with file formats e.g.  JSON.

Usage:

To create a home automation application, extend the provided base classes with your custom logic and configurations. 
Instantiate and configure your application, then run it to start automating your home.

Example:
::

    from juham.app  import JApp

    class MyHomeAutomationApp(JApp):
        def __init__(self, name):
            super().__init__(name)
            # Custom initialization code here

        def handle_event(self, event):
            # Custom event handling code here



    app = MyHome("cottage")
    app.run()


"""

from .japp import JApp

__all__ = ["JApp"]
__version__ = "1.0.0"
__author__ = "Juha Meskanen"
