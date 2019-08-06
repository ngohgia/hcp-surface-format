from .base_generator import BaseWorkbenchGenerator
import os
import subprocess

class NewSphericalTemplatesGenerator(BaseWorkbenchGenerator):
    def __init__(self, num_vertices, output_dir):
        super(NewSphericalTemplatesGenerator, self).__init__(output_dir)

        assert (num_vertices >= 1000), "The resolution needs to be at least 1000"
        self.num_vertices = num_vertices
        self.right_sphere_file = os.path.join(self.output_dir, "R.sphere.%dk_fs_LR.surf.gii" % (self.num_vertices // 1000))
        self.left_sphere_file = os.path.join(self.output_dir, "L.sphere.%dk_fs_LR.surf.gii" % (self.num_vertices // 1000))

        # the actual number of vertices of the template
        self.true_num_vertices = None

    def generate_spheres(self):
        self.run("surface-create-sphere", "%d %s" % (self.num_vertices, self.right_sphere_file))
        self.run("surface-flip-lr", "%s %s" % (self.right_sphere_file, self.left_sphere_file))
        self.run("set-structure", "%s CORTEX_RIGHT" %(self.right_sphere_file))
        self.run("set-structure", "%s CORTEX_LEFT" %(self.left_sphere_file))

        surf_info = self.run("surface-information", self.right_sphere_file)
        self.true_num_vertices = int(surf_info.split("\n")[2].split()[-1])

        print("New spherical templates created at %s and %s with %d vertices" %
                (self.right_sphere_file, self.left_sphere_file, self.true_num_vertices))
