Troubleshooting
====================================

Here a list of known issues.
If the problem persists, you can contact the MASER developer team at: maser.support@groupes.renater.fr.

  * **//I have an error message "[Errno 13] Permission denied:" during installation//:**

This means that you don't have the right to install the package in your Python "site-packages" local directory.
To solve this problem, install the package as a super user (e.g., using sudo command for instance), or modify the "site-packages" user access permissions.

  * **//I have an error message "Exception: Cannot find CDF C library. Try os.putenv("CDF_LIB", library_directory) before import." during the installation"//:**

This means that the %%$CDF_LIB%% environmment variable is not set. This variable is required to run the CDF software distribution from Python. For more information about how to set up this software, visit the CDF home page at http://cdf.gsfc.nasa.gov/.
