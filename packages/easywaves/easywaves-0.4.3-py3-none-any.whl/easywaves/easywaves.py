# from .curves import curves as c
import numpy as np
from .curves import Curves, npCurves

def ease(currentTime, beginValue, changeValue, duration, easingFunction=Curves.cubicIn):

    if currentTime <= 0:
        return beginValue
    elif currentTime >= duration:
        return beginValue + changeValue
    
    progress = easingFunction(currentTime / duration)
    
    currentValue = beginValue + progress * changeValue
    
    return currentValue


def ease_map(inValue, inMin, inMax, outMin, outMax, easingFunction=Curves.cubicIn):
    
    changeValue = outMax - outMin
    duration = inMax - inMin
    
    return ease(inValue, outMin, changeValue, duration, easingFunction)


def ease_map_np(inMin, inMax, outMin, outMax, easingFunction=npCurves.cubicInOut, resolution=0.1):
    
    points = (outMax - outMin) / resolution
    t = np.linspace(inMin, inMax, points)
    t = easingFunction(t)


def ease_array(startY, endY, length, easing_func):
    t = np.linspace(0, 1, length)
    eased_t = easing_func(t)
    return startY + (endY - startY) * eased_t


def ease_xy(fromXY, toXY, easingFunction=npCurves.circInOut, resolution=0.1):
    
    point1 = np.array(fromXY)
    point2 = np.array(toXY)
    distance = np.sqrt(np.sum((point2 - point1)**2))
    
    t = np.linspace(0, 1, int(distance / resolution))
    t = easingFunction(t)

    interpolated_x = toXY[0] + t * (fromXY[0] - toXY[0])
    interpolated_y = toXY[1] + t * (fromXY[1] - toXY[1])

    return np.column_stack((interpolated_x, interpolated_y))


def wave(x, easingFunction):
    # ensure that 0 to 1 = a full wave
    x *= 2
    # ensure that the wave starts on zero
    x -= 0.5
    # modulus to repeat wave
    x = x % 2.0
    
    x = np.where(x > 1, 2 - x, x)
    
    x = 2 * easingFunction(x) - 1
    
    return x
