## Directory Memorizer

This CLI tool is meant to save time navigating between frequently used directories from [Cmder](https://cmder.net/) (it can probably be made to work on ConEMU and perhaps on other command shells as well, but I haven't tested this). It provides the following functionality:

* Save the current directory you're in under your shortcut name of choice (or you may explicitly specify directory for the given shortcut).
* Remove shortcuts.
* List all shortcuts with their mapped directories (alphabetically sorted in ascending order).
* Search through your shortcut list (the Wildcard character is '%').
* Navigate directly to the directory mapped to that shortcut (or alternatively, open that directory in a file explorer window). This feature will fallback on fuzzy string matching if no exact shortcut is found.

### Requirements

* Windows 7 or higher (it might work on older versions of windows). *Other operating systems are not yet supported.
* Python 3.7 (should work on 2.7 and probably other versions of 3, but this is untested)
* Jellyfish (pip install jellyfish)
* Fuzzy (pip install fuzzy)

For Windows:
* Cmder [https://cmder.net/](https://cmder.net/) (this tool can probably be made to work with some other command shells)

### Installation

#### Windows

Note that these instructions assume you're using Cmder.

If you don't have [Python](https://www.python.org/downloads/) installed, download the latest version of Python 3, and make sure it can be run from command line. Then run:

pip install fuzzy
pip install jellyfish

If that failed, you may also need to add the scripts directory (from your python installation), to your PATH variable as well.

Install the [Cmder](https://cmder.net/) console emulator if you haven't already.

Next, navigate to the startup scripts directory for Cmder. From the Cmder install directory, it's in **__config/profile.d__** - if you're not sure where Cmder is located, the default configuration usually has Cmder opening in its own installation directory by default, so just open Cmder, run **cd config/profile.d**, and then run **explorer .\**. Not only will you have Cmder shell in the startup directory, but you'll have an explorer window open here too (we'll need this shortly).

If you don't already have a startup batch script in this directory, create one with whatever name you wish ("startup.bat" should suffice). Now open this file in your preferred editor.

If this is a new script, it's recommended that you add @echo off as the first line of the script so that the commands we run in this script don't pollute your Cmder shell everytime you run Cmder.

Add the following lines:

```Batchfile:

REM Directory Memorizer commands
DOSKEY sd=%~dp0%scripts\Directory_Memorizer\launcher.bat -c $*
DOSKEY se=%~dp0%scripts\Directory_Memorizer\launcher.bat -e $*

```

If you're unfamiliar with Batch scripting, note above the lines starting with 'DOSKEY'. Here we're using the DOSKEY command to create an alias for a command, so you can simply use that name in place of that command. Here I created two aliases 'sd' and 'se'. The difference between these two commands will be explained momentarily. Also note that REM just indicates a comment (it doesn't run or do anything, but it's useful for documenting what we're doing).

Now create a new folder in this directory called scripts (if you haven't already), go inside that folder, and place the Directory_Memorizer project folder inside it.

Now restart Cmder. Installation should now be complete! 

Test to make sure it works by running:

```Console:
cd config/profile.d
sd -a cmder_startup
cd /
sd cmder_startup
se cmder_startup
```

The above created a shortcut to our startup scripts location (it assumes a fresh install of Cmder, behaviour may vary between Operating Systems, I tested on Windows 7). We cd to root, then passed our shortcut name 'cmder_startup' to the sd command, which took us back to the startup scripts directory. We then fed the se command our shortcut and it opened that directory in a File Explorer window instead.

## Usage

The functionality of the tool can be viewed at any time using by passing it the -h parameter.

```Console:
sd -h
```

To add a shortcut to the current working directory:

```Console:
sd -a <shortcut_name>
```

To add a shortcut to a specific directory (this should generally be the full path, but really anything could go here - just know that it will be fed to the CD or explorer commands when it is used):

```Console:
sd -a <shortcut_name> <directory_path>
```

To remove a shortcut:

```Console:
sd -r <shortcut_name>
```

To use shortcut to change directories.

```Console:
sd <shortcut_name>
```

To open a shortcut in the file explorer.

```Console:
se <shortcut_name>
```

To list all shortcuts (in alphabetical order):

```Console:
sd -l
```

To search for shortcuts matching a search term (in this example, we'll search for shortcuts with 'startup' in their name):

```Console:
sd -s startup
```

For searches, wildcards may also be used. By default, your search term is wrapped by wildcard character on both sides if none are specified. The wildcard character is '%'.
Wildcard characters can be placed wherever. __Under the hood, it's just python creating a regex string out of the search term by replacing the '%' characters with '.*'.__

```Console:
sd -s %project%reports%
```