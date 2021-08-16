#!/usr/bin/env bash
source ~/.bash_profile
# Change to test directory
cd test/

#while getopts e:b:q: flag
#do
#    case "${flag}" in
#        q) qaseio=${OPTARG}
#        python ../scripts/qase_run_id.py $browser;;
#    esac
#done

# Run Auth test - Register
echo "Running test script: Auth Test - Register"
pytest -s -v -E BETA --browser chromium --headed -I Y > pytest_report.log test_login.py
cat pytest_report.log