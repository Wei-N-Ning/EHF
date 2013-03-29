struct refdef_s
{
  unsigned int x;
  unsigned int y;
  unsigned int width;
  unsigned int height;
  float tanHalfFovX;
  float tanHalfFovY;
  float vieworg[3];
  float viewaxis[3][3];
  float viewOffset[3];
  int time;
  float zNear;
  float blurRadius;
  byte dof[32];
  byte film[44];
  byte glow[20];
  byte primaryLights[16320];
  int localClientNum;
};