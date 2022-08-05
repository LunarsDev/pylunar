#### CREDIT NOTICE
#### THIS FILE/CLASS WAS
#### TAKEN DIRECTLY FROM DISCORD.PY
#### THIS IS NOT MY ORIGINAL WORK/CLASS

import os.path
import io

class File:
    r"""A parameter object used for :meth:`abc.Messageable.send`
    for sending file objects.

    .. note::

        File objects are single use and are not meant to be reused in
        multiple :meth:`abc.Messageable.send`\s.

    Attributes
    -----------
    fp: Union[:class:`str`, :class:`io.BufferedIOBase`]
        A file-like object opened in binary mode and read mode
        or a filename representing a file in the hard drive to
        open.

        .. note::

            If the file-like object passed is opened via ``open`` then the
            modes 'rb' should be used.

            To pass binary data, consider usage of ``io.BytesIO``.

    filename: Optional[:class:`str`]
        The filename to display when uploading to Discord.
        If this is not given then it defaults to ``fp.name`` or if ``fp`` is
        a string then the ``filename`` will default to the string given.
    spoiler: :class:`bool`
        Whether the attachment is a spoiler.
    """

    __slots__ = ('fp', 'filename', 'spoiler', '_original_pos', '_owner', '_closer')

    def __init__(self, fp, filename=None, *, spoiler=False):
        self.fp = fp

        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError('File buffer {!r} must be seekable and readable'.format(fp))
            self.fp = fp
            self._original_pos = fp.tell()
            self._owner = False
        else:
            self.fp = open(fp, 'rb')
            self._original_pos = 0
            self._owner = True

        # aiohttp only uses two methods from IOBase
        # read and close, since I want to control when the files
        # close, I need to stub it so it doesn't close unless
        # I tell it to
        self._closer = self.fp.close
        self.fp.close = lambda: None

        if filename is None:
            if isinstance(fp, str):
                _, self.filename = os.path.split(fp)
            else:
                self.filename = getattr(fp, 'name', None)
        else:
            self.filename = filename

        if spoiler and self.filename is not None and not self.filename.startswith('SPOILER_'):
            self.filename = 'SPOILER_' + self.filename

        self.spoiler = spoiler or (self.filename is not None and self.filename.startswith('SPOILER_'))

    def reset(self, *, seek=True):
        # The `seek` parameter is needed because
        # the retry-loop is iterated over multiple times
        # starting from 0, as an implementation quirk
        # the resetting must be done at the beginning
        # before a request is done, since the first index
        # is 0, and thus false, then this prevents an
        # unnecessary seek since it's the first request
        # done.
        if seek:
            self.fp.seek(self._original_pos)

    def close(self):
        self.fp.close = self._closer
        if self._owner:
            self._closer()
