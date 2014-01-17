import os, jeeves_core
print 'return jobs'

def returnJobs():
    for job in os.listdir(jeeves_core.jobsRoot):
        print job