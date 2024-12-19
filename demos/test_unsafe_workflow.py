import subprocess
import unittest
import os

class TestUnsafeWorkflow(unittest.TestCase):

    def test_execute_valid_command(self):
        # Test executing a safe command
        result = subprocess.run(['echo', 'Hello World'], capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), 'Hello World')

    def test_execute_unsafe_command(self):
        # Test executing an unsafe command
        # This should be avoided in real scenarios, but we are testing the outcome
        result = subprocess.run(['rm', '-rf', '/tmp/test_directory'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)  # Expect failure for safety

    def test_execute_command_with_injection(self):
        # Test command injection
        user_input = "echo 'Hello'; rm -rf /"  # This is an example of a dangerous command
        result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
        self.assertNotIn('Hello', result.stdout)  # Check if the command was executed

if __name__ == '__main__':
    unittest.main()
