% plus_slurm documentation master file, created by
% sphinx-quickstart on Mon Mar 26 16:49:50 2018.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Welcome to plus_slurm's documentation!

```{admonition} Migrating from obob_condor or hnc_condor?
If you work at the University of Salzburg and have previously used
the HTCondor cluster via [obob_condor on python](https://obob-condor.readthedocs.io)
or the `hnc_condor` package of [obob_ownft](https://gitlab.com/obob/obob_ownft),
take a look at {doc}`how to migrate to the new system here <migrate_from_obob_condor>`.
```

## What is this?

`plus_slurm` is a package that makes it easy to submit python jobs to a cluster
running [Slurm](https://slurm.schedmd.com/). In contrast to other available
packages like [Submit it!](https://github.com/facebookincubator/submitit),
[simple-slurm](https://pypi.org/project/simple-slurm/) or [easy-slurm](https://pypi.org/project/easy-slurm/),
it is optimized for the Slurm based clusters at the University of Salzburg,
including the most commonly encountered use-cases.

As a consequence, the choices made during the development of this package are
highly opinionated. Simplicity always trumps flexibility. The focus is on
providing a good user experience, not providing all choices offered by Slurm.

## Should I use this?

If you work at the University of Salzburg, this package is most probably a good
way to start using the cluster.

If you have previously worked with [obob_condor](https://obob-condor.readthedocs.io)
you will see that you can use all your old code as the interface is the same.

If you work at some other institution with a Slurm cluster, you can use this
package as well. Everything should work as expected.

May just take a look at {doc}`the tutorial <first_steps_python>` so you can see what
this package has to offer.

```{admonition} If you work at the University of Salzburg 
This documentation also provides some insights about the cluster,
the software you can use etc. So, even if you want to use a different package
or no package at all, you are still adviced to read through the
{doc}`general cluster introduction <cluster_intro>`.
```

If you are already familiar with our cluster infrastructure (because you
are migrating from Matlab), you can skip the first section and go directly to 
{doc}`first_steps_python`. Otherwise, get {doc}`cluster_intro`.

```{toctree}
:caption: Contents
:maxdepth: 2

cluster_intro
migrate_from_obob_condor
first_steps_python
autofilename
reference
```

# Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
