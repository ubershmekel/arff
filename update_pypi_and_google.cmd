
c:\python27\python.exe setup.py bdist --format=wininst
@pause
c:\python27\python.exe setup.py sdist
@pause

c:\python27\python.exe setup.py sdist upload
@pause
c:\python27\python.exe setup.py google_upload --src
@pause
