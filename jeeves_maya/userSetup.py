print 'STARTING MAYA USERSETUP.PY'

import sys, os, jeeves_core, jeeves_maya

# callbacks

if jeeves_core.getVars.findJob():
    print 'JOB FOUND - FULL SETUP'
else:
    print 'NO JOB FOUND - PARTIAL SETUP'

print 'FINISHED MAYA USERSETUP.PY'