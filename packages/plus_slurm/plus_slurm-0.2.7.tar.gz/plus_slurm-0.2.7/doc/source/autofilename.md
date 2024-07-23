# Automatically generating filenames for your jobs

## Introduction

A common pattern for cluster jobs is:

1. They accept a bunch of parameters like:
   1. subject_id
   2. condition
   3. etc...
2. They load the respective data
3. Do some computation
4. Save the data to the storage

A common analysis also has more than one cluster job. Normally, each job 
stores its output in a separate folder. A good practise is that each subject
gets their sub_folder in this job folder. Furthermore, all the
job folders are normally in one "meta" folder.

Let's assume our project is called "super_markov". This means, you would
have a folder like: `/mnt/obob/staff/hmustermann/super_markov/data`. You might
then have a cluster job called `Preprocess`. The data of the subject
`19800908igdb` should thus be stored in `/mnt/obob/staff/hmustermann/super_markov/data/Preprocess/19800908igdb/...`

Let's take this one step further and assume, for every subject, we have
two conditions, `ordered` and `random` and we run separate jobs for each of them.

So, the final filenames would then look like:

* `/mnt/obob/staff/hmustermann/super_markov/data/Preprocess/19800908igdb/19800908igdb__condition_ordered.dat`
* `/mnt/obob/staff/hmustermann/super_markov/data/Preprocess/19800908igdb/19800908igdb__condition_random.dat`

**Does this not look like something we should automate?**

And one further issue: A cluster job might just die... Imagine, you submit 
100 jobs and 2 of them do not complete. You want to resubmit only the two jobs
that failed.

**Ok, let's automate that as well!**

## Say hello to {class}`plus_slurm.AutomaticFilenameJob`

{class}`plus_slurm.AutomaticFilenameJob` is a subclass of {class}`plus_slurm.Job`.
This means that it basically does all the same things and you use it in a very
similar way: You override the {meth}`plus_slurm.AutomaticFilenameJob.run` method
with the commands that you want to run on the cluster and it will do just that.

However, it introduces some additional methods that automate the file naming process.

For this to work properly, however, you should do some preparations.

## Derive a Job class for the project

In order to use a common data folder for the whole project, the easiest way
is to create a project specific Job class:

```python
from plus_slurm import AutomaticFilenameJob


class MyProjectJobs(AutomaticFilenameJob):
    base_data_folder = '/mnt/obob/staff/hmustermann/super_markov/data'
```

You see that the code is really simple. We create the class, derive it from
{class}`plus_slurm.AutomaticFilenameJob` and the only thing we add to this
class is that we set {attr}`plus_slurm.AutomaticFilenameJob.base_data_folder`.

## Write your Job classes for the individual jobs

Writing the individual job classes is as straight forward as you already know
with the only exception that we derive those classes from the project wide
job class we just created.

```python
import joblib # This is a very good library for saving python objects.
from plus_slurm import JobCluster, PermuteArgument

class Preprocess(MyProjectJobs):
    job_data_folder = 'Preprocessing'

    def run(self, subject_id, condition):
        # here you load your data
        # now you do you processing

        # now we want to save the data...
        joblib.dump(result_data, self.full_output_path)

job_cluster = JobCluster()
job_cluster.add_job(
   Preprocess,
   subject_id=PermuteArgument(['19800908igdb', '19700809abcd']),
   condition=PermuteArgument(['ordered', 'random'])
)

job_cluster.submit()
```

As you can see, the `Preprocess` job gets gets executed four times (once for
every combination of the `subject_id` and `condition` arguments).

Additionally, it set the `job_data_folder` property to define, in which subfolder
of `base_data_folder` (which we defined in `MyProjectJobs` above) the data would
end up in.

`self.full_output_path` now automatically generate a filename like this:

```python
'base_data_folder/job_data_folder/subject_id/subject_id__firstKwargName_value__secondKwargName_value.dat'
```

So, in our case, this would be for the first job:

```python
'/mnt/obob/staff/hmustermann/super_markov/data/Preprocessing/19800908igdb/19800908igdb__condition_ordered.dat'
```

## Things to keep in mind

### All folders are created automatically

If you do not want this, you can set {attr}`plus_slurm.AutomaticFilenameJob.create_folder` to `False`.

### Only keyword arguments are used for filename creation

You must specify the arguments as keyword arguments to be used for the filename
when you add the job.

### The order of the keyword arguments in the filename is the order to the arguments in the add_job call.

So, keep it constant!

### There are more advanced usages

Like you can exclude kwargs from going into the filename. In this case, it
might make sense to add a hash value instead. For instance if you
iterate over multiple time regions.

For all information, check out the {class}`reference <plus_slurm.AutomaticFilenameJob>`.
