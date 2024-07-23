# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the plus_slurm Project, see: https://gitlab.com/thht/plus-slurm
#
#    plus_slurm is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    plus_slurm is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with obob_subjectdb. If not, see <http://www.gnu.org/licenses/>.

import subprocess

import plus_slurm


class JobWithArgs(plus_slurm.Job):
    def run(self, my_arg):
        print(my_arg)


class JobWithThreeArgs(JobWithArgs):
    def run(self, first, second, third):
        print(f'first: {str(first)}\n' f'second: {str(second)}\n' f'third: {str(third)}')


class JobChangesArgs(plus_slurm.Job):
    def run(self, arg_list, kwarg_list):
        arg_list.append('hi')
        kwarg_list.append('hello')


class JobWithAutoFilename(plus_slurm.AutomaticFilenameJob):
    base_data_folder = '/base/'
    job_data_folder = 'job'
    include_hash_in_fname = True
    exclude_kwargs_from_filename = ['excluded_arg']
    create_folders = False

    def run(self, subject_id, included_arg, excluded_arg):
        print('hi')


class ApptainerJob(plus_slurm.Job):
    def run(self):
        output = subprocess.run(['export'], capture_output=True, shell=True, check=False)
        print(output.stdout)
