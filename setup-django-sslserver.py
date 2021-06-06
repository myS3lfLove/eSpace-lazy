import subprocess, os

def touch(file, content=""):
    with open(file, 'w') as fp:
        fp.write(content)
        pass

def installRequirments():#python -m pipenv install -r requirments.txt
    subprocess.run(['python', '-m', 'pipenv', 'install', '-r', 'requirments.txt'])
    os.system("python -m pipenv run pip freeze > requirments.txt")
    #subprocess.run(['python', '-m', 'pipenv', 'run', 'pip', 'freeze', '>', 'requirments.txt'])

def install(package):#python -m pipenv install <name(s)>
    subprocess.run(['python', '-m', 'pipenv', 'install', package])
    os.system("python -m pipenv run pip freeze > requirments.txt")
    #subprocess.run(['python', '-m', 'pipenv', 'run', 'pip', 'freeze', '>', 'requirments.txt'])

def createProject(name):#python -m pipenv run django-admin startproject <name>
    subprocess.run(['python', '-m', 'pipenv', 'run', 'django-admin', 'startproject', name])
    os.rename(name, 'src')
    touch('src/'+name+'/password.py', content="from credentials.credentials import credentials\n\ndef fetch(argument):\n    return credentials.get(argument)")
    lines = []
    with open('src/'+name+'/settings.py', 'r') as fp:
        lines = fp.readlines()
    index = lines.index('from pathlib import Path\n')
    lines[index] = "import os, sys\nfrom pathlib import Path\nfrom .password import fetch\n"

    index = lines.index('BASE_DIR = Path(__file__).resolve().parent.parent\n')
    lines[index] = "BASE_DIR = Path(__file__).resolve().parent.parent\nROOT_DIR = Path(__file__).resolve().parent.parent.parent\n"

    index = lines.index('# SECURITY WARNING: keep the secret key used in production secret!\n')
    lines[index+1] = "SECRET_KEY = fetch('secret_key')\n"

    with open('src/'+name+'/settings.py', 'w') as fp:
        fp.writelines(lines)

def createApp(projName, appName):#python -m pipenv run django-admin startapp <name>
    os.chdir('src')
    subprocess.run(['python', '-m', 'pipenv', 'run', 'django-admin', 'startapp', appName])
    os.chdir('..')
    lines = []
    with open('src/'+projName+'/settings.py', 'r') as fp:
        lines = fp.readlines()
    indexS = lines.index('INSTALLED_APPS = [\n')
    indexE = lines.index(']\n')
    lines[indexE] = "    '"+appName+"',\n"+lines[indexE]

    index = lines.index("        'DIRS': [],\n")
    lines[index] = "        'DIRS': [BASE_DIR / 'templates'],\n"

    index = lines.index("STATIC_URL = '/static/'\n")
    lines[index] = "STATIC_URL = '/static/'\nMEDIA_URL = '/media/'\nSTATICFILES_DIRS = [\n	BASE_DIR / 'static',\n	BASE_DIR / 'media',\n]\nSTATIC_ROOT = ROOT_DIR / 'Files/staticFile'\nMEDIA_ROOT = ROOT_DIR / 'Files/mediaFile'\n"

    with open('src/'+projName+'/settings.py', 'w') as fp:
        fp.writelines(lines)

def registerApp(projName, appName):#
    #os.chdir('src\'+projName)
    lines = []
    with open('src/'+projName+'/settings.py', 'r') as fp:
        lines = fp.readlines()
    indexS = lines.index('INSTALLED_APPS = [\n')
    indexE = lines.index(']\n')
    lines[indexE] = "    '"+appName+"',\n"+lines[indexE]
    with open('src/'+projName+'/settings.py', 'w') as fp:
        fp.writelines(lines)
    #print(os.getcwd())

def makeFolder(folderName):#
    os.mkdir(folderName)

def setup():#
    subprocess.run(['python', '-m', 'pipenv', 'sync'])
    subprocess.run(['python', '-m', 'pipenv', 'run', 'python', 'src\manage.py', 'makemigrations'])
    subprocess.run(['python', '-m', 'pipenv', 'run', 'python', 'src\manage.py', 'migrate'])
    subprocess.run(['python', '-m', 'pipenv', 'run', 'python', 'src\manage.py', 'collectstatic'])
    print('Enter following details for root user')
    subprocess.run(['python', '-m', 'pipenv', 'run', 'python', 'src\manage.py', 'createsuperuser'])

if __name__ == '__main__':
    touch('Pipfile')
    installRequirments()
    #install('django')
    #install('django-sslserver')
    createProject('main')
    registerApp('main', 'sslserver')
    createApp('main', 'dataStorage')
    makeFolder('src\media')
    makeFolder('src\static')
    makeFolder('src\credentials')
    touch('src\credentials\credentials.py', 'credentials = {\n\t"email_username" : "optional",\n\t"email_password" : "optional",\n\t"postgresql_name" : "optional",\n\t"postgresql_username" : "optional",\n\t"postgresql_password" : "optional",\n\t"postgresql_host" : "optional",\n\t"postgresql_port" : "optional",\n\t"secret_key" : "required",\n\t"consumer_key" : "optional",\n\t"consumer_secret" : "optional",\n\t"access_token" : "optional",\n\t"access_token_secret" : "optional",\n}')
    print('Enter credentials in src\credentials\credentials.py')
    os.system("notepad src\credentials\credentials.py")
    os.system("pause")
    setup()