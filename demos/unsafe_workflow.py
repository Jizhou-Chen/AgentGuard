import subprocess

def execute_command(user_input):
    # This function executes a shell command provided by the user
    # WARNING: This is unsafe as it does not validate the input
    subprocess.run(user_input, shell=True)

if __name__ == '__main__':
    # Example of unsafe execution
    user_command = input("Enter a command to execute: ")
    execute_command(user_command)
