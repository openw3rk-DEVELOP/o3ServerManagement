
o3ServerManagement
------------------

Current version: 2.1.7<br>
License: MIT License<br>
Developer: openw3rk INVENT<br>
Copyright: (c) openw3rk INVENT<br>
GitHub: https://github.com/openw3rk-DEVELOP/o3ServerManagement<br>
Website: https://o3sm.openw3rk.de | https://openw3rk.de<br>

<h3>Overview:</h3>


o3ServerManagement is a Python-based graphical user interface application designed for server and system monitoring, backup management,<br> port scanning, and command-line terminal operations. 
<br>It offers a user-friendly interface to monitor system resources, create backups, scan network ports, and execute commands efficiently.

<h3>Features:</h3>


System Monitoring: Real-time display of CPU usage, RAM, disk space, network traffic, and CPU temperature.<br>

Backup Management: Easy backup creation with selection of source and destination directories.<br>

Port Scanner: Scan a range of ports on a specified host or IP address.<br>

Terminal: Integrated command-line interface supporting commands such as backup creation, system information display, and help.<br>

Info Tab: Provides application details with clickable links to the website and source code repository.<br>

Automatic Dependency Installation: Automatically installs required Python packages (such as psutil) if missing.<br>



<h3>Installation Requirements:</h3>

Python 3.0 or higher<br>



<h3>Run from Source:</h3>


Clone or download the repository.

Execute the main script using:

<pre><code>python o3ServerManagement.py</code></pre>


<h3>Usage:</h3>


System Monitoring Tab: View live system metrics.

Backup Management Tab: Select source and destination folders to create backups.

Port Scan Tab: Enter host and port range to scan for open or closed ports.

Terminal Tab: Run commands such as:

<pre><code>backup --make -from:<source> -to:<destination></code></pre><br>
<pre><code>system -meta --show</code></pre><br>
<pre><code>help --show</code></pre><br>
<pre><code>info --show</code></pre><br>
<pre><code>exit</code></pre><br>


<h3>Packaging with PyInstaller (Windows):</h3>


To create a Windows executable that runs without opening a console window, use the following command:<br>

<pre><code>pyinstaller --noconsole --onefile --icon=o3ServerManagement_ico.ico o3ServerManagement_v2.1.7.py</code></pre><br>

he resulting executable will launch as a GUI application without showing a terminal window ('--noconsole').<br>

Note the MIT licensing.<br>


<h3>License:</h3>

This project is licensed under the MIT License. See the LICENSE.txt file for full details.<br>
Copyright (c) openw3rk INVENT<br>
