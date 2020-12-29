from manimlib.imports import *
class ThreeD(SpecialThreeDScene):
    def construct(self):
        sphere = self.get_sphere()
        cube = Cube()
        prism = Prism()
        self.play(ShowCreation(sphere))
        self.play(ReplacementTransform(sphere, cube))
        self.play(ReplacementTransform(cube, prism))
        self.wait(2)
