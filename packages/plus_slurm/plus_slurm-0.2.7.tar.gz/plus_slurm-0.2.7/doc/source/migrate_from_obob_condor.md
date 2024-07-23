# Migrating from `obob_condor` or `hnc_condor`

If you previously used the HTCondor cluster at the University of Salzburg either
via [obob_condor] or 
the `hnc_condor` package of [obob_ownft],
migrating to the new cluster is quite easy for you. This document provides
an overview what you need to do and what is different.

## General
Although the underlying scheduling system changed from [htcondor] to [slurm],
the general principles all still apply: You define your jobs by
writing a class that derives from a specific `Job` class, specify the
resources needed and submit everything to a queue from which it then
gets executed when it is your turn.

However, there are some notable changes:

### No more bombers
Both the interim solution as well as the new cluster do not have
personalized virtual machines a.k.a. bombers anymore. They are replaced by
two possibilities, depending on your use case:

1. Login Nodes: These machines are shared with all cluster users. They **must
    not be used for real computations!** Submitting jobs and some light
    development are fine, though. **If you use too much RAM or CPU, you
    will get kicked out of the node!**
2. Interactive Jobs: These are not available right now but will be
    the replacements for the bombers. You basically run a job that you can
    connect to via [xpra], ssh or Visual Studio Code. This is for real
    computation that needs to be done interactively or for development that
    needs more RAM and / or CPU.

```{warning}
Until the interactive jobs are available, please continue to use your
bombers for any interactive things.
```

### New command line commands
All the `condor_*` commands are not going to work anymore, of course. Here
are the most import counterparts of the [slurm] world.

| What it does                    | HTCondor        | Slurm      |
|---------------------------------|-----------------|------------|
| Show the jobs in the queue      | `condor_q`      | `squeue`   |
| Get Information about the nodes | `condor_status` | `sinfo`    |
| Remove a queued or running job  | `condor_rm`     | `scancel`  |

There are more commands, of course and all commands also have lots of
parameters and switches. Take a look at the [slurm website][slurm] to know
more.

### Memory
If your `Job` wanted to use more RAM than specified, the behavior of [htcondor]
was to kill the job, update the memory requirements and run the job again.

[Slurm][slurm] is just going to kill your `Job`.

### Time
[Slurm][slurm] requires you to specify how much time you jobs need to run.

## If you use python
Migrating from [obob_condor] is straight forward, because `plus_slurm` is a
drop-in replacement.

1. In your `requirements.txt` or `environment.yml` replace the [obob_condor]
    dependency by `plus_slurm`.
2. Fix all your imports: `from obob_condor import Job, JobCluster` becomes:
    `from plus_slurm import Job, JobCluster`.
3. Make sure to not use the `adjust_mem` and `owner` parameters when instantiating
    {class}`plus_slurm.JobCluster`.
4. Make sure to set the `request_time` parameter when instantiating
    {class}`plus_slurm.JobCluster`.
5. Remember that you need to be on the Login Node to submit your jobs.

And that's it!

## If you use Matlab
### Code migration
Migrating your code from `hnc_condor` to `plus_slurm` is also really straight forward.

1. When initializing `obob_ownft`, make sure to request `plus_slurm` as a 
    package: `cfg.package.plus_slurm = true;`
2. Replace all `obob_condor_*` calls with `obob_slurm_*`.
3. Make sure to not use `cfg.adjust_mem` and `cfg.owner`.
4. Make sure to set the `cfg.request_time`.
5. Remember that you need to be on the Login Node to submit your jobs.

And that's it!

### Submitting from an interactive Matlab
Unfortunately, there is no X2Go available on the cluster login nodes. But you
can use [xpra] as an alternative.

Make sure to install it on your local machine. Then open a terminal and enter:

```bash
xpra start --ssh="ssh" ssh://bXXXXXX@login5-gui.acsc.sbg.ac.at --start-child="/mnt/obob/bin/Matlab/R2020a/bin/matlab -desktop"  --exit-with-children 
```

Wait a bit and you will get a full-blown Matlab window that runs on the login node...


[htcondor]: https://htcondor.readthedocs.io
[slurm]: https://slurm.schedmd.com
[xpra]: https://xpra.org/
[obob_condor]: https://obob-condor.readthedocs.io
[obob_ownft]: https://gitlab.com/obob/obob_ownft