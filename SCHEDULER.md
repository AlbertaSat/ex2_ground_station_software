# Scheduler Notes

Basic format and API for using the scheduler

## File Format

Schedules loosely follow the crontab model. Each line of a scheduler file
has a time specifying when to run and a task to run at that time. The format
of the time specifier is:

```
millisecond second minute hour weekday day month year
```

The interpretation of most of the fields is obvious, except that `weekday` is
the day of the week, with Sunday defined as 1, and `year` is the number of years
since the *epoch* (January 1, 1970), so 2023 would be represented as 53.

The reason for this slightly curious format is to allow for periodic tasks.
The `crontab(5)` man page covers a whole range of periodicity specifiers,
for example:

```
# YukonSat play next audio file 30 minutes past every hour of 2023 
0 0 30 * * * * 53 yk.audio.playback
# AlbertaSat take an image every 5 minutes, every hour forever
0 0 0-59/5 * * * * ex2.iris.capture
```

Currently, only the wildcard (`*`) is implemented but we can enhance the
periodicity support as we understand our mission requirements better.



