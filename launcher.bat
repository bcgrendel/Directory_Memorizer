@echo off

rem Get this script's directory
set script_path=%~dp0

rem
if "%~1" == "" goto :end
set is_cd=y
if "%~1" == "-e" set is_cd=n

rem default output is to list all directory shortcut mappings
if "%~2" == "" goto :list_all

set first_param=%2

if "%first_param%" == "-l" goto :list_all
if "%first_param%" == "-list" goto :list_all

if "%first_param%" == "-h" goto :print_help
if "%first_param%" == "-help" goto :print_help

rem if only one parameter provided, it must be the shortcut name, cd to the expanded directory.
if "%~3" == "" goto :cd_to_dir

set second_param=%3

if "%first_param%" == "-d" goto :remove_directory
if "%first_param%" == "-r" goto :remove_directory
if "%first_param%" == "-remove" goto :remove_directory

if "%first_param%" == "-s" goto :search_shortcuts
if "%first_param%" == "-search" goto :search_shortcuts

set third_param="%cd%"
if not "%~4" == "" set third_param="%4"

if "%first_param%" == "-a" goto :add_directory
if "%first_param%" == "-add" goto :add_directory

rem Incorrect usage...
echo.
echo ^[launcher.bat^] ERROR: Incorrect syntax.
echo.
goto :print_help
goto :end

:add_directory
python %script_path%main.py -a %second_param% %third_param%
goto :end

:remove_directory
python %script_path%main.py -r %second_param%
goto :end

:cd_to_dir
FOR /F "tokens=* USEBACKQ" %%F IN (`python %script_path%main.py %first_param%`) DO (
set dir_path=%%F
)
if "%is_cd%" == "y" cd "%dir_path%"
if "%is_cd%" == "n" explorer "%dir_path%"
goto :end

:search_shortcuts
python %script_path%main.py -s %second_param%
goto :end

:list_all
python %script_path%main.py -l
goto :end

:print_help
echo.
echo   Usage:
echo   ------
echo.
echo     [No arguments]                        List all shortcuts
echo.
echo     -a ^<shortcut_name^> ^[directory_path^]   Adds shortcut.
echo                                           Uses current directory ^if 'directory_path' is not specified.
echo.
echo     -r ^<shortcut_name^>                    Removes shortcut.
echo.
echo     -s ^<search_term^>                      Lists shortcuts matching the search term.
echo                                           May use the '%%' character as wildcard.
echo           EXAMPLE: %%project%%reports%%
echo.
echo     -h                                    Displays this help message.
goto :end

:end