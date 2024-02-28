# Python Project Template

The purpose of this project is to maintain my personal **`Python project templates`** that I commonly use.

Main functions are as follows:

- Automatically creates and manages a virtualenv for your projects by [pipenv](https://github.com/pypa/pipenv)
- Python code formatter [black](https://github.com/psf/black)
- Sort your python project imports by [isort](https://github.com/PyCQA/isort)
- Static code analysis by [pylint](https://github.com/PyCQA/pylint)

> It's recommended that you use [vscode](https://code.visualstudio.com/) to develop your projects.

Execute the following command in the terminal to get started quickly:

```shell
# Assuming you are already using conda to manage your python environment
conda create -n python3.10 python=3.10
# Clone repository
git clone https://github.com/howie6879/py_project_template your_project_name
cd your_project_name
# Remove .git
rm -Rf .git

# Install python env for your project
pipenv install --python ~/anaconda3/envs/python38/bin/python3.10 --skip-lock --dev
# Start coding
```

BTW, For my insights on python project development management you can read this article: [浅谈Python项目开发&管理](https://www.howie6879.cn/post/2021/14_about_python_env/).
