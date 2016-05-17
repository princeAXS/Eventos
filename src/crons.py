from crontab import CronTab


tab = CronTab()
cmd = 'sudo python /Users/prince/Desktop/eventos/src/eventos.py'
# You can even set a comment for this command
cron_job = tab.new(cmd)
#cron_job.minute.every(2)
cron_job.hour.every(24)


# to remove the job from cron list 
tab.remove( cron_job )


#writes content to crontab
tab.write()
print tab.render()
