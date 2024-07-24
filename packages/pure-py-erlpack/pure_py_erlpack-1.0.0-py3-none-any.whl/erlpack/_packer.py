from erlpack.types import Atom

DEFAULT_RECURSE_LIMIT = 256
BIG_BUF_SIZE = 1024 * 1024 * 2
INITIAL_BUFFER_SIZE = 1024 * 1024
MAX_SIZE = (2 ** 32) - 1
NULL = 0

from .encoder import erlpack_append_int, erlpack_append_nil, erlpack_append_true, erlpack_append_false, erlpack_append_version, erlpack_append_small_integer, erlpack_append_integer, erlpack_append_unsigned_long_long, erlpack_append_long_long, erlpack_append_double, erlpack_append_atom, erlpack_append_atom_utf8, erlpack_append_binary, erlpack_append_string, erlpack_append_tuple_header, erlpack_append_nil_ext, erlpack_append_list_header, erlpack_append_map_header

class EncodingError(Exception):
    pass


class ErlangTermEncoder(object):
    # cdef erlpack_buffer pk
    # cdef char* _encoding
    # cdef char* _unicode_errors
    # cdef char* _unicode_type
    # cdef object _encode_hook
    # cdef bool _in_use

    def __cinit__(self):
        self.pk = b""

    def __init__(self, encoding=b'utf-8', unicode_errors=b'strict', unicode_type=b'binary', encode_hook=None):
        if encoding is None:
            self._encoding = NULL
            self._unicode_errors = NULL
        else:
            if isinstance(encoding, str):
                _encoding = encoding.encode('ascii')
            else:
                _encoding = encoding

            if isinstance(unicode_errors, str):
                _unicode_errors = unicode_errors.encode('ascii')
            else:
                _unicode_errors = unicode_errors

            self._encoding = _encoding.decode("utf-8")
            self._unicode_errors = _unicode_errors.decode("utf-8")

        self._unicode_type = unicode_type
        self._encode_hook = encode_hook
        self._in_use = False

    def _ensure_buf(self):
        """
        Ensures that a buffer is available to be written to when serializing data.

        If there is no buffer, allocate one sized to `INITIAL_BUFFER_SIZE`. If allocation
        fails, raise a MemoryError.
        """
        self.pk = bytearray()
        # if self.pk.buf != NULL:
        #     self.pk.length = 0

        # else:
        #     self.pk.buf = <char*> malloc(INITIAL_BUFFER_SIZE)
        #     if self.pk.buf == NULL:
        #         raise MemoryError('Unable to allocate buffer')

        #     self.pk.allocated_size = INITIAL_BUFFER_SIZE
        #     self.pk.length = 0

    def _free_big_buf(self):
        """
        If the buffer is larger than `BIG_BUF_SIZE`, free it, so that packing large data does not hold onto
        the big buffer after the serialization is complete.
        """
        if len(self.pk) >= BIG_BUF_SIZE:
            self.pk = bytearray()

    def __dealloc__(self):
        del self.pk

    def _pack(self, o, nest_limit=DEFAULT_RECURSE_LIMIT):
        # cdef int ret
        # cdef long long llval
        # cdef unsigned long long ullval
        # cdef long longval
        # cdef double doubleval
        # cdef size_t sizeval
        # cdef dict d
        # cdef object obj

        if nest_limit < 0:
            raise EncodingError('Exceeded recursion limit')

        if o is None:
            ret = erlpack_append_nil(self.pk)

        elif o is True:
            ret = erlpack_append_true(self.pk)

        elif o is False:
            ret = erlpack_append_false(self.pk)

        elif isinstance(o, int):
            if 0 <= o <= 255:
                ret = erlpack_append_small_integer(self.pk, o)

            elif -2147483648 <= o <= 2147483647:
                ret = erlpack_append_integer(self.pk, o)

            else:
                if o > 0:
                    # this assures a overflow error
                    o.to_bytes(8)
                    ret = erlpack_append_unsigned_long_long(self.pk, o)

                else:
                    # this assures a overflow error
                    o.to_bytes(8, signed=True)
                    ret = erlpack_append_long_long(self.pk, o)

        elif isinstance(o, float):
            ret = erlpack_append_double(self.pk, o)

        elif isinstance(o, Atom):
            # TODO: Erlang can support utf-8 atoms, but until all of the
            # clients we know can speak it, we are going to continue sending
            # the latin-1 encoded deprecated style.
            obj = o.encode('latin-1', 'strict')
            ret = erlpack_append_atom(self.pk, obj)

        elif isinstance(o, bytes):
            ret = erlpack_append_binary(self.pk, o)

        elif isinstance(o, str):
            ret = self._encode_unicode(o)

        elif isinstance(o, tuple):
            if len(o) > MAX_SIZE:
                raise ValueError('tuple is too large')

            ret = erlpack_append_tuple_header(self.pk, len(o))
            if ret != 0:
                return ret

            for item in o:
                ret = self._pack(item, nest_limit - 1)
                if ret != 0:
                    return ret

        elif isinstance(o, list):
            sizeval = len(o)
            if sizeval == 0:
                ret = erlpack_append_nil_ext(self.pk)
            else:

                if sizeval > MAX_SIZE:
                    raise ValueError("list is too large")

                ret = erlpack_append_list_header(self.pk, sizeval)
                if ret != 0:
                    return ret

                for item in o:
                    ret = self._pack(item, nest_limit - 1)
                    if ret != 0:
                        return ret

                ret = erlpack_append_nil_ext(self.pk)

        # elif PyDict_CheckExact(o): # TODO: check this is the same as the replacment
        elif isinstance(o, dict):
            sizeval = len(o)

            if sizeval > MAX_SIZE:
                raise ValueError("dict is too large")

            ret = erlpack_append_map_header(self.pk, sizeval)
            if ret != 0:
                return ret

            for k, v in o.items():
                ret = self._pack(k, nest_limit - 1)
                if ret != 0:
                    return ret

                ret = self._pack(v, nest_limit - 1)
                if ret != 0:
                    return ret

        elif hasattr(o, '__erlpack__'):
            obj = o.__erlpack__()
            return self._pack(obj, nest_limit - 1)

        else:
            if self._encode_hook:
                obj = self._encode_hook(o)
                if obj is not None:
                    return self._pack(obj, nest_limit - 1)

            raise NotImplementedError('Unable to serialize %r' % o)

        return ret

    def _encode_unicode(self, obj):
        if not self._encoding:
            return self._pack([ord(x) for x in obj])

        st = obj.encode(self._encoding, self._unicode_errors)
        size = len(st)

        if self._unicode_type == b'binary':
            if size > MAX_SIZE:
                raise ValueError('unicode string is too large using unicode type binary')

            return erlpack_append_binary(self.pk, st)

        elif self._unicode_type == b'str':
            if size > 0xFFF:
                raise ValueError('unicode string is too large using unicode type str')

            return erlpack_append_string(self.pk, st, size)

        else:
            raise TypeError('Unknown unicode encoding type %s' % self._unicode_type)

    def pack(self, obj):
        self._ensure_buf()
        if self._in_use:
            raise RuntimeError("Attempting to reuse an ErlangTermEncoder that is currently encoding something")

        self._in_use = True
        try:
            ret = erlpack_append_version(self.pk)
            if ret == -1:
                raise MemoryError

            ret = self._pack(obj, DEFAULT_RECURSE_LIMIT)
            if ret == -1:
                raise MemoryError
            elif ret:  # should not happen.
                raise TypeError('_pack returned code(%s)' % ret)

            return bytes(self.pk)
        finally:
            self._free_big_buf()
            self._in_use = False

