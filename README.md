## sal_pipeline
VFX Pipeline toolset for Graduate project in 2017 : Visual effects, Digital art, Rangsit University

### to do [WIP] :
- [x] Project Explorer
- [ ] Asset importer (wip)
- [ ] Global Publisher
- [ ] scene archive tool
- [ ] Connect pipeline to Project manager platform (Shotgun, TACTIC)

## Usage
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

## Configuration

rename file `configure_default.json` to `configure.json` and setup your project configuration.

I use computer name to mapped with username.

```JSON
{
	"setting": {
		"project_path": "P:/_Project_directory_",
		"project_code": "_Project_code_name_",
		"project_name": "_Project_full_name_"
	},
	"username" :{
		"COMPUTERNAME" : "USERNAME",
		"COMPUTERNAME_1" : "USERNAME_1"
	}
}
```

