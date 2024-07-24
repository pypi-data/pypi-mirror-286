import ctypes

FORMAT_VERSION = 131
NEW_FLOAT_EXT = ord('F')       # 70  [Float64:IEEE float]
BIT_BINARY_EXT = ord('M')      # 77  [UInt32:Len, UInt8:Bits, Len:Data]
COMPRESSED = ord('P')          # 80  [UInt4:UncompressedSize, N:ZlibCompressedData]
SMALL_INTEGER_EXT = ord('a')   # 97  [UInt8:Int]
INTEGER_EXT = ord('b')         # 98  [Int32:Int]
FLOAT_EXT = ord('c')           # 99  [31:Float String] Float in string format (formatted "%.20e", sscanf "%lf"). Superseded by NEW_FLOAT_EXT
ATOM_EXT = ord('d')            # 100 [UInt16:Len, Len:AtomName] max Len is 255
REFERENCE_EXT = ord('e')       # 101 [atom:Node, UInt32:ID, UInt8:Creation]
PORT_EXT = ord('f')            # 102 [atom:Node, UInt32:ID, UInt8:Creation]
PID_EXT = ord('g')             # 103 [atom:Node, UInt32:ID, UInt32:Serial, UInt8:Creation]
SMALL_TUPLE_EXT = ord('h')     # 104 [UInt8:Arity, N:Elements]
LARGE_TUPLE_EXT = ord('i')     # 105 [UInt32:Arity, N:Elements]
NIL_EXT = ord('j')             # 106 empty list
STRING_EXT = ord('k')          # 107 [UInt16:Len, Len:Characters]
LIST_EXT = ord('l')            # 108 [UInt32:Len, Elements, Tail]
BINARY_EXT = ord('m')          # 109 [UInt32:Len, Len:Data]
SMALL_BIG_EXT = ord('n')       # 110 [UInt8:n, UInt8:Sign, n:nums]
LARGE_BIG_EXT = ord('o')       # 111 [UInt32:n, UInt8:Sign, n:nums]
NEW_FUN_EXT = ord('p')         # 112 [UInt32:Size, UInt8:Arity, 16*Uint6-MD5:Uniq, UInt32:Index, UInt32:NumFree, atom:Module, int:OldIndex, int:OldUniq, pid:Pid, NunFree*ext:FreeVars]
EXPORT_EXT = ord('q')          # 113 [atom:Module, atom:Function, smallint:Arity]
NEW_REFERENCE_EXT = ord('r')   # 114 [UInt16:Len, atom:Node, UInt8:Creation, Len*UInt32:ID]
SMALL_ATOM_EXT = ord('s')      # 115 [UInt8:Len, Len:AtomName]
MAP_EXT = ord('t')             # 116 [UInt32:Airty, N:Pairs]
FUN_EXT = ord('u')             # 117 [UInt4:NumFree, pid:Pid, atom:Module, int:Index, int:Uniq, NumFree*ext:FreeVars]
ATOM_UTF8_EXT = ord('v')       # 118 [UInt16:Len, Len:AtomName] max Len is 255 characters (up to 4 bytes per)
SMALL_ATOM_UTF8_EXT = ord('w') # 119 [UInt8:Len, Len:AtomName]


def erlpack_append_small_atom_ext(pk: bytearray, b: bytes):
	pk.extend([SMALL_ATOM_EXT, len(b)])
	pk.extend(b)
	return 0

def erlpack_append_nil(pk: bytearray)->int:
	return erlpack_append_small_atom_ext(pk, b"nil")
def erlpack_append_true(pk: bytearray)->int:
	return erlpack_append_small_atom_ext(pk, b"true")
def erlpack_append_false(pk: bytearray)->int:
	return erlpack_append_small_atom_ext(pk, b"false")

def erlpack_append_small_integer(pk: bytearray, d: int)->int:
	pk.extend([SMALL_INTEGER_EXT, d])
	return 0
class asUnsigned(ctypes.Union):_fields_=[
	("i32",ctypes.c_int32),
	("u32",ctypes.c_uint32)
]
def erlpack_append_integer(pk: bytearray, d: int)->int:
	pk.append(INTEGER_EXT)
	pun = asUnsigned()
	pun.i32 = d
	pk.extend(pun.u32.to_bytes(4, "big"))
	return 0
def erlpack_append_unsigned_long_long(pk: bytearray, d: int)->int:
	pk.append(SMALL_BIG_EXT)
	buf = []
	while (d > 0):
		buf.append(d & 0xFF)
		d >>= 8
	pk.append(len(buf))
	pk.append(0)
	pk.extend(buf)
	return 0
def erlpack_append_long_long(pk: bytearray, d: int)->int:
	pk.append(SMALL_BIG_EXT)
	ull = -d if d < 0 else d
	buf = []
	while (ull > 0):
		buf.append(ull & 0xFF)
		ull >>= 8
	pk.append(len(buf))
	pk.append(1 if d < 0 else 0)
	pk.extend(buf)
	return 0

class typePunner(ctypes.Union):_fields_=[
	("ui64",ctypes.c_uint64),
	("df",ctypes.c_double)
]
def erlpack_append_double(pk: bytearray, f: float)->int:
	pk.append(NEW_FLOAT_EXT)
	p =typePunner()
	p.df = f
	pk.extend(p.ui64.to_bytes(8, "big"))
	return 0

def erlpack_append_atom(pk: bytearray, b: bytes)->int:
	if (len(b) < 255): return erlpack_append_small_atom_ext(pk, b)

	pk.append(ATOM_EXT)
	if (len(b) > 0xFFFF): return 1
	
	pk.extend(len(b).to_bytes(2, "big"))
	pk.extend(b)
	return 0

def erlpack_append_binary(pk: bytearray, b: bytes)->int:
	pk.append(BINARY_EXT)
	pk.extend(len(b).to_bytes(4, "big"))
	pk.extend(b)
	return 0

def erlpack_append_tuple_header(pk: bytearray, length: int)->int:
	if (length < 256): pk.extend([SMALL_TUPLE_EXT, length])
	else:
		pk.append(LARGE_TUPLE_EXT)
		pk.extend(length.to_bytes(4, "big"))
	return 0

def erlpack_append_nil_ext(pk: bytearray)->int:
	pk.append(NIL_EXT)
	return 0

def erlpack_append_list_header(pk: bytearray, length: int)->int:
	pk.append(LIST_EXT)
	pk.extend(length.to_bytes(4, "big"))
	return 0

def erlpack_append_map_header(pk: bytearray, length: int)->int:
	pk.append(MAP_EXT)
	pk.extend(length.to_bytes(4, "big"))
	return 0

def erlpack_append_version(pk: bytearray)->int:
	pk.append(FORMAT_VERSION)
	return 0


def erlpack_append_string(pk: bytearray, b: bytes)->int:
	pk.append(STRING_EXT)
	pk.extend(len(b).to_bytes(2, "big"))
	pk.extend(b)
	return 0

#dummy as unused
erlpack_append_int=0
erlpack_append_atom_utf8=0
