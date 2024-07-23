#! /usr/bin/env python

import logtool
from path import Path
from collections.abc import Iterable

@logtool.log_call
def findfile_path (fname, paths, exts = None):
  fnames = ([fname,] if fname is None or isinstance (fname, str)
            else fname)
  dpath = ([paths,] if paths is None or isinstance (paths, str)
           else paths)
  lext = ([exts,] if exts is None or isinstance (exts, str)
          else exts)
  for d in dpath:
    if d is None:
      continue
    d = Path (d).expanduser ()
    for f in fnames:
      if f is None:
        continue
      for e in lext:
        if exts is None:
          if (d / f).is_file ():
            return (d / f).strip ()
          else:
            continue
        if (d / f + e).is_file ():
          return (d / f + e).strip ()
  return None
