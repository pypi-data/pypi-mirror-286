# How to use plus_slurm

Submitting Jobs to the cluster is quite simple using the plus_slurm package.

## Make sure you are on a Login Node

Accessing the cluster requires the code to be run on a Login Node as only those
can submit jobs to the cluster.

All the code also needs to be on a shared folder so all the Compute Nodes can
access the files as well. In general, this is your home-folder and folders
you find under `/mnt`. The specifics depend on the cluster you are using, though

You also need to be in a python environment that has `plus_slurm` in its
dependencies. If you do not now what this means, please take a look at
[this tutorial](https://thht.gitlab.io/tutorials/using_python_for_science/01_prepare_computer_for_scientific_python/introduction.html).

## Define a simple job

The first thing you need to do is define what your job should do. You therefore write a class that derives from
{class}`plus_slurm.Job`. The only things you have to do is to supply a run method.

```python
import plus_slurm

class MyJob(plus_slurm.Job):
    def run(self):
        print('Hello World!')
```

The job class can be anywhere in your sourcecode tree as long as it is **not** 
in the script doing the actual job submission. So, put it in a module
(i.e. a `.py` file) or a package (i.e. a `.py` file in a folder that
also has a `__init__.py` file).

## Define a job that takes arguments

Your job can also take any kind of arguments:

```python
import plus_slurm

class JobWithArgs(plus_slurm.Job):
    def run(self, normal_arg, key_arg='my_default'):
        print('normal_arg=%s\nkey_arg=%s' % (str(normal_arg), str(key_arg)))
```

## Getting and configuring the JobCluster

In order to submit your job, you need to get an instance of {class}`plus_slurm.JobCluster`. The constructor of this class
has a lot of keyword arguments. You can set none, some or all of them. They all have quite sensible defaults:

```python
import plus_slurm

my_jobs = plus_slurm.JobCluster(required_ram='6G')
```

Now we have a JobCluster that asks for 6GB of RAM per Job.

## Adding jobs to the JobCluster

In order to add the jobs, use the {func}`plus_slurm.JobCluster.add_job` method:

```python
my_jobs.add_job(MyJob)
my_jobs.add_job(JobWithArgs, 'this_is_the_normal_arg', key_arg='and this the key arg')
```

## Adding multiple jobs with just one call

A common use case of job submission is that you want to run the same job on a number of different combinations of
parameters.

Let's consider a job like this:

```python
class AverageData(plus_slurm.Job):
    def run(self, subject_id, condition, lp_filter_freq)
        ...
```

And you have a list of subject_ids and conditions:

```python
subject_ids = [
    '19800908igdb',
    '19990909klkl',
    '17560127anpr']

conditions = [
    'visual',
    'auditory']
```

We want to run the jobs for all combinations of subject_ids and conditions. This is what {class}`plus_slurm.PermuteArgument`
is for:

```python
from plus_slurm import PermuteArgument

my_jobs.add_job(AverageData, PermuteArgument(subject_ids), PermuteArgument(conditions), 30)
```

This call adds 6 jobs, one for every combination of subject_ids and conditions.

This works for all kinds of arguments (normal ones and keyword arguments).

## Submitting the Job

Now, all you need to do is to call submit:

```python
my_jobs.submit()
```

For more advanced uses take a look at the {doc}`reference`.
