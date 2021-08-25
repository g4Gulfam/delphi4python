import setuptools, os, sys, platform, shutil

#Force platform wheel
try:
  from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
  class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
      _bdist_wheel.finalize_options(self)
      self.root_is_pure = False
except ImportError:
  bdist_wheel = None 
 
#Find sys/machine file
def buildfilepath():
  ossys = platform.system()
  platmac = platform.machine()
  platmacshort = ""
  sfilename = ""
  print("OS:", ossys, "Machine", platmac)
  if ossys == "Windows":
    sfilename = "DelphiVCL.pyd"
    if platmac.endswith('64'):
      #Win x64	
      platmacshort = "Win64"
    else:
      #Win x86
      platmacshort = "Win32"

  if not platmacshort:
    raise ValueError("Undetermined platform.")
    
  pyversionstrshort = f"{sys.version_info.major}{sys.version_info.minor}"

  return f"DelphiVCL_{platmacshort}_{pyversionstrshort}{os.sep}{sfilename}"

#Copy target file from lib to pkg folder
def copylibfiletopkg(slibfile, spkgfile): 
  spkgdirname = os.path.dirname(spkgfile)
  if not os.path.exists(spkgdirname):
    os.makedirs(spkgdirname)
  shutil.copy(slibfile, spkgfile)
  
  #libdirname = os.path.dirname(slibfile)
  #shutil.rmtree(libdirname)
  
#Validate lib paths
def validatelibpaths(slibdir, slibfile):
  print(f"Check for lib dir: {slibdir}")    
  if not os.path.exists(f"{slibdir}"):
    raise ValueError(f"Invalid lib path: {slibdir}")
    
  print(f"Check for lib path: {slibfile}")
  if not os.path.exists(slibfile):
    raise ValueError(f"Invalid lib path: {slibfile}")
  
#Validate pkg paths
def validatepkgpaths(spkgfile):
  print(f"Check for pkg path: {spkgfile}")
  if not os.path.exists(spkgfile):
    raise ValueError(f"Invalid pkg path: {spkgfile}")
    
#Clear pkg files (trash)
def clearpkgtrashfiles():
  sdir = os.path.join(os.curdir, "delphivcl")
  files = os.listdir(sdir)
  filtered_files = [file for file in files if file.endswith(".so") or file.endswith(".pyd")]
  for file in filtered_files:
    fpath = os.path.join(sdir, file)
    print("Removing trash file:", fpath)
    os.remove(fpath)
    
def isbuildprocess():
  return "bdist_wheel" in sys.argv or "sdist" in sys.argv    
    
def isdistprocess():  
  sdistdir = os.path.join(os.curdir, "dist")
  return os.path.exists(sdistdir)
  
def distprocess():
  sdir = os.path.join(os.curdir, "delphivcl")  
  for fname in os.listdir(sdir):
    if 'DelphiVCL' in fname:
      return os.path.basename(fname)
  return None  
    
def buildprocess():
  spath = buildfilepath()
  sfilename = os.path.basename(spath)
  
  slibdir = os.path.join(os.curdir, "lib")
  slibfile = os.path.join(slibdir, spath)

  spkgdir = os.path.join(os.curdir, "delphivcl")
  spkgfile = os.path.join(spkgdir, sfilename)
 
  clearpkgtrashfiles()	  
  validatelibpaths(slibdir, slibfile)
  copylibfiletopkg(slibfile, spkgfile)
  validatepkgpaths(spkgfile)     
  
  return sfilename
     
sfilename = None  
print("Check for process type") 
if isbuildprocess():  
  print("Found a build process")  
  sfilename = buildprocess()
elif isdistprocess():  
  print("Found a distribution process")
  sfilename = distprocess()
else:
  raise ValueError("Undetermined process type")  
  
print("Working with file: ", sfilename)  
  
"""def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
            
list_files(f"{os.curdir}")"""  

def get_release_version():
    """Creates a new version incrementing by 1 the number of build specified in the
    DelphiVCL-0-01/__version__.py file."""
    lcals = locals()
    gbals = globals()
    with open(os.path.join(os.getcwd(), "delphivcl", "__version__.py"), "rt") as opf:
        opffilecontents = opf.read()
        retvalue = exec(opffilecontents, gbals, lcals)
    versorigstr = lcals["__version__"]
    return versorigstr
    
versnewstr = get_release_version()   

with open("README.md", "r") as fh:
  long_description = fh.read()      

setuptools.setup(
  name="delphivcl",
  version=versnewstr,
  description="Delphi VCL for Python",
  author="Lucas Belo, Jim McKeeth",
  author_email="lucas.belo@live.com",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=["delphivcl"],
  package_data={"delphivcl": [sfilename]},
  classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3 :: Only',
            'Operating System :: Microsoft :: Windows',                        
        ],		
  cmdclass={'bdist_wheel': bdist_wheel},
)
