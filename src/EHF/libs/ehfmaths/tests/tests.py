from EHF.libs.ehfmaths import functions as ehfmaths_functions
from EHF.libs.ehfmaths.types import *


def simpleTest1():
    proj = ehfmaths_functions.getProjectionMatrix(nz=0.06, fz=2000.0601, fovH=1.2870, fovV=1.8546)
    print proj
#    idMat = SimpleMatrix()
#    idMat.setM(0,0,1.0)
#    idMat.setM(1,1,1.0)
#    idMat.setM(2,2,1.0)
#    idMat.setM(3,3,1.0)
    a = VECTOR3(0.0, 0.0, 1.0)
    b = VECTOR3(1.0, 0.0, 0.0)
    #   0.0       0.0       0.0    1.0000    0.9177       0.0   -0.3972       0.0
    #   -0.0366    0.9957   -0.0847       0.0    0.3955    0.0923    0.9138       0.0
    #   -123.5014   60.9055 -183.5093       0.0       0.0       inf    1.2870    0.9599
    upVec = VECTOR3(-0.0366,    0.9957,   -0.0847)
    forwardVec = VECTOR3(0.3955,    0.0923,    0.9138)
    transVec = VECTOR3(-123.5014,   60.9055, -183.5093)
    #print x
    #print y
    #print z
    viewM = ehfmaths_functions.getViewMatrix(forwardVec, transVec, upVec)
    print "\n\n", viewM
    
    print "\n\n", proj.multTo(viewM)
    


def testPerpendicular():
    """
    NOTE: the dot product in theory should produce 0, but because the 
    original dumped floats is rounded to have only 4 decimal point precision, 
    thus we won't get the perfect result here!!
    """
    upVec = VECTOR3(-0.0366,    0.9957,   -0.0847)
    forwardVec = VECTOR3(0.3955,    0.0923,    0.9138)
    leftVec = VECTOR3( 0.9177,       0.0,   -0.3972)
    print "up . forward: ", round(upVec.dotProduct(forwardVec), 8)
    print "up . left: ", round(upVec.dotProduct(leftVec), 8)
    print "left . forward: ", round(leftVec.dotProduct(forwardVec), 8)


def testMatrixSetM():
    mat = SimpleMatrix()
    mat.setM(0,0, 3.0)
    mat.setM(1,0, 4.0)
    mat.setM(2,0, 5.0)
    mat.setM(3,0, 1.0)
    
    mat2 = ehfmaths_functions.getIdMatrix()
    mat2.setM(2,0, 3.14)
    
    print mat.multTo(mat2)
    print mat2.multTo(mat)

def testMatrixMult():
    """
    vec * mat1 * mat2 * mat3 == vec * (mat1 * mat2 * mat3) ???
    """
    import random
    vec = VECTOR3(31.1, -19.18, 18.44)
    print vec, "\n"
    
    mat1 = SimpleMatrix()
    [mat1.setM(i/4, i%4, random.randint(1,15)/13.05) for i in range(16)]
    print mat1, "\n"
    
    mat2 = SimpleMatrix()
    [mat2.setM(i/4, i%4, random.randint(1,15)/11.81) for i in range(16)]
    print mat2, "\n"
    
    mat3 = SimpleMatrix()
    [mat3.setM(i/4, i%4, random.randint(1,15)/12.34) for i in range(16)]
    print mat3, "\n"
    
    print "\n\n==========="

    print vec.multToMat(mat1).multToMat(mat2).multToMat(mat3)
    
    print "\n"
    
    print vec.multToMat( mat1.multTo(mat2).multTo(mat3) )

def testNormalization():
    upVec = VECTOR3(-0.0366,    0.9957,   -0.0847)
    forwardVec = VECTOR3(0.3955,    0.0923,    0.9138)
    leftVec = VECTOR3( 0.9177,       0.0,   -0.3972)
    
    upVecS = upVec.scalar_mul(10)
    upVecN = upVec.normalize()
    
    print upVec.dotProduct(forwardVec)
    print upVecS.dotProduct(forwardVec)
    print upVecN.dotProduct(forwardVec)
    
def validateViewVectors():
    """
    viewVector order: right, up, forward
    
    before
    0.8378       0.0   -0.5460       0.0   -0.0826    0.9885   -0.1268       0.0
    0.5397    0.1513    0.8281       0.0  279.9696{174.6449}{-288.8244}       0.0
    
    after
    0.7948       0.0   -0.6069       0.0   -0.0532    0.9961   -0.0697       0.0
    0.6045    0.0877    0.7917       0.0  270.6172  174.6037 -301.0818       0.0
    """
    viewOriginBefore = VECTOR3(279.9696, 174.6449, -288.8244)
    
    
    viewOriginAfter = VECTOR3(270.6172,  174.6037, -301.0818)
    
    print (viewOriginBefore - viewOriginAfter).normalize()
    

def validateWorldAxis():
    """
    order: right, up, forward
    
    forward:
    before
    0.9135       0.0   -0.4069       0.0   -0.0158    0.9992   -0.0354       0.0
    0.4065    0.0387    0.9128       0.0 -104.2033  147.9466  689.8074       0.0
    after
    0.8917       0.0   -0.4526       0.0   -0.0229    0.9987   -0.0452       0.0
    0.4520    0.0506    0.8906       0.0 -108.8845  147.9466  680.7183       0.0
    
    right:                                                
    before
    0.9399       0.0   -0.3415       0.0   -0.0061    0.9998   -0.0168       0.0
    0.3414    0.0179    0.9397       0.0 -109.5459  147.9466  684.5769       0.0
    after
    0.9409       0.0   -0.3387       0.0   -0.0086    0.9997   -0.0238       0.0
    0.3386    0.0253    0.9406       0.0 -103.3640  147.9466  682.3727       0.0
    
    left:
    before
    0.9149       0.0   -0.4037       0.0   -0.0168    0.9991   -0.0382       0.0
    0.4033    0.0417    0.9141       0.0 -103.4697  147.9466  678.8103       0.0
    after
    0.9149       0.0   -0.4037       0.0   -0.0168    0.9991   -0.0382       0.0
    0.4033    0.0417    0.9141       0.0{-111.3338}{147.9466}{682.2825}       0.0
    
    
    COD4 view axis:
   
    forward:
    before
 4332.6313-6581.7788   60.1250   x -0.9988   -0.0230    0.0441   y 0.0230   -0.9997 0.0   z  0.0441    0.0010    0.9990 4332.6313-6581.7788   60.1250       0.0
    after:
 3717.5200-6583.9316   60.1250   x -0.9995   -0.0127    0.0287   y 0.0128   -0.9999 0.0   z  0.0287    0.0004    0.9996 3717.5200-6583.9316   60.1250       0.0
     
    right:
    before
 3717.5200-6583.9316   60.1250   -0.9995   -0.0281    0.0127    0.0281   -0.9996
       0.0    0.0127    0.0004    0.9999 3717.5200-6583.9316   60.1250       0.0
    after:
 3714.4236-6104.6191   61.7635   -0.9985   -0.0537   -0.0105    0.0537   -0.9986
       0.0   -0.0104   -0.0006    0.9999 3714.4236-6104.6191   61.7635       0.0
    
    """
    # test forward
#    forwardBefore = VECTOR3(4332.6313,-6581.7788,   60.1250)
#    forwardAfter = VECTOR3(3717.5200,-6583.9316,   60.1250)
#    print (forwardBefore-forwardAfter).normalize()
#    # test right
#    # it turns out the *RIGHT* view vector is actually LEFT-pointing!!!
#    rightBefore = VECTOR3(-109.5459,  147.9466,  684.5769)
#    rightAfter = VECTOR3(-103.3640,  147.9466,  682.3727)
#    result= (rightBefore-rightAfter).normalize()
#    print result
#    # test left:
#    leftBefore = VECTOR3(-103.4697,  147.9466,  678.8103)
#    leftAfter = VECTOR3(-111.3338,  147.9466,  682.2825)
#    print (leftBefore-leftAfter).normalize()
    
    # test COD4 forward (z)
    forwardBefore = VECTOR3(4313.0508,-6593.6685,   60.1250)
    forwardAfter = VECTOR3(3752.8669,-6610.1543,   60.1250)
    print (forwardBefore-forwardAfter).normalize()
    
    # test COD4 right (x)
    rightBefore = VECTOR3( 3717.5200,-6583.9316,   60.1250)
    rightAfter = VECTOR3( 3714.4236,-6104.6191,   61.7635 )
    print (rightBefore-rightAfter).normalize()
    
if __name__ == "__main__":
    #simpleTest1()
    #testPerpendicular()
    #testMatrixSetM()
    #testMatrixMult()
    #testNormalization()
    #validateViewVectors()
    validateWorldAxis()