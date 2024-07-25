import inquirer
import os

from bluedac.utils.save_config import save_config

def init():
    # Checks if user declared project name containing '.' or '/'.
    while True:
        repo_name: str = input("Insert repository name: ")

        if any(punct in repo_name for punct in [".", "/"]):
            print("Invalid input. Avoid using '.' or '/' in repository's name.")
        else:
            break

    # -------------------- Language selection -------------------- #
    languages = [
        inquirer.List(
            "language",
            message="Select project's main programming language:",
            choices=["Python", "Javascript", "Typescript", "Go", "Java", "C#"],
        ),
    ]
    language: str = inquirer.prompt(languages)["language"]

    # C# converted to csharp in CDK init, else the lowercase version of the choice.
    language = "csharp" if language == "C#" else language.lower()

    # -------------------- Branching strategy selection -------------------- #
    branching_strategies = [
        inquirer.List(
            "branching_strategy",
            message="What branching strategy do you want to use?",
            choices=["Trunk Based Development", "GitFlow"],
        ),
    ]
    branching_strategy: str = inquirer.prompt(branching_strategies)["branching_strategy"]

    # Name refactoring
    branching_strategy = "tbd" if branching_strategy == "Trunk Based Development" else "gitflow"

    try:
        # Create project directory and cd into it.
        project_dir_path: str = f"{os.getcwd()}/{repo_name}"
        os.mkdir(project_dir_path)
        os.chdir(project_dir_path)
    except FileExistsError:
        print(f"Error. Directory '{repo_name}' already exists.")
        exit()

    # Launching CDK init command to initialize project structure.
    os.system(f"cdk init app --language {language} 2>/dev/null")

    # Create BlueDAC configuration and save it to 'bluedac_config.json'.
    save_config(repo_name, language, branching_strategy)

    # -------------- Adding dependencies -------------- #
    with open("requirements.txt", "w") as reqs:
        reqs.write("bluedac \n")

    print(f" \
Repository {repo_name} initialized with {language} as programming language. \n \
Your project's configuration has been defined in {os.getcwd()}/bluedac_config.json. \n \n \
Next steps: \n \
1. Inspect {os.getcwd()}/{repo_name}/bluedac_config.json for eventual misconfigurations. \n \
2. 'dac confirm' to confirm your project's configuration. \n \
3. 'source .venv/bin/activate; pip install -r ./requirements.txt' to install dependencies. \n \
4. Write some code. \n \
5. 'dac test --generate' to generate boilerplate tests. \n \
6. 'dac test' to launch tests. Optionally, you can specify the resources to test (e.g. 'dac test buckets'). \n \n \
Have fun with your new project! 💻 \
    ")
