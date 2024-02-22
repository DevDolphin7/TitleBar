import importlib, glob, sys, os


class Data():
    def __init__(self,cleaning=False,pyc=False):
        # Set class variables
        self.packages = []
        self.package_path = []
        self.module_paths = []
        self.module_list = []
        self.cleaning = cleaning
        self.pyc = pyc

        # Adjust current working directory and define the packages and modules
        self.set_cwd()
        self.define_dat_packages()
        self.define_dat_modules()
        self.restore_cwd()

    def set_cwd(self):
        self._original_cwd = os.getcwd()
        os.chdir(os.path.realpath(__file__)[:-11])

    
    def restore_cwd(self):
        os.chdir(self._original_cwd)


    def define_dat_packages(self):
        # Define the packages that are in dat at initialization
        relative_path = "./"
        
        all_dirs = [d[0] for d in os.walk(relative_path)]
        
        for dir_name in all_dirs:
            if dir_name == relative_path: continue
            if not "__" in dir_name:
                self.packages.append(dir_name.replace(".\dat","").replace("\\",""))
                # Add dir_name to sys.path to work after compiled
                sys.path.append(dir_name)

    def define_dat_modules(self):
        # Get dat package module paths
        for package in self.packages:
            self.package_path.append(os.path.dirname(__file__)+"\\"+package)

        # Create a list of modules in the dat packages
        for paths in self.package_path:
            self.all_module_paths = glob.glob(os.path.join(paths, "*.py"))
            for module_path in self.all_module_paths:
                self.module_paths.append(module_path)
        file_ext = -3
        self.module_list = [ os.path.basename(f)[:file_ext] for f in self.module_paths if os.path.isfile(f) and not f.endswith('__init__.py')]

        # Check if any module names appear twice in dat
        if len(set(self.module_list)) < len(self.module_list):
            raise ImportError("Directory \"dat\" contains multiple modules with the same name.")

    def data(self, file_name):
        # Check if file_name is a valid module
        self.set_cwd()
        if not file_name in self.module_list:
            raise ValueError("The given module does not exist in the packages within dat")

        # Import the desired module
        for _ in self.packages:
            try: data_module = importlib.import_module(file_name)
            except ModuleNotFoundError: pass

        # Return the data
        data = data_module.data()
        self.restore_cwd()
        return data
