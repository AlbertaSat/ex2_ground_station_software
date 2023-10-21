# Scheduler Notes

Basic format and API for using the scheduler

## File Format

Schedules loosely follow the crontab model. Each line of a scheduler file
has a time specifying when to run and a task to run at that time. The format
of the time specifier is:

```
millisecond second minute hour day month year
```

The interpretation of most of the fields is reasonably straight forward.
Legal ranges for each field are:

  |-------|-----------|
  | msec | 0-999 |
  | sec | 0-59 |
  | min | 0-59 |
  | hour | 0-23 |
  | day | 1-31 |
  | month | 1-12 |
  | year | 2023-2026 |
  | | or 23-26 |
  |-------|-----------|

The reason for this slightly curious format is to allow for periodic tasks.
The `crontab(5)` man page covers a whole range of periodicity specifiers,
although we only support "wildcard" (`*`) and "step" (`/`). For example:

```
# YukonSat play next audio file 30 minutes past every hour of March 2023.
0 0 30 * * 3 23 yk.audio.playback
# AlbertaSat take an image every 5 minutes, every hour forever
0 0 */5 * * * ex2.iris.capture
```

The scheduler uses Unix UTC timestamps to schedule its tasks, and it is
expected that we will synchronize the satellite's clock to earth's.
The groundstation parses each cron spec into three timestamps:
`first` is the timestamp of the first execution of the task;
`period` is the repeat time in seconds;
and `last` is the expiry or last execution of a periodic task.
The cron format allows users to specify schedules that can be parsed
into these 3 fields, however, if users find the format confusing or not
expressive enough we can easily change it, since the parsing is done on
the ground station.

Note: as of February 2023 the `last` field is always 0, i.e. all periodic
commands run forever. Until expiry is implemented, you can just delete a
schedule that has finished.
