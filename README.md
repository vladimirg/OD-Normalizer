# Instructions for Windows exe build

1. Start with a minimal environment (miniconda3 works OK).
1. Note that in Anaconda defaults numpy is compiled against MKL, which is huge. Instead, install the numpy that works with OpenBLAS, as suggested [here]( https://stackoverflow.com/questions/45722188/tutorial-for-installing-numpy-with-openblas-on-windows).

	>conda create -n openblas python=3.8
conda activate openblas
conda install conda-forge::blas=*=openblas
conda install -c conda-forge numpy

	Apparently, installing with pip also works (and is often recommended when using Pyinstaller).
1. Install the rest of the relevant packages (pandas, openpyxl, gooey, pyinstaller).
1. Generate a build spec with:
	>pyi-makespec --windowed --onefile --collect-submodules openpyxl od_normalizer.py
	
	NB 1:  `--collect-submodules openpyxl` was added since some of its necessary submodules were missing in previous builds and led to crashes.
	
	NB 2: `--onefile` is better for distribution, but may be slower on start up, and hides the imports (if debugging the build is required). Alternatively can build with `--onedir`.
	
1. Download and extract UPX (optional, reduces EXE size).
1. Run pyinstaller with:
	>pyinstaller -y --upx-dir=C:\dev\upx-4.2.3-win64 od_normalizer.spec
