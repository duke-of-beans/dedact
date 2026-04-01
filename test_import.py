import sys
import site

print('Python version:', sys.version)
print('\nSite packages:', site.getsitepackages())
print('\nSys.path:')
for p in sys.path:
    print('  ', p)

print('\n' + '='*60)
print('Attempting to import dedact...')
try:
    import dedact
    print('[OK] dedact imported successfully')
    print('    Location:', dedact.__file__)
    print('    Version:', dedact.__version__)
except ImportError as e:
    print('[FAIL] Cannot import dedact:', e)
    
print('\nChecking editable install...')
import os
site_packages = site.getsitepackages()[0]
pth_file = os.path.join(site_packages, '__editable__.dedact-1.0.0.pth')
print('Looking for:', pth_file)
if os.path.exists(pth_file):
    print('[OK] .pth file exists')
    with open(pth_file) as f:
        print('    Contents:', f.read().strip())
else:
    print('[WARN] .pth file not found')
    print('    Checking for easy-install.pth...')
    easy_install = os.path.join(site_packages, 'easy-install.pth')
    if os.path.exists(easy_install):
        print('[OK] easy-install.pth exists')
        with open(easy_install) as f:
            for line in f:
                if 'dedact' in line.lower():
                    print('    Found:', line.strip())
