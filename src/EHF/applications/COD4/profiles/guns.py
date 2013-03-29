"""
$FUNCTION() -> return (px, py)
"""

def M16IronSight(frame):
    return (0, 1)
    
def M16RedDot(frame):
    px, py = 0, 1
    if frame % 2 == 0:
        py += 1
    return (px, py)

# it's stupid but it has to update this list ...
guns = [M16IronSight, M16RedDot]