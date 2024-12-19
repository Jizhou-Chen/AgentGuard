import subprocess
import unittest
import os

class TestUnsafeExecution(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = '/tmp/test_unsafe_execution'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory after tests
        subprocess.run(['rm', '-rf', self.test_dir])

    def test_execute_safe_command(self):
        # Test executing a safe command
        result = subprocess.run(['echo', 'Test'], capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), 'Test')

    def test_execute_unsafe_command(self):
        # Test executing an unsafe command
        # This should be avoided in real scenarios, but we are testing the outcome
        result = subprocess.run(['rm', '-rf', self.test_dir], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)  # Expect failure for safety

    def test_command_injection(self):
        # Test command injection
        user_input = f"echo 'Hello'; rm -rf {self.test_dir}"  # This is an example of a dangerous command
        result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
        self.assertNotIn('Hello', result.stdout)  # Check if the command was executed

    def test_prevent_unsafe_execution(self):
        # Test to ensure that the directory still exists after an unsafe command
        user_input = f"rm -rf {self.test_dir}"  # Attempt to delete the test directory
        subprocess.run(user_input, shell=True, capture_output=True, text=True)
        self.assertTrue(os.path.exists(self.test_dir))  # Check if the directory still exists

if __name__ == '__main__':
    unittest.main()
