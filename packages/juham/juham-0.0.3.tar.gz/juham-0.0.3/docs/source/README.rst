Welcome to Juham™ - Juha's Ultimate Home Automation Masterpiece
===============================================================



Important Changes
-----------------

This release introduces bug fixes.

In version 0.0.2, the framework used a feature that required a newer Python version than 3.8:
::

   _class_id : str | None = None

   def instantiate(class_id: str) -> Self

Attempted to upgrade Python on a few systems and even tried building it from the source code.
Unfortunately, this led to significant issues. 

All the code reverted back to be compatible with Python 3.8.

For more about the changes in this release consult :doc:`CHANGELOG <CHANGELOG>`


Project Status and Current State
--------------------------------

The software is still in planning stage.  
In its current state, you might call it merely a home automation mission, 
rather than masterpiece, but I'm working hard to turn it into a masterpiece! 



Goals
-----

Develop the ultimate home automation framework that can control all the
apparatuses in my home, and maybe also other homes.


Install
-------

1. pip install juham. This installs all the dependencies as well, I hope.

2. Set up InfluxDB 3.0 and Crafana for user interface. Not an absolute requirement, Juham™ can
   live fine without them. However, I stongly recommen using Graphana and InfluxDB, as they allow you to
   monitor your home anywhere in the world. 

3. Configure Juham™. When started all classes attempt to initialize themselves from their
   JSON configuration files, located in config sub folder. The  files to pay attention to
   are:
   
   * `config/Base.json` - fill with your MQTT host and port information. 
   * `config/JDatabase.json` - fill with your InfluxDB account information. 
   * `config/RVisualCrossing.json` - you need APIKEY to fetch weather forecast from  Visual Crossing site.
  
4. Configure `myhome.py` to run as a service, or as a quick test from console: `python3 myhome.py`. This program is a fully functional
   automation system, serving as a good starting point for your real home.
   



Design
------

The design is based on object-oriented paradigm, a modular plugin architecture, full abstraction, 
and overall robustness of design. If you appreciate these concepts, look no further — you've come to the right place!

The magic of Juham™ home automation emerges from the 'Object' base class. Just like all creatures on Earth share a common 
ancestor, all components of Juham™ trace their lineage back to this first life form of software (okay, maybe 
that’s a bit dramatic, but you get the idea).

The 'Object' base class plus a few others in the 'juham.base'module
are generic by nature, any software could be built on top of them. I'm actually planning to publish them as a separate 
python packages (yet another task to be added into :doc:`TODO <TODO>`).

The actual home automation specific classes revolve around  the MQTT broker and standardized Juham™ MQTT messages.

Data acquisition clients, such as those reading temperature sensors, electricity prices, and power levels from solar panels, 
to name a few, publish data to respective MQTT topics. Automation clients listening to these topics can then perform their 
designated tasks, such as control the temperature of a hot water boiler.




Developer Documentation
-----------------------

The documentation is still a work in progress. Originally, the documentation was generated using Doxygen, 
a tool primarily used for generating developer documentation in the C++ ecosystem. To feel more like a Python 
professional, I replaced it with Python's native documentation tool, Sphinx. After several frustrating 
hours (okay, days), I got it working, but it will require a few more hours (okay, days) of effort to be really usable.


Special Thanks
--------------

This project would not have been possible without the generous support of two extraordinary gentlemen: my best friend, Teppo K., 
and my son, `Mahi.fi <https://mahi.fi>`_. The project began with Teppo's donation of a Raspberry Pi computer, a few temperature sensors, and an inspiring 
demonstration of his own home automation system. My ability to translate my ideas into Python is greatly due to my son, Mahi.
His support and encouragement have been invaluable in bringing this project to life. 
Thank you both!
