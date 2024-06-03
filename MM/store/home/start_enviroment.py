import subprocess

# Path to your virtual environment activate script
venv_activate_script = r'C:\Desktop\MNM\MM\Scripts\activate'

# Command to activate virtual environment
activate_command = f'call {venv_activate_script}'

# Change directory to your Django project directory
django_project_directory = r'C:Desktop\MNM\MM\store'
os.chdir(django_project_directory)

# Activate virtual environment using subprocess
subprocess.call(activate_command, shell=True)

# Now you're in the virtual environment, you can run Django commands
# For example, run the Django development server
subprocess.call('python manage.py runserver', shell=True)
