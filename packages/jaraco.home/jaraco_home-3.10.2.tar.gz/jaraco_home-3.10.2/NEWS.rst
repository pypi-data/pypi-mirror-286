v3.10.2
=======

Bugfixes
--------

- Prefer tempora.parse for its better timezone support.


v3.10.1
=======

Bugfixes
--------

- Fix clean_phone when country code is included without plus prefix.


v3.10.0
=======

Features
--------

- Allow the dialed number to be supplied.


v3.9.0
======

Features
--------

- Restored Python 3.8 compatibility.


v3.8.1
======

Bugfixes
--------

- Fix check-traps to actually reflect status.


v3.8.0
======

Features
--------

- Add script for checking the mouse trap(s).


v3.7.0
======

Features
--------

- Allow time and browser to be specified in spam call reporter.


v3.6.0
======

Features
--------

- Add routine to quickly report spam calls to FTC.


v3.5.1
======

Bugfixes
--------

- Removed workaround in tests.


v3.5.0
======

Features
--------

- Require Python 3.8 or later.


v3.4.0
======

In HDHomeRun utility, now include device ID in the data.

v3.3.1
======

Fix bug in gather_status.

v3.3.0
======

- Idle tuners are now detected in random order.
- Tuner ID is now included in the status.

v3.2.0
======

HDHomeRun routine can now automatically update the package.

Require Python 3.9 or later.

v3.1.2
======

Use absolute path for hdhomerun_config, else it fails in LaunchAgent.

v3.1.1
======

Bugfixes in hdhomerun.

v3.1.0
======

Add hdhomerun module.

v3.0.2
======

Switch to PEP 420 for namespace packages.

3.0.1
=====

Require later lxml to avoid DeprecationWarning.

3.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

Drop support for Python 3.5 and earlier.

2.0
===

Drop support for Python 3.4 and earlier.

1.1
===

Moved hosting to GitHub. Refreshed package metadata.

1.0
===

Initial release.
