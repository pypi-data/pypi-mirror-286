import os
from datetime import datetime
import subprocess

def export_requirements(fpath="/Users/macjianfeng/Dropbox/github/python/py2ls/"):
    """
    Main function to generate a timestamped requirements file and convert it to Poetry dependencies.
    """
    
    current_time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    fpath_requirements = f"{fpath}{current_time}_requirements.txt"
    print("Current date and time:", current_time)

    os.makedirs(os.path.dirname(fpath_requirements), exist_ok=True)

    try:
        with open(fpath_requirements, 'w') as requirements_file:
            subprocess.run(['pip', 'freeze'], stdout=requirements_file, check=True)
        print(f"Requirements have been saved to {fpath_requirements}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the requirements file: {e}")
    txt_corr=[]
    for txt_ in re.split('\n', txt):
        if len(txt_) <=40:
            txt_corr.append(txt_.replace("==",' = "^')+'"\n')
    with open(fpath_requirements.replace('requirements.txt','for_poetry.txt'), 'w') as f:
        f.writelines(txt_corr)

def main():
    export_requirements(fpath="/Users/macjianfeng/Dropbox/github/python/py2ls/") 

if __name__ == "__main__":
    main()
