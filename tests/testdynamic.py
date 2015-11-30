import numpy as np
from holoviews import Dimension, DynamicMap, Image
from holoviews.element.comparison import ComparisonTestCase

frequencies =  np.linspace(0.5,2.0,5)
phases = np.linspace(0, np.pi*2, 5)
x,y = np.mgrid[-5:6, -5:6] * 0.1

def sine_array(phase, freq):
    return np.sin(phase + (freq*x**2+freq*y**2))



class DynamicTestGeneratorOpen(ComparisonTestCase):

    def test_generator_open_init(self):
        generator = (Image(sine_array(0,i)) for i in range(10))
        dmap=DynamicMap(generator)
        self.assertEqual(dmap.mode, 'open')

    def test_generator_open_stopiteration(self):
        generator = (Image(sine_array(0,i)) for i in range(10))
        dmap=DynamicMap(generator)
        for i in range(9):
            el = next(dmap)
            self.assertEqual(type(el), Image)
        try:
            el = next(dmap)
            raise AssertionError("StopIteration not raised when expected")
        except Exception as e:
            if e.__class__ != StopIteration:
                raise AssertionError("StopIteration was expected, got %s" % e)

    def test_generator_open_iter(self):
        generator = (Image(sine_array(0,i)) for i in range(10))
        dmap=DynamicMap(generator) # One call to next in constructor
        ims = [im for im in dmap]
        self.assertEquals(len(ims), 9)



class DynamicTestCallableOpen(ComparisonTestCase):

    def test_callable_open_init(self):
        fn = lambda i: Image(sine_array(0,i))
        dmap=DynamicMap(fn)
        self.assertEqual(dmap.mode, 'open')



class DynamicTestCallableClosed(ComparisonTestCase):

    def test_callable_closed_init(self):
        fn = lambda i: Image(sine_array(0,i))
        dmap=DynamicMap(fn, kdims=[Dimension('dim', range=(0,10))])
        self.assertEqual(dmap.mode, 'closed')