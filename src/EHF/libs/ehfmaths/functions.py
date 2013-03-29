import math

from EHF.libs.ehfmaths.types import COORD, RECT
from EHF.libs.ehfmaths.types import VECTOR, VECTOR3, VECTOR4
from EHF.libs.ehfmaths.types import CameraTransform
from EHF.libs.ehfmaths.types import MATRIX44, SimpleMatrix


# ---------------------------------------------------------------------
# the following functions implement the slightly lower-level view/projection
# matrix calculation, 
# requires camera/view vectors (up/forward/right) and fov/nz/fz
# ---------------------------------------------------------------------
def getIdMatrix():
    mat = SimpleMatrix()
    mat.setM(0,0, 1.0)
    mat.setM(1,1, 1.0)
    mat.setM(2,2, 1.0)
    mat.setM(3,3, 1.0)
    return mat

    
def getProjectionMatrix(nz, fz, fovH, fovV):
    """
    @param nz: near plane
    @type  nz: float
    
    @param fz: far plane
    @type  fz: float
    
    @param fovH: horizontal fov
    @type  fovH: float
    
    @param fovV: vertical fov
    @type  fovV: float
    
    D3DXMATRIX 
    ProjectionMatrix(const float near_plane, // Distance to near clipping 
                                             // plane
                     const float far_plane,  // Distance to far clipping 
                                             // plane
                     const float fov_horiz,  // Horizontal field of view 
                                             // angle, in radians
                     const float fov_vert)   // Vertical field of view 
                                             // angle, in radians
    {
        float    h, w, Q;
    
        w = (float)1/tan(fov_horiz*0.5);  // 1/tan(x) == cot(x)
        h = (float)1/tan(fov_vert*0.5);   // 1/tan(x) == cot(x)
        Q = far_plane/(far_plane - near_plane);
    
        D3DXMATRIX ret;
        ZeroMemory(&ret, sizeof(ret));
    
        ret(0, 0) = w;
        ret(1, 1) = h;
        ret(2, 2) = Q;
        ret(3, 2) = -Q*near_plane;
        ret(2, 3) = 1;
        return ret;
    }   // End of ProjectionMatrix
    """
    w = 1.0 / math.tan( fovH*0.5 )
    h = 1.0 / math.tan( fovV*0.5 )
    q = fz / ( fz - nz )
    mat = SimpleMatrix()
    mat.setM(0, 0, w)
    mat.setM(1, 1, h)
    mat.setM(2, 2, q)
    mat.setM(3, 2, -1*q*nz)
    mat.setM(2, 3, 1.0)
    return mat


def getViewMatrix(up, right, forward, position):
    mat = SimpleMatrix()
    
    mat.setM(0,0,right.x)
    mat.setM(0,1,up.x)
    mat.setM(0,2,forward.x)
    mat.setM(0,3,0.0)
    
    mat.setM(1,0,right.y)
    mat.setM(1,1,up.y)
    mat.setM(1,2,forward.y)
    mat.setM(1,3,0.0)
    
    mat.setM(2,0,right.z)
    mat.setM(2,1,up.z)
    mat.setM(2,2,forward.z)
    mat.setM(2,3,0.0)
    
    mat.setM(3,0,-position.dotProduct(right))
    mat.setM(3,1,-position.dotProduct(up))
    mat.setM(3,2,-position.dotProduct(forward))
    mat.setM(3,3,1.0)

    return mat


def old_worldToScreenMatrix(worldMatrix, position, scrCenterX, scrCenterY):
    """
    BOOL worldToScreen(D3DXVECTOR3* in, D3DXVECTOR3* out)
    {
        const D3DXMATRIX & m_Screen = *( D3DXMATRIX * )&WORLDRENDER->m_render->WorldTransform;
        D3DXVECTOR3 vOrigin = ( *in );
        FLOAT screenX = static_cast< FLOAT >( ScreenWidth ) / 2.0f;
        FLOAT screenY = static_cast< FLOAT >( ScreenHeight ) / 2.0f;
        FLOAT w = m_Screen.m [0][3] * vOrigin.x +
            m_Screen.m [1][3] * vOrigin.y +
            m_Screen.m [2][3] * vOrigin.z +
            m_Screen.m [3][3];
        if( w < 0.0001f )
            return FALSE;
        FLOAT x =   m_Screen.m [0][0] * vOrigin.x +
            m_Screen.m [1][0] * vOrigin.y +
            m_Screen.m [2][0] * vOrigin.z +
            m_Screen.m [3][0]; 
        FLOAT y =   m_Screen.m [0][1] * vOrigin.x +
            m_Screen.m [1][1] * vOrigin.y +
            m_Screen.m [2][1] * vOrigin.z +
            m_Screen.m [3][1]; 
        out->x = screenX + screenX * x / w;
        out->y = screenY - screenY * y / w;
        return TRUE;
    }
    """
    _w = worldMatrix.getM(0,3) * position.x + worldMatrix.getM(1,3) * position.y + worldMatrix.getM(2,3) * position.z + worldMatrix.getM(3,3)
    if _w < 0.1:
        return None
    _x = worldMatrix.getM(0,0) * position.x + worldMatrix.getM(1,0) * position.y + worldMatrix.getM(2,0) * position.z + worldMatrix.getM(3,0)
    _y = worldMatrix.getM(0,1) * position.x + worldMatrix.getM(1,1) * position.y + worldMatrix.getM(2,1) * position.z + worldMatrix.getM(3,1)
    
    x = scrCenterX + scrCenterX * _x / _w
    y = scrCenterY + scrCenterY * _y / _w
    
    return COORD(x, y)


def worldToScreenMatrix(vProjMatrix, position, scrCenterX, scrCenterY):
    _position = SimpleMatrix()
    _position.setM(0,0,position.x)
    _position.setM(1,0,position.y)
    _position.setM(2,0,position.z)
    _position.setM(3,0,1.0)
    _position = vProjMatrix.multTo(_position)
    if _position.getM(3,0) < 0.001:
        return None
    invW = 1.0/_position.getM(3,0)
    x = (1.0 + _position.getM(0,0) * invW) * scrCenterX
    y = (1.0 + _position.getM(1,0) * invW) * scrCenterY
    z = _position.getM(2,0)
    if z < 0.001:
        return COORD(x,y)
    else:
        return None


# -------------------------------------------------------------------------
# the following two function is based on view axis and view origin,
# such as COD series
# -------------------------------------------------------------------------
def worldToScreenTransform(viewAxisX, viewAxisY, viewAxisZ, origin, target):
    """
    given the three view axis and two vectors, return the screen space transform 
    corresponding to target's world transform
    
    @param origin: viewport origin, ie. the player position
    @type  origin: L{EHF.libs.ehfmaths.VECTOR}
    
    @param target: the world space transform of the object of interests
    @type  target: L{EHF.libs.ehfmaths.VECTOR}
    
    @return: screen space transform
    @rtype : L{EHF.libs.ehfmaths.VECTOR}
    """
    delta = (target - origin).normalize()
    scrTransform = VECTOR3()
    scrTransform.x = delta.dotProduct(viewAxisY)
    scrTransform.y = delta.dotProduct(viewAxisZ)
    scrTransform.z = delta.dotProduct(viewAxisX)
    return scrTransform


def worldToScreen(fovX, fovY, scrCenterX, scrCenterY, viewAxisX, viewAxisY, viewAxisZ, origin, target):
    scrTransform = worldToScreenTransform(viewAxisX, viewAxisY, viewAxisZ, origin, target)
    if scrTransform.z < 0.1:
        return None
    x = scrCenterX * (1 - (scrTransform.x / fovX / scrTransform.z))
    y = scrCenterY * (1 - (scrTransform.y / fovY / scrTransform.z))
    return COORD(x, y)

