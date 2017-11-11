## sal_pipeline
VFX Pipeline toolset for Graduate project in 2017 : Visual effects, Digital art, Rangsit University

### to do [WIP] :
- [x] Project Explorer
- [ ] Asset importer (wip)
- [ ] Global Publisher
- [ ] scene archive tool
- [ ] Connect pipeline to Project manager platform (Shotgun, TACTIC)

## Usage
1) Install this repository in your computer.
2) Copy prefs folder to ```Documents\maya\2016\prefs```
3) Open Maya then load sal_pipeline shelf.
4) Add `SAL_MODULE_PATH` to `Maya.env` 

```SAL_MODULE_PATH = Path:/To/sal_pipeline_repo```

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

