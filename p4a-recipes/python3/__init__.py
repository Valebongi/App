from pythonforandroid.recipes.python3 import Python3Recipe
from pythonforandroid.util import ensure_dir
from os.path import join


class Python3RecipePinned(Python3Recipe):
    """
    Custom Python3 recipe that disables problematic modules on Android.
    Modules like _uuid and _lzma fail because they depend on libraries
    not available in Android NDK.
    """

    def build_arch(self, arch):
        super().build_arch(arch)
        
        # Create Setup.local to disable problematic modules
        build_dir = self.get_build_dir(arch.arch)
        setup_local_path = join(build_dir, 'Modules', 'Setup.local')
        
        ensure_dir(join(build_dir, 'Modules'))
        
        # Write disabled modules (commented out with *)
        with open(setup_local_path, 'w') as f:
            f.write('# Disable problematic modules for Android\n')
            f.write('*disabled*\n')
            f.write('_uuid\n')
            f.write('_lzma\n')
            f.write('grp\n')


recipe = Python3RecipePinned()
