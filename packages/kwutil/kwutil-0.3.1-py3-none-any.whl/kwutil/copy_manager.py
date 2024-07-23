"""
Notes:
    It would be nice for this to support an rsync backend that could sync
    at the src/dst pair level. Not sure if this works.

References:
    https://unix.stackexchange.com/questions/133995/rsyncing-multiple-src-dest-pairs
    https://serverfault.com/questions/163859/using-rsync-as-a-queue
    https://unix.stackexchange.com/questions/602606/rsync-source-list-to-destination-list
"""
import ubelt as ub


class CopyManager:
    """
    Helper to execute multiple copy operations on a local filesystem.

    Example:
        >>> import ubelt as ub
        >>> from kwutil import copy_manager
        >>> dpath = ub.Path.appdir('kwutil', 'tests', 'copy_manager')
        >>> src_dpath = (dpath / 'src').ensuredir()
        >>> dst_dpath = (dpath / 'dst').delete()
        >>> src_fpaths = [src_dpath / 'file{}.txt'.format(i) for i in range(10)]
        >>> for fpath in src_fpaths:
        >>>     fpath.touch()
        >>> copyman = copy_manager.CopyManager(workers=0)
        >>> for fpath in src_fpaths:
        >>>     dst = fpath.augment(dpath=dst_dpath)
        >>>     copyman.submit(fpath, dst)
        >>> copyman.run()
        >>> assert len(dst_dpath.ls()) == len(src_dpath.ls())
        >>> copyman = copy_manager.CopyManager(workers=0)
        >>> for fpath in src_fpaths:
        >>>     dst = fpath.augment(dpath=dst_dpath)
        >>>     copyman.submit(fpath, dst)
        >>> import pytest
        >>> with pytest.raises(FileExistsError):
        >>>     copyman.run()
        >>> copyman = copy_manager.CopyManager(workers=0)
        >>> for fpath in src_fpaths:
        >>>     dst = fpath.augment(dpath=dst_dpath)
        >>>     copyman.submit(fpath, dst, skip_existing=True)
        >>> copyman.run()
    """

    def __init__(self, workers=0, mode='thread', eager=False,
                 overwrite=False, skip_existing=False):
        """
        Args:
            workers (int): number of parallel workers to use

            mode (str): thread, process, or serial

            eager (bool):
                if True starts copying as soon as a job is submitted, otherwise it
                wait until run is called.

            overwrite (bool):
                if True will overwrite the file if it exists, otherwise it will
                error unless skip_existing is True. Defaults to False.

            skip_existing (bool):
                if jobs where the destination already exists should be skipped by
                default. Default=False
        """
        self._pool = ub.JobPool(mode=mode, max_workers=workers)
        self._unsubmitted = []
        self.eager = eager
        self.skip_existing = skip_existing
        self.overwrite = overwrite

    def __enter__(self):
        self._pool.__enter__()
        return self

    def __len__(self) -> int:
        return len(self._unsubmitted) + len(self._pool)

    def __exit__(self, ex_type, ex_value, ex_traceback):
        """
        Args:
            ex_type (Type[BaseException] | None):
            ex_value (BaseException | None):
            ex_traceback (TracebackType | None):

        Returns:
            bool | None
        """
        return self._pool.__exit__(ex_type, ex_value, ex_traceback)

    def submit(self, src, dst, skip_existing=False, overwrite=None,
               follow_file_symlinks=False, follow_dir_symlinks=False,
               meta='stats'):
        """
        Args:
            src (str | PathLike): source file or directory

            dst (str | PathLike): destination file or directory

            skip_existing (bool | None):
                if jobs where the destination already exists should be skipped by
                default. If None, then uses the class default. Default=None

            overwrite (bool | None):
                if True will overwrite the file if it exists, otherwise it will
                error unless skip_existing is True. If None, then uses the
                class default. Default=None.

            follow_file_symlinks (bool):
                If True and src is a link, the link will be resolved before
                it is copied (i.e. the data is duplicated), otherwise just
                the link itself will be copied.

            follow_dir_symlinks (bool):
                if True when src is a directory and contains symlinks to
                other directories, the contents of the linked data are
                copied, otherwise when False only the link itself is
                copied.

            meta (str | None):
                Indicates what metadata bits to copy. This can be 'stats' which
                tries to copy all metadata (i.e. like :py:func:`shutil.copy2`),
                'mode' which copies just the permission bits (i.e. like
                :py:func:`shutil.copy`), or None, which ignores all metadata
                (i.e.  like :py:func:`shutil.copyfile`).
        """
        if skip_existing is None:
            skip_existing = self.skip_existing
        if overwrite is None:
            overwrite = self.overwrite
        task = {
            'src': src,
            'dst': dst,
            'skip_existing': skip_existing,
            'overwrite': overwrite,
            'follow_file_symlinks': follow_file_symlinks,
            'follow_dir_symlinks': follow_dir_symlinks,
            'meta': meta,
        }
        if self.eager:
            self._pool.submit(_copy_worker, **task)
        else:
            self._unsubmitted.append(task)

    def run(self, desc=None, verbose=1, pman=None):
        """
        Args:
            desc (str | None): description for progress bars
            verbsoe (int): verbosity level
        """
        from kwutil import util_progress
        _our_pman = None
        if pman is None:
            pman = _our_pman = util_progress.ProgressManager(
                backend='progiter')
            _our_pman.__enter__()

        if verbose:
            print('Run copy')

        try:
            for task in self._unsubmitted:
                self._pool.submit(_copy_worker, **task)
            self._unsubmitted.clear()
            job_iter = self._pool.as_completed()
            desc = desc or 'copying'
            prog = pman.progiter(
                job_iter, desc=desc, total=len(self._pool), verbose=verbose)
            for job in prog:
                job.result()
        except Exception as ex:
            if _our_pman is not None:
                _our_pman.__exit__(ex, type(ex), None)
            raise
        finally:
            if _our_pman is not None:
                _our_pman.__exit__(None, None, None)


def _copy_worker(src, dst, skip_existing, overwrite, follow_file_symlinks, follow_dir_symlinks, meta):
    """
    Args:
        str (PathLike | str):
        dst (PathLike | str):
        overwrite (bool):
        skip_existing (bool):
    """
    src = ub.Path(src)
    dst = ub.Path(dst)
    if not skip_existing or not dst.exists():
        dst.parent.ensuredir()
        src.copy(dst, overwrite=overwrite,
                 follow_file_symlinks=follow_file_symlinks,
                 follow_dir_symlinks=follow_dir_symlinks, meta=meta)
