
import os
import sys
import shutil
import argparse

INSTALL_DIRECTORY = sys.path[0]

parser = argparse.ArgumentParser(
	prog=f"python erktheme.py",
	description='Erk Theme Compiler',
	epilog="""Edit the files in the \"Theme\" folder, and when you're ready to create your Erk theme, execute this program with the name
of the theme as the only argument. This will create a zip archive, named <THEME_NAME>.zip. This can be imported into Erk by using the
-T or --install-theme arguments."""
)


parser.add_argument('name', metavar='NAME', type=str, help='A name for the theme')

parser.add_argument("-b","--base", metavar='DIRECTORY', type=str, help='Compile theme from the given directory')

parser.add_argument("-n","--new", help='Creates a new theme with all default settings', action="store_true")

args = parser.parse_args()

if args.new:
	shutil.copytree(os.path.join(INSTALL_DIRECTORY, "base"), args.name, ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
	sys.exit(0)

THEME = args.name

if args.base:
	SOURCE = args.base
else:
	SOURCE = os.path.join(INSTALL_DIRECTORY, "base")

os.mkdir("./dist")
os.mkdir(f"./dist/{THEME}")

os.system(f"compile_resources.bat {SOURCE}")

#shutil.copytree("./Theme/images", f"./dist/{THEME}/images",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copy(f"{SOURCE}/resources.py", f"./dist/{THEME}/resources.py")
shutil.copy(f"{SOURCE}/text.json", f"./dist/{THEME}/text.json")
shutil.copy(f"{SOURCE}/widgets.qss", f"./dist/{THEME}/widgets.qss")
shutil.copy(f"{SOURCE}/icon.png", f"./dist/{THEME}/icon.png")

os.remove(f"{SOURCE}/resources.py")

os.system("powershell.exe -nologo -noprofile -command \"& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist', 'erk_theme.zip'); }\" ")

shutil.rmtree('./dist')

os.rename('erk_theme.zip', f"{THEME}.zip")

