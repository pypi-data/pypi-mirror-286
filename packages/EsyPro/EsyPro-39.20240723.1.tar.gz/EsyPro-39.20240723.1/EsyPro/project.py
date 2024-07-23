from .path_tool import MyPath


class Project(MyPath):
    #region basic structure
    structure = [
        'myscripts',
        
        'requirements.txt',
        '.gitignore',
        'readme.md',
    ]
    #endregion
    
    @classmethod
    def from_main_file(cls, file=__file__):
        return cls(MyPath(file).get_parent())

    def check_project_structure(self, next=False):
        r = True

        for structure in self.structure:
            path = self.cat(structure)
            if not path.exist():
                r = False
                print('文件(夹)', structure, '不存在')

        if not r:
            return next
        return True
    
    def create_structure(self):

        for structure in self.structure:
            path = self.cat(structure)
            if not path.exist():
                path.ensure()
                print('文件(夹)', structure, '已创建')

        with open(self.cat(self.structure[2]), 'w') as f:
            f.write("""
.*
!.gitignore
**/__*
""")

        with open(self.cat(self.structure[3]), 'w') as f:
            f.write("""
# template

template project: description


## authors

{authors involved into project, if necessary mark contribution behind a name}

## environment

{environment}

## structure

the project follows structure:

```
# this is the root of project
.  
	# path for scripts
	./myscripts  

		# exact script
		./myscripts/.../{script_name}.py 

		# (selectable) path for assets
		./myscripts/.../{script_name}_assets 

		# (selectable) readme file
		./myscripts/.../{script_name}.md 

	# costume packages for project
	./{packages}  

	# git control
	./.gitignore  

	# readme file for project
	./readme.md  

	# enVironment control
	./requirements.txt  

	# init or main
	./main.py  
```

# scripts

            """)

