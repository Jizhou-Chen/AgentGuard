#!/bin/bash

# Install necessary tools
sudo apt-get update
sudo apt-get install -y selinux-utils selinux-basics

# Create the SELinux module file if it doesn't exist
if [ ! -f tests/sandbox_safety_constraints.te ]; then
    echo "module sandbox_safety_constraints 1.0;

require {
    type untrusted_t;
    type user_home_t;
    type init_t;
    class file { read open getattr };
    class process { execmem execstack };
}

# Block execution of potentially unsafe commands
neverallow untrusted_t self:process { execmem execstack };

# Prevent access to sensitive files
neverallow untrusted_t user_home_t:file { read open getattr };
neverallow untrusted_t init_t:file { read open getattr };" > tests/sandbox_safety_constraints.te
fi

# Create the SELinux module
sudo checkmodule -M -m -o sandbox_safety_constraints.mod tests/sandbox_safety_constraints.te
sudo semodule_package -o sandbox_safety_constraints.pp -m sandbox_safety_constraints.mod

# Load the SELinux module
sudo semodule -i sandbox_safety_constraints.pp

# Set SELinux to enforcing mode
sudo setenforce 1

echo "Sandbox safety constraints have been applied."
