struct GfxDepthOfField
{
  float viewModelStart;
  float viewModelEnd;
  float nearStart;
  float nearEnd;
  float farStart;
  float farEnd;
  float nearBlur;
  float farBlur;
};
struct GfxFilm
{
  bool enabled;
  float brightness;
  float contrast;
  float desaturation;
  bool invert;
  float tintDark[3];
  float tintLight[3];
};
struct GfxGlow
{
  bool enabled;
  float bloomCutoff;
  float bloomDesaturation;
  float bloomIntensity;
  float radius;
};
struct GfxLight
{
  char type;
  char canUseShadowMap;
  char unused[2];
  float color[3];
  float dir[3];
  float origin[3];
  float radius;
  float cosHalfFovOuter;
  float cosHalfFovInner;
  int exponent;
  unsigned int spotShadowIndex;
  int *def;
};