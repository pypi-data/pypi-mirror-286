import os
from   setuptools                     import setup
from   setuptools                     import Extension
from   pybind11                       import get_include


sourceDirectory = os.path.join("src", "CPP Static Library")
pythonDirectory = os.path.join("src", "Python Extension")

setup(
    ext_modules=[
        Extension(
            name="SegmentSignalPy",
            sources=[
                os.path.join(pythonDirectory, file)
                for file in ["module.cpp", "SegmentationResultsPy.cpp"]
            ] + [
                os.path.join(sourceDirectory, file)
                for file in ["SegmentSignalFunctions.cpp", "SegmentationResults.cpp", "SegmentSignal.cpp"]
            ],
            include_dirs=[get_include(), sourceDirectory],
            language="c++",
            extra_compile_args=[]
        )
    ]
)
