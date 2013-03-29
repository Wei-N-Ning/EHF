import math

from ctypes import Structure
from ctypes import c_float
from ctypes import c_int

from EHF.core import win32types


class COORD(Structure):
    """
    represents a coord
    """
    _fields_ = [ ("x", c_float),
                 ("y", c_float) ]
    

class RECT(Structure):
    """
    represents a rect
    """
    _fields_ = [ ("left", c_int),
                 ("top", c_int),
                 ("right", c_int),
                 ("bottom", c_int) ]


class VECTOR(Structure):
    """
    a C-Vector class, 
    can be used directly in rpm(), 
    
    it's not suggested to pass this type of object in and out of the pipeline,
    use the pure python version VECTOR3 instead.
    
    call toPyVector3() to convert this type to the pure python type
    """
    _fields_ = [ ("x", c_float),
                 ("y", c_float),
                 ("z", c_float) ]
    
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dotProduct(self, dot):
        return self.x*dot.x + self.y*dot.y + self.z*dot.z;
    
    def scalar_mul(self, multiplier):
        return VECTOR(self.x * multiplier, self.y * multiplier, self.z * multiplier)
    
    def __add__(self, other):
        return VECTOR(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return VECTOR(self.x-other.x, self.y-other.y, self.z-other.z)
    
    def __str__(self):
        return "<%f, %f, %f>" % (self.x, self.y, self.z)
    
    def __repr__(self):
        return self.__str__()
    
    def toPyVector3(self):
        return VECTOR3(self.x, self.y, self.z)
    
    def toPyVector4P(self):
        return VECTOR4(self.x, self.y, self.z, 1.0)
    
    def toPyVector4D(self):
        return VECTOR4(self.x, self.y, self.z, 0.0)
    
    

class VECTOR3(object):
    """
    represents a 3-dimensional vector
    """
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dotProduct(self, dot):
        return self.x*dot.x + self.y*dot.y + self.z*dot.z;
    
    def crossProduct(self, other):
        nx = self.y*other.z - other.y*self.z
        ny = self.z*other.x - other.z*self.x
        nz = self.x*other.y - other.x*self.y
        return VECTOR3(nx, ny, nz)
    
    def multToMat(self, mat):
        nx = self.x*mat.getM(0,0) + self.y*mat.getM(1,0) + self.z*mat.getM(2,0) + mat.getM(3,0)
        ny = self.x*mat.getM(0,1) + self.y*mat.getM(1,1) + self.z*mat.getM(2,1) + mat.getM(3,1)
        nz = self.x*mat.getM(0,2) + self.y*mat.getM(1,2) + self.z*mat.getM(2,2) + mat.getM(3,2)
        return VECTOR3(nx, ny, nz)

    def scalar_mul(self, multiplier):
        return VECTOR3(self.x * multiplier, self.y * multiplier, self.z * multiplier)

    def normalize(self):
        length = self.length()
        nx = self.x/length
        ny = self.y/length
        nz = self.z/length
        return VECTOR3(nx, ny, nz)
    
    def toPointVector4(self):
        return VECTOR4(self.x, self.y, self.z, 1.0)
    
    def toDirectionVector4(self):
        return VECTOR4(self.x, self.y, self.z, 0.0)
    
    def __add__(self, other):
        return VECTOR3(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return VECTOR3(self.x-other.x, self.y-other.y, self.z-other.z)
    
    def __str__(self):
        return "<%f, %f, %f>" % (self.x, self.y, self.z)
    
    def __repr__(self):
        return self.__str__()
    

class VECTOR4(object):
    """
    represents a 4-dimensional vector.
    
    this type is required for frostbite engine games
    """
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    def __str__(self):
        return "<%f, %f, %f, %f>" % (self.x, self.y, self.z, self.w)
    
    def __repr__(self):
        return self.__str__()
    
    def multToMat(self, mat):
        nx = self.x*mat.getM(0,0) + self.y*mat.getM(1,0) + self.z*mat.getM(2,0) + self.w*mat.getM(3,0)
        ny = self.x*mat.getM(0,1) + self.y*mat.getM(1,1) + self.z*mat.getM(2,1) + self.w*mat.getM(3,1)
        nz = self.x*mat.getM(0,2) + self.y*mat.getM(1,2) + self.z*mat.getM(2,2) + self.w*mat.getM(3,2)
        nw = self.x*mat.getM(0,3) + self.y*mat.getM(1,3) + self.z*mat.getM(2,3) + self.w*mat.getM(3,3)
        return VECTOR4(nx, ny, nz, nw)

    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z + self.w*self.w)
    
    def _length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dotProduct(self, dot):
        return self.x*dot.x + self.y*dot.y + self.z*dot.z + self.w*dot.w;
    
    def crossProduct(self, other):
        """
        NOTE cross product should ONLY apply to directional vector not Points!!
        and since it only applies to vector, we can safely set nw to 0.0
        """
        nx = self.y*other.z - other.y*self.z
        ny = self.z*other.x - other.z*self.x
        nz = self.x*other.y - other.x*self.y
        nw = 0.0
        return VECTOR4(nx, ny, nz, nw)
    
    def scalar_mul(self, multiplier):
        return VECTOR4(self.x * multiplier, self.y * multiplier, self.z * multiplier, self.w * multiplier)

    def normalize(self):
        """
        NOTE normalization should only apply to directional vector
        """
        length = self.length()
        nx = self.x/length
        ny = self.y/length
        nz = self.z/length
        nw = self.w/length
        return VECTOR4(nx, ny, nz, nw)
    
    def toPointVector4(self):
        return VECTOR4(self.x, self.y, self.z, 1.0)
    
    def toDirectionVector4(self):
        return VECTOR4(self.x, self.y, self.z, 0.0)
    
    def __add__(self, other):
        return VECTOR4(self.x+other.x, self.y+other.y, self.z+other.z, self.w+other.w)
    
    def __sub__(self, other):
        return VECTOR4(self.x-other.x, self.y-other.y, self.z-other.z, self.w-other.w)
    

    
class CameraTransform(Structure):
    """
    represents a complete camera(view) transform.
    
    the C/C++ version of this structure implements a union of 
    4 sets of VECTOR4 and an array of 16 floats
     
    it can be used directly in rpm to get the *linerTransform* (BF3/ MOHW)
    the 4 sets of VECTOR4 are right, up, forward, trans
    
    * i think trans is the eye position
    """
    _fields_ = [ ("arr", c_float * 16) ]
    
    def getRightVec4(self):
        return VECTOR4(self.arr[0], self.arr[1], self.arr[2], self.arr[3])
    def getRightVec3(self):
        return VECTOR3(self.arr[0], self.arr[1], self.arr[2])
    
    def getUpVec4(self):
        return VECTOR4(self.arr[4], self.arr[5], self.arr[6], self.arr[7])
    def getUpVec3(self):
        return VECTOR3(self.arr[4], self.arr[5], self.arr[6])
    
    def getForwardVect4(self):
        return VECTOR4(self.arr[8], self.arr[9], self.arr[10], self.arr[11])
    def getForwardVect3(self):
        return VECTOR3(self.arr[8], self.arr[9], self.arr[10])
        
    def getTransVect4(self):
        return VECTOR4(self.arr[12], self.arr[13], self.arr[14], self.arr[15])
    def getTransVect3(self):
        return VECTOR3(self.arr[12], self.arr[13], self.arr[14])
    
    
class MATRIX44(Structure):
    """
    simulates a D3DXMATRIX class.
    
    it's not suggested to pass this type of object in and out of the pipeline, 
    use the pure python version SimpleMatrix instead.
    """
    _fields_ = [ ("arr",   win32types.c_float * 16) ]
    
    def toPySimpleMatrix(self):
        return SimpleMatrix(self)
    
    def toArray(self):
        array = [ [0.0 for i in range(4)] for j in range(4) ]
        count = 0
        for i in range(4):
            for j in range(4):
                array[j][i] = self.arr[count]
                count += 1
        return array
    
    def toList(self):
            mat = []
            count = 0
            row = []
            for entry in self.arr:
                if count and count % 4 == 0:
                    # start a new row
                    mat.append(row)
                    row = []
                row.append(entry)
                count += 1
            mat.append(row)
            return mat
    
    def m(self, row, column):
        return self.arr[row*4+column]
    
    
class SimpleMatrix(object):
    """
    represents a 4x4 matrix
    
    use getM() and setM() to access to the individual entry
    """
    def __init__(self, cMatrix=None):
        """
        initialize from a MATRIX44 structure or use the default constructor
        """
        if cMatrix:
            self.data = [entry for entry in cMatrix.arr]
        else:
            self.data = [0.0 for i in range(16)]
            
    def getM(self, row, column):
        return self.data[row*4+column]
    
    def setM(self, row, column, value):
        self.data[row*4+column] = value
    
    def toString(self):
        return '\n'.join( [ ' '.join( ["%.4f"%self.getM(i,j) for j in range(4)] ) for i in range(4) ] )
    
    def __str__(self):
        return self.toString()
    
    def __repr__(self):
        return self.toString()
    
    def multTo(self, other):
        result = SimpleMatrix()
        for row_index in range(4):
            for column_index in range(4):
                newEntry = sum( [self.getM(row_index, _k)*other.getM(_k, column_index) for _k in range(4)] )
                result.setM(row_index, column_index, newEntry)
        return result
    
    def multToVec4(self, vec4):
        x = self.getM(0,0) * vec4.x + self.getM(0,1) * vec4.y + self.getM(0,2) * vec4.z + self.getM(0,3) * vec4.z
        y = self.getM(1,0) * vec4.x + self.getM(1,1) * vec4.y + self.getM(1,2) * vec4.z + self.getM(1,3) * vec4.z
        z = self.getM(2,0) * vec4.x + self.getM(2,1) * vec4.y + self.getM(2,2) * vec4.z + self.getM(2,3) * vec4.z
        w = self.getM(3,0) * vec4.x + self.getM(3,1) * vec4.y + self.getM(3,2) * vec4.z + self.getM(3,3) * vec4.z
        return VECTOR4(x, y, z, w)