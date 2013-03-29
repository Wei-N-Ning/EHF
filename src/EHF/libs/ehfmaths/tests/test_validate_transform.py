from EHF.libs.ehfmaths import functions as ehfmaths_functions
from EHF.libs.ehfmaths.types import *

import numpy

def test_validate_transform():
    """
    given the view origin P, and another space point T (for target),
    T is visually in front of P thus its camera space coord should be
    within the screen range
    
    order: right, up, forward

                Vec3 left;
                Vec3 up;
                Vec3 forward;
                Vec3 trans;

    forward ==> right                    ; right = old_forward
    right ==> back ==> forward inverse   ; forward = inverse old_right
    up ==> up                            ; up = old_up
    
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

    """
    pointP = VECTOR4(-104.2033,  147.9466,  689.8074,   1.0)
    pointT = VECTOR4(-108.8845,  147.9466,  680.7183,   1.0)
    
    # note that the origin "right" is left-pointing! and forward is back-pointing
    up = VECTOR4( -0.0158,    0.9992,   -0.0354,       0.0)
    forward = VECTOR4(0.4065,    0.0387,    0.9128,       0.0).scalar_mul(-1)
    right = VECTOR4(0.9135,       0.0,   -0.4069,       0.0).scalar_mul(-1)
    print right
    viewTransformMat = ehfmaths_functions.getViewMatrix(up, right, forward, pointP)
    matT = numpy.matrix([[right.x, right.y, right.z, right.w],
                         [up.x, up.y, up.z, up.w],
                         [forward.x, forward.y, forward.z, forward.w],
                         [pointP.x, pointP.y, pointP.z, 1.0]])
    
    target = numpy.matrix( [[-108.8845,  147.9466,  680.7183,       1.0]] )
    
    # use VECTOR4.multToMat() to transform the point!!!
    # same with numpy, the order of compute transformed vector is: V * M
    pointT_v = pointT.multToMat(viewTransformMat)
    
    print pointT_v
    
if __name__ == "__main__":
    test_validate_transform()