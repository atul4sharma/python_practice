#!/usr/bin/env python

#  The file_iterator class is to iterate line of files
#  when we are trying to ignore some rows according to pattern
#  
#  ignore the line group(inside ----) that starts with #
#  ie 
#  
#  cmd1
#  cmd2
#  --------
#  #cmd1          // Ignore this group
#  cmd2           // Ignore this group
#  -------
#  cmd1           // Ignore this group
#  #cmd2          // Ignore this group
#  ---
#  

import re

class group_structure(object):
    def __init__(self, lines_group, start, end):
        self._group = lines_group
        self._start = start
        self._end   = end

    def group(self):
        return self._group

    def __repr__(self):
        return "group: line[{0}-{1}]{2}".format(self._start, self._end, self._group)


class file_iterator(object):

    def __init__(self, file_name):
        print "opening file"
        self._file_name    = file_name
        self._ignored_rows = []

    def ignored_rows(self):
        return self._ignored_rows

    def __enter__(self):
        self._file_obj     = open(self._file_name, 'r')
        self._previous     = self._file_obj.next()
        self._group        = 3 if re.search("^#comparison-file", self._previous) else 2
        self._line_counter = 0
        return self

    def __exit__(self, type, value, traceback):
        print "closing file\n"
        self._file_obj.close()

    def __iter__(self):
        return self

    def _get_next_group(self):
        lines_group         = [self._file_obj.next().rstrip() for i in range(self._group)]
        prev_line_count     = self._line_counter
        self._line_counter += len(lines_group)

        group_object = group_structure(lines_group[:-1], prev_line_count, self._line_counter)

        return group_object

    def _is_valid_group(self, group):
        if any(re.search("^#",cmd) for cmd in group):
                return False
        return True

    def next(self):
        next_group = self._get_next_group()
        while not self._is_valid_group(next_group.group()):
            self._ignored_rows.append(next_group)
            next_group = self._get_next_group()
        return next_group.group()


with file_iterator("group_two.txt") as obj:
    for line in obj:
        print line
    print 
    print "ignored groups are "
    for g in obj.ignored_rows():
        print g

with file_iterator("group_three.txt") as obj2:
    for line in obj2:
        print line
