# sal_pipeline
VFX Pipeline toolset for Graduate project in 2017 : Visual effects, Digital art, Rangsit University

# Usage
Install this repository and connect by this python script:

```python
import sys

toolPath = 'C:/Path/To/repository'

if toolPath not in sys.path :
	sys.path.append(toolPath)

from sal_pipeline import salPipeline
reload(salPipeline)

# your app name
salPipeline.app_projectExplorer()
```
