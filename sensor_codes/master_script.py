import subprocess
import sys

# List of scripts to be executed
scripts = ["python3 temp_sensor/example.py", "python3 press_sensor/example.py", "sudo python3 echosounder_sensor/examples/simplePingExample.py"]

def run_script_in_new_terminal(script_path):
    # Comando para abrir un nuevo terminal y ejecutar el script
    command = f'terminal -e "{script_path}"'
    try:
        # Ejecutar el comando en un nuevo proceso
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
	print(f"Error al ejecutar el script: {e}")
	sys.exit(1)

#Execute each script
for script in scripts:
    run_script_in_new_terminal(script)
